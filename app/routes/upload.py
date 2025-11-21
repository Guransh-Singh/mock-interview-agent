from fastapi import APIRouter, File, UploadFile
from app.services.file_reader import extract_text_from_file
from app.services.parser_service import parse_resume, parse_jd
from app.services.session_manager import create_session

router = APIRouter()

@router.post("/upload-docs")
async def upload_docs(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):
    # Extract text
    resume_text = await extract_text_from_file(resume)
    jd_text = await extract_text_from_file(jd)

    # Parse both
    parsed_resume = await parse_resume(resume_text)
    parsed_jd = await parse_jd(jd_text)

    # Make session
    session_id = create_session(parsed_resume, parsed_jd)

    return {
        "message": "Documents uploaded & parsed successfully.",
        "session_id": session_id,
        "resume_preview": resume_text[:500],
        "jd_preview": jd_text[:500]
    }
