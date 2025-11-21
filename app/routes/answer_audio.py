from fastapi import APIRouter, Form, File, UploadFile
from app.services.stt_service import speech_to_text
from app.routes.answer import submit_answer  # reuse existing logic

router = APIRouter()

@router.post("/submit-answer-audio")
async def submit_answer_audio(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    """
    User speaks the answer → convert to text → reuse submit-answer logic.
    """
    transcript = await speech_to_text(file)
    return await submit_answer(session_id=session_id, transcript=transcript)
