import whisper
import tempfile
import os
from imageio_ffmpeg import get_ffmpeg_exe

ffmpeg_path = get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_path)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
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
