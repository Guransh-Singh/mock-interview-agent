from fastapi import APIRouter, File, UploadFile
from app.services.stt_service import speech_to_text

router = APIRouter()

@router.post("/speech-to-text")
async def convert_audio(file: UploadFile = File(...)):
    """
    Convert uploaded audio to text (Whisper local).
    """
    text = await speech_to_text(file)
    return {"transcript": text}
