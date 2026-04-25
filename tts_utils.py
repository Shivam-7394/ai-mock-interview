from gtts import gTTS
import tempfile

def speak_text(text):
    try:
        tts = gTTS(text=text, lang='en')

        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            return f.name

    except Exception as e:
        return None