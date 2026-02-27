    
LM_STUDIO_URL   = "http://10.149.95.50:1234/v1"
REASONING_MODEL = "qwen2.5-coder-7b-instruct"
EMBEDDING_MODEL = "text-embedding-all-minilm-l6-v2"
CHROMA_DIR      = "./chroma_store"
MAX_TOKENS      = 1024
TEMP_CODE       = 0.1
TEMP_EXPLAIN    = 0.3

AUTO_QUESTIONS = [
    "What are the overall statistics of this dataset?",
    "Which columns have the most missing values?",
    "What is the distribution of the most important column?",
    "What are the top correlations between numeric columns?",
    "What is the most interesting pattern in this data?",
]