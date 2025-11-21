from fastapi import APIRouter, Form
from app.services.parser_service import parse_resume, parse_jd
from app.services.session_manager import create_session

router = APIRouter()

@router.post("/create-session")
async def create_session_route(
    resume_text: str = Form(...),
    jd_text: str = Form(...)
):
    # Parse resume
    parsed_resume = await parse_resume(resume_text)
    # Parse JD
    parsed_jd = await parse_jd(jd_text)

    # Create session
    session_id = create_session(parsed_resume, parsed_jd)

    return {
        "message": "Session created",
        "session_id": session_id,
        "parsed_resume": parsed_resume,
        "parsed_jd": parsed_jd
    }
