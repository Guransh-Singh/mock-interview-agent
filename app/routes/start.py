from fastapi import APIRouter, Form
from app.services.question_service import generate_questions
from app.services.session_manager import SESSIONS

router = APIRouter()

@router.post("/start-interview")
async def start_interview(
    session_id: str = Form(...),
    question_count: int = Form(5)
):
    session = SESSIONS.get(session_id)
    
    if not session:
        return {"error": "Invalid session_id"}

    resume = session["resume"]
    jd = session["jd"]

    questions = await generate_questions(resume, jd, question_count)

    session["questions"] = questions
    session["current"] = 0
    session["answers"] = []

    # 🔥 METHOD 2: PRINT THE SESSION TO THE CONSOLE
    print("\n================ SESSION DEBUG ================")
    print(session)
    print("===============================================\n")

    return {
        "message": "Interview started",
        "total_questions": len(questions),
        "first_question": questions[0]
    }
