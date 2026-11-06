import io
import streamlit as st


def transcribe_audio(audio_bytes):
    """Transcribe audio from st.audio_input using speech_recognition.
    Returns transcribed text or None if failed."""
    try:
        import speech_recognition as sr
    except ImportError:
        st.warning("Voice input requires: pip install SpeechRecognition")
        return None

    recognizer = sr.Recognizer()
    try:
        # st.audio_input returns UploadedFile (BytesIO-like)
        audio_data = audio_bytes.read()
        audio_file = io.BytesIO(audio_data)
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        # Try Hindi first, then English
        try:
            text = recognizer.recognize_google(audio, language="hi-IN")
        except sr.UnknownValueError:
            text = recognizer.recognize_google(audio, language="en-IN")
        return text
    except Exception as e:
        st.error(f"Voice transcription failed: {e}")
        return None


def text_to_speech(text):
    """Convert text to speech audio bytes using gTTS.
    Returns bytes (MP3) or None if failed."""
    try:
        from gtts import gTTS
    except ImportError:
        return None

    try:
        # Detect if text is primarily Hindi
        hindi_chars = sum(1 for c in text if "\u0900" <= c <= "\u097f")
        lang = "hi" if hindi_chars > len(text) * 0.3 else "en"

        tts = gTTS(text=text[:500], lang=lang)  # limit length for TTS
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception:
        return None
