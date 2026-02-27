# rag_engine.py  — B2 owns this file
import hashlib
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import chromadb
from chromadb.config import Settings

from llm_client import get_embedding
from config import CHROMA_DIR

# Persistent client so index survives Streamlit reruns
_chroma   = chromadb.PersistentClient(path=CHROMA_DIR)
_col      = None
_last_hash = None


def _hash(df: pd.DataFrame) -> str:
    """Short hash to detect if CSV content changed."""
    return hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()[:10]


def _col_id(col: str) -> str:
    """Collision-safe ChromaDB id for a column name."""
    return f'col_{hashlib.md5(col.encode()).hexdigest()[:8]}'


def build_rag_index(df: pd.DataFrame) -> str:
    """Index the entire CSV schema into ChromaDB."""
    global _col, _last_hash

    h = _hash(df)
    if h == _last_hash:
        return h  # Same file — skip rebuild

    try:
        _chroma.delete_collection('csv_context')
    except Exception:
        pass  # Collection didn't exist yet — fine

    _col       = _chroma.create_collection('csv_context')
    _last_hash = h
    docs, ids  = [], []

    # ── Chunk 1: Overall schema summary ──────────────────────
    docs.append(
        f'Dataset has {df.shape[0]} rows and {df.shape[1]} columns. '
        f'Column names: {list(df.columns)}'
    )
    ids.append('schema')

    # ── Chunk per column: name + type + stats ────────────────
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = int(df[col].isnull().sum())
        null_pct = f'{nulls/len(df)*100:.1f}%'

        if pd.api.types.is_numeric_dtype(df[col]):
            chunk = (
                f'Column {col}: numeric ({dtype}), '
                f'min={df[col].min():.4g}, max={df[col].max():.4g}, '
                f'mean={df[col].mean():.4g}, std={df[col].std():.4g}, '
                f'median={df[col].median():.4g}, '
                f'nulls={nulls} ({null_pct})'
            )
        else:
            vals = df[col].dropna().unique()[:6].tolist()
            chunk = (
                f'Column {col}: categorical ({dtype}), '
                f'unique={df[col].nunique()}, sample={vals}, '
                f'nulls={nulls} ({null_pct})'
            )
        docs.append(chunk)
        ids.append(_col_id(col))

    # ── Chunk: Top correlations (numeric columns only) ───────
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if len(numeric_cols) >= 2:
        corr    = df[numeric_cols].corr().unstack()
        top     = corr[corr.abs() < 1].abs().nlargest(6)
        corr_str = 'Top correlations: ' + ', '.join(
            f'{a}↔{b}={v:.2f}' for (a, b), v in top.items()
        )
        docs.append(corr_str)
        ids.append('correlations')

    # ── Chunk: Sample rows ───────────────────────────────────
    docs.append('Sample data rows:\n' + df.head(5).to_string(index=False))
    ids.append('sample_rows')

    # ── Embed in parallel, then store ────────────────────────
    with ThreadPoolExecutor(max_workers=4) as ex:
        embs = list(ex.map(get_embedding, docs))

    _col.add(documents=docs, ids=ids, embeddings=embs)
    return h


def retrieve_context(question: str, n: int = 4) -> str:
    """Find top-n most relevant chunks to inject into the LLM prompt."""
    if _col is None or _col.count() == 0:
        return 'No dataset loaded yet.'
    try:
        q_emb = get_embedding(question)
    except Exception as e:
        return f'[RAG error: could not embed question — {e}]'

    results = _col.query(
        query_embeddings=[q_emb],
        n_results=min(n, _col.count())
    )
    chunks = results['documents'][0] if results['documents'] else []
    return '\n\n'.join(chunks)