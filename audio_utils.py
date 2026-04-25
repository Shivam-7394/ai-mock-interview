from audiorecorder import audiorecorder
import speech_recognition as sr
import tempfile

def record_audio(key=None):
    audio = audiorecorder("🎤 Speak", "⏹ Stop", key=key)
    return audio

def speech_to_text(audio):
    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        audio.export(f.name, format="wav")

        with sr.AudioFile(f.name) as source:
            data = recognizer.record(source)

    try:
        return recognizer.recognize_google(data)
    except:
        return ""