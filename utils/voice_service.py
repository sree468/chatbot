import io
import re
from gtts import gTTS

# gTTS language code mapping
LANGUAGE_AUDIO_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Kannada": "kn"
}

def clean_text_for_speech(text: str) -> str:
    """Removes markdown syntax, links, and code blocks for smooth speech playback."""
    cleaned = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    cleaned = re.sub(r'[*_#`~]', '', cleaned)
    cleaned = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', cleaned)
    return cleaned.strip()

def generate_speech(text: str, language: str) -> bytes:
    """Converts input text to an MP3 byte stream in the selected language."""
    clean_text = clean_text_for_speech(text)[:2500]
    lang_code = LANGUAGE_AUDIO_CODES.get(language, "en")
    
    tts = gTTS(text=clean_text, lang=lang_code)
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    return buffer.getvalue()