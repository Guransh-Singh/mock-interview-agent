# app/services/followup_service.py

from app.services.llm_client import call_llm
import json


async def generate_followup(question_text: str, user_answer: str):

    system = (
        "You are a senior technical interviewer. "
        "Your job is to generate ONLY a follow-up question that probes deeper "
        "into the weaknesses or missing details from the user's answer. "
        "Your output MUST BE a valid JSON object, no markdown, no backticks."
    )

    prompt = f"""
You asked the following technical interview question:

MAIN QUESTION:
{question_text}

USER ANSWER:
{user_answer}

Your task:
- Identify the biggest gap or weakness in the user's answer.
- Generate ONE follow-up question that helps assess deeper knowledge.
- The follow-up must be specific, not generic.

Return JSON:
{{
  "followup": "string"
}}
"""

    response = await call_llm(system, prompt)

    # Try to parse JSON safely
    try:
        data = json.loads(response)
        followup = data.get("followup")
    except Exception:
        # fallback: return the raw text as a follow-up
        followup = response.strip()

    return {"followup": followup}
