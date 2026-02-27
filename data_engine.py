import re
import pandas as pd
from llm_client import generate_code, generate_explanation
from rag_engine import retrieve_context
from visualizer import auto_chart
from config     import AUTO_QUESTIONS


def _extract_code(raw: str) -> str:
    raw = re.sub(r"```python", "", raw)
    raw = re.sub(r"```",       "", raw)
    lines = [l for l in raw.strip().splitlines() if l.strip()]
    return "\n".join(lines).strip()


def _safe_exec(code: str, df: pd.DataFrame):
    local = {"df": df, "pd": pd}
    try:
        exec(code, {"__builtins__": {}}, local)
        if "result" in local:
            return local["result"], None
        user_vars = [k for k in local if k not in ("df", "pd")]
        if user_vars:
            return local[user_vars[-1]], None
        return None, "No result variable found"
    except Exception as e:
        return None, str(e)


def answer_question(df: pd.DataFrame,
                    question: str,
                    history: list) -> dict:

    context = retrieve_context(question)

    prompt = f"""
Dataset context — use these EXACT column names:
{context}

DataFrame is loaded as variable df.
Question: "{question}"

Rules:
- Store answer in variable named result
- Only use pandas (df and pd available)
- No imports
- Max 6 lines
- Return ONLY code
"""
    raw  = generate_code(
        system="Return only Python pandas code. No markdown.",
        user=prompt
    )
    code = _extract_code(raw)

    result, error = _safe_exec(code, df)

    if error:
        retry = f"""
{prompt}
Previous attempt failed: {error}
Column names are case-sensitive. Use exact names from context.
Write simpler corrected code.
"""
        raw           = generate_code(
            system="Return only Python code. Fix the error.",
            user=retry
        )
        code          = _extract_code(raw)
        result, error = _safe_exec(code, df)

    if error or result is None:
        return {
            "answer"      : "Could not compute an answer.",
            "code"        : code,
            "explanation" : f"Error: {error}",
            "chart"       : None
        }

    explain = generate_explanation(
        system="Explain data results in one clear sentence.",
        user=f"""
Question: "{question}"
Code that ran: {code}
Result: {str(result)[:400]}
Write ONE sentence explaining this result with actual numbers.
"""
    )

    return {
        "answer"      : str(result)[:300],
        "code"        : code,
        "explanation" : explain,
        "chart"       : auto_chart(question, result, df)
    }


def run_auto_insights(df: pd.DataFrame) -> list:
    ICONS    = ["📊", "⚠️", "📈", "🔗", "💡"]
    insights = []
    for i, q in enumerate(AUTO_QUESTIONS):
        try:
            out = answer_question(df, q, [])
            insights.append({
                "icon"  : ICONS[i],
                "title" : q[:38] + "..." if len(q) > 38 else q,
                "value" : str(out["answer"])[:60],
                "detail": str(out["explanation"])[:80],
            })
        except Exception as e:
            insights.append({
                "icon"  : ICONS[i],
                "title" : q[:38],
                "value" : "Could not compute",
                "detail": str(e)[:60],
            })
    return insights