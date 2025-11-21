# app/routes/improvement.py
from fastapi import APIRouter, Form
from app.services.improvement_service import generate_improvement_plan
from app.services.session_manager import SESSIONS

router = APIRouter()

@router.post("/generate-improvement")
async def generate_improvement(session_id: str = Form(...)):
    session = SESSIONS.get(session_id)
    if not session:
        return {"error": "Invalid session_id"}

    # prepare session summary for the prompt
    summary = {
        "resume": session.get("resume"),
        "jd": session.get("jd"),
        "answers": session.get("answers", [])
    }

    plan = await generate_improvement_plan(summary)
    # store in session
    session["final_plan"] = plan
    return {"improvement_plan": plan}
