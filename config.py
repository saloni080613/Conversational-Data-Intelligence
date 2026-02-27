# config.py — single source of truth for all settings
# B1 fills in LM_STUDIO_URL once server is running

LM_STUDIO_URL     = "http://127.0.0.1:1234"  # B1 updates this
REASONING_MODEL   = "qwen2.5-coder-7b-instruct"
EMBEDDING_MODEL   = "text-embedding-all-minilm-l6-v2"
CHROMA_PERSIST_DIR = "./chroma_store"
MAX_TOKENS        = 1024
TEMPERATURE_CODE  = 0.1   # Low = deterministic code
TEMPERATURE_CHAT  = 0.3   # Slightly higher for explanations

AUTO_INSIGHT_QUESTIONS = [
    "What are the overall statistics of this dataset?",
    "Which columns have missing values and how many?",
    "What is the distribution of the most important column?",
    "What are the top correlations between columns?",
    "What is the most interesting pattern in this data?",
]