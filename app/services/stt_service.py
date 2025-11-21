import whisper
import tempfile
import os
import os
# Add ffmpeg to PATH manually so Python can find it
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

# Load model ONCE (slow on first load, fast afterward)
model = whisper.load_model("base")

async def speech_to_text(file):
    """
    Converts uploaded audio to text using Whisper local model.
    """
    audio_bytes = await file.read()

    # Save audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    # Run transcription
    result = model.transcribe(tmp_path)

    # Delete temp file
    os.remove(tmp_path)

    return result["text"]
