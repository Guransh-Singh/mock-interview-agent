import io
import fitz  # PyMuPDF
from docx import Document

async def extract_text_from_file(uploaded):
    file_bytes = await uploaded.read()
    filename = uploaded.filename.lower()

    # PDF (best with fitz)
    if filename.endswith(".pdf"):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    # DOCX
    if filename.endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)

    # Plain text
    try:
        return file_bytes.decode("utf-8")
    except:
        return file_bytes.decode("latin-1")
