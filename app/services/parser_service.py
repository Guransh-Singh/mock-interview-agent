import re
import json
from .llm_client import call_llm

# Load prompts
with open("app/prompts/resume_parser.txt", "r", encoding="utf-8") as f:
    RESUME_PROMPT = f.read()

with open("app/prompts/jd_parser.txt", "r", encoding="utf-8") as f:
    JD_PROMPT = f.read()


def clean_json(text: str):
    """
    Remove code fences like ```json ... ```
    """
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    return text.strip()


async def parse_resume(text: str):
    system_prompt = (
        "You are a strict resume parser. "
        "Return ONLY valid JSON. "
        "DO NOT wrap in ```json fences. "
        "No explanation text."
    )

    user_prompt = RESUME_PROMPT.replace("{{RESUME_TEXT}}", text)

    response = await call_llm(system_prompt, user_prompt)
    cleaned = clean_json(response)

    try:
        return json.loads(cleaned)
    except Exception as e:
        return {
            "error": "Invalid JSON",
            "raw": cleaned,
            "exception": str(e)
        }


async def parse_jd(text: str):
    system_prompt = (
        "You are a strict job description parser. "
        "Return ONLY valid JSON with no code fences."
    )

    user_prompt = JD_PROMPT.replace("{{JD_TEXT}}", text)

    response = await call_llm(system_prompt, user_prompt)
    cleaned = clean_json(response)

    try:
        return json.loads(cleaned)
    except Exception as e:
        return {
            "error": "Invalid JSON",
            "raw": cleaned,
            "exception": str(e)
        }
