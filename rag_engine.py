# rag_engine.py — RAG indexing & retrieval (ChromaDB-free for Py 3.14 compat)
import hashlib
import numpy as np
import pandas as pd

from llm_client import get_embedding

_docs: list[str] = []
_embeddings: list[list[float]] = []
_last_hash: str | None = None


def _hash(df: pd.DataFrame) -> str:
    """Short hash to detect if CSV content changed."""
    return hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()[:10]


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    a_np = np.array(a, dtype=np.float32)
    b_np = np.array(b, dtype=np.float32)
    dot = np.dot(a_np, b_np)
    norm = np.linalg.norm(a_np) * np.linalg.norm(b_np)
    if norm == 0:
        return 0.0
    return float(dot / norm)


def build_rag_index(df: pd.DataFrame) -> str:
    """Index the entire CSV schema into an in-memory vector store."""
    global _docs, _embeddings, _last_hash

    h = _hash(df)
    if h == _last_hash:
        return h  # Same file — skip rebuild

    _last_hash = h
    new_docs: list[str] = []

    # ── Chunk 1: Overall schema summary ──────────────────────
    new_docs.append(
        f'Dataset has {df.shape[0]} rows and {df.shape[1]} columns. '
        f'Column names: {list(df.columns)}'
    )

    # ── Chunk per column: name + type + stats ────────────────
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = int(df[col].isnull().sum())
        null_pct = f'{nulls / len(df) * 100:.1f}%'

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
        new_docs.append(chunk)

    # ── Chunk: Top correlations (numeric columns only) ───────
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr().unstack()
        top = corr[corr.abs() < 1].abs().nlargest(6)
        corr_str = 'Top correlations: ' + ', '.join(
            f'{a}↔{b}={v:.2f}' for (a, b), v in top.items()
        )
        new_docs.append(corr_str)

    # ── Chunk: Sample rows ───────────────────────────────────
    new_docs.append('Sample data rows:\n' + df.head(4).to_string(index=False))

    # ── Embed all chunks ─────────────────────────────────────
    new_embeddings: list[list[float]] = []
    for d in new_docs:
        new_embeddings.append(get_embedding(d))

    _docs = new_docs
    _embeddings = new_embeddings
    return h


def retrieve_context(question: str, n: int = 4) -> str:
    """Find top-n most relevant chunks by cosine similarity."""
    if not _docs:
        return 'No dataset loaded yet.'

    try:
        q_emb = get_embedding(question)
    except Exception as e:
        return f'[RAG error: could not embed question — {e}]'

    # Compute similarities and pick top-n
    scores = [
        (i, _cosine_similarity(q_emb, emb))
        for i, emb in enumerate(_embeddings)
    ]
    scores.sort(key=lambda x: x[1], reverse=True)
    top = scores[:min(n, len(scores))]

    chunks = [_docs[i] for i, _ in top]
    return '\n\n'.join(chunks)
