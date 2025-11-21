# app/services/improvement_service.py
import json, re
from .llm_client import call_llm

# load prompt
with open("app/prompts/improvement_plan.txt", "r", encoding="utf-8") as f:
    IMPROVEMENT_PROMPT = f.read()

def clean_text(t: str) -> str:
    t = re.sub(r"```json", "", t, flags=re.I)
    t = re.sub(r"```", "", t)
    return t.strip()

async def generate_improvement_plan(session_summary: dict):
    """
    session_summary: dict with keys:
      - resume (parsed resume)
      - jd (parsed jd)
      - answers (list of {question_text, transcript, evaluation})
    Returns parsed JSON or fallback dict.
    """
    system_prompt = (
        "You are a concise career coach who outputs ONLY valid JSON following the schema in the prompt."
    )

    # Fill template
    user_prompt = IMPROVEMENT_PROMPT.replace("{{SESSION_SUMMARY}}", json.dumps(session_summary))

    resp = await call_llm(system_prompt, user_prompt)
    cleaned = clean_text(resp)
    try:
        return json.loads(cleaned)
    except Exception as e:
        return {"error": "Invalid JSON from model", "raw": cleaned, "exception": str(e)}
