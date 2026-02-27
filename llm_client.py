import requests
from openai import OpenAI
from config import (
    LM_STUDIO_URL,
    REASONING_MODEL,
    EMBEDDING_MODEL,
    MAX_TOKENS,
    TEMP_CODE,
    TEMP_EXPLAIN
)

client = OpenAI(
    base_url = LM_STUDIO_URL,
    api_key  = "lm-studio"
)


def check_server_health() -> dict:
    try:
        r = requests.get(
            f"{LM_STUDIO_URL}/models",
            timeout=5
        )
        if r.status_code == 200:
            models = [m["id"] for m in r.json().get("data", [])]
            return {"status": "online", "models": models}
        return {"status": "error", "models": []}
        resp = client.models.list(timeout=5)
        models = [m.id for m in resp.data]
        return {"status": "online", "models": models}
    except Exception as e:
        return {"status": "offline", "error": str(e)}


def get_embedding(text: str) -> list:
    resp = client.embeddings.create(
        model = EMBEDDING_MODEL,
        input = text[:2000]
    )
    return resp.data[0].embedding


def generate_code(system: str, user: str) -> str:
    resp = client.chat.completions.create(
        model       = REASONING_MODEL,
        messages    = [
            {"role": "system", "content": system},
            {"role": "user",   "content": user}
        ],
        temperature = TEMP_CODE,
        max_tokens  = MAX_TOKENS,
    )
    return resp.choices[0].message.content.strip()


def generate_explanation(system: str, user: str) -> str:
    resp = client.chat.completions.create(
        model       = REASONING_MODEL,
        messages    = [
            {"role": "system", "content": system},
            {"role": "user",   "content": user}
        ],
        temperature = TEMP_EXPLAIN,
        max_tokens  = 512,
    )
    return resp.choices[0].message.content.strip()