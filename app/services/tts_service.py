from gtts import gTTS
import uuid
import os

AUDIO_DIR = "generated_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def text_to_speech(text: str):
    """
    Convert text to MP3 using gTTS (free).
    Returns the file path of the generated audio.
    """
    file_id = str(uuid.uuid4())
    file_path = f"{AUDIO_DIR}/{file_id}.mp3"
    
    tts = gTTS(text=text, lang="en")
    tts.save(file_path)
    
    return file_path
