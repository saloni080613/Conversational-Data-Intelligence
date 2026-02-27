# rag_engine.py
import hashlib
import pandas as pd
import chromadb
from chromadb.config import Settings
from llm_client import get_embedding
from config import CHROMA_DIR

# Initialize ChromaDB in-memory (resets per session) [cite: 251, 252]
_chroma = chromadb.Client(Settings(anonymized_telemetry=False))
_col = None   
_last_hash = None 

def _hash(df: pd.DataFrame) -> str:
    '''Create a short hash to detect if CSV changed.''' [cite: 255, 256]
    return hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()[:10]

def build_rag_index(df: pd.DataFrame) -> str:
    '''Index the entire CSV schema into ChromaDB.''' [cite: 260, 262]
    global _col, _last_hash
    h = _hash(df)
    if h == _last_hash:
        return h 

    # Fresh collection for new file [cite: 270, 271, 275]
    try:
        _chroma.delete_collection('csv_context')
    except Exception:
        pass
    _col = _chroma.create_collection('csv_context')
    _last_hash = h

    docs, ids, embs = [], [], []

    # Chunk 1: Overall schema summary [cite: 278, 281]
    schema = (f'Dataset has {df.shape[0]} rows and {df.shape[1]} columns. '
              f'Column names: {list(df.columns)}')
    docs.append(schema); ids.append('schema')

    # Chunk per column: name + type + stats [cite: 283, 284]
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = int(df[col].isnull().sum())
        if df[col].dtype in ['int64', 'float64']:
            chunk = (f'Column {col}: numeric {dtype}, min={df[col].min():.4g}, '
                    f'max={df[col].max():.4g}, mean={df[col].mean():.4g}, nulls={nulls}')
        else:
            vals = df[col].dropna().unique()[:6].tolist()
            chunk = (f'Column {col}: {dtype}, unique values={df[col].nunique()}, '
                    f'sample={vals}, nulls={nulls}')
        docs.append(chunk)
        ids.append(f'col_{col[:28]}')

    # Chunk: Sample rows for context [cite: 300, 301]
    sample = 'Sample data rows:\n' + df.head(4).to_string(index=False)
    docs.append(sample); ids.append('sample_rows')

    # Embed and store [cite: 303, 305, 306]
    for d in docs:
        embs.append(get_embedding(d))
    _col.add(documents=docs, ids=ids, embeddings=embs)
    return h

def retrieve_context(question: str, n: int = 4) -> str:
    '''Find top-n most relevant chunks to inject into the LLM prompt.''' [cite: 308, 311]
    if _col is None or _col.count() == 0:
        return 'No dataset loaded yet.'
    q_emb = get_embedding(question)
    results = _col.query(query_embeddings=[q_emb], n_results=min(n, _col.count()))
    chunks = results['documents'][0] if results['documents'] else []
    return '\n\n'.join(chunks)