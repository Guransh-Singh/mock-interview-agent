from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from app.services.tts_service import text_to_speech

router = APIRouter()

@router.get("/question-audio")
async def question_audio(text: str = Query(...)):
    """
    Generate audio for a question via GET.
    """
    file_path = text_to_speech(text)
    return FileResponse(file_path, media_type="audio/mpeg")
