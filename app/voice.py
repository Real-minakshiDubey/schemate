import io
import streamlit as st


def transcribe_audio(audio_bytes, language_mode: str = "Auto (English / Hindi)"):
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

        # sr.AudioFile expects WAV format. Try directly, or convert with pydub if needed
        try:
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
        except Exception:
            try:
                from pydub import AudioSegment
                audio_file.seek(0)
                seg = AudioSegment.from_file(audio_file)
                wav_io = io.BytesIO()
                seg.export(wav_io, format="wav")
                wav_io.seek(0)
                with sr.AudioFile(wav_io) as source:
                    audio = recognizer.record(source)
            except Exception as conv_err:
                st.error(f"Audio processing error: {conv_err}")
                return None

        # Determine language priority based on user selection or smart fallback
        if language_mode == "English":
            try:
                return recognizer.recognize_google(audio, language="en-IN")
            except sr.UnknownValueError:
                return None
        elif language_mode == "Hindi":
            try:
                return recognizer.recognize_google(audio, language="hi-IN")
            except sr.UnknownValueError:
                return None
        else:
            # Auto mode: try English first so English sentences aren't phonetically written in Devanagari!
            try:
                return recognizer.recognize_google(audio, language="en-IN")
            except sr.UnknownValueError:
                try:
                    return recognizer.recognize_google(audio, language="hi-IN")
                except sr.UnknownValueError:
                    return None
    except Exception as e:
        st.error(f"Voice transcription failed: {e}")
        return None


def clean_text_for_speech(text: str) -> str:
    """Markdown formatting, asterisks, bullets aur special characters ko clean karo
    taaki TTS 'tarankit' ya 'asterisk' bolne ke bajaye saaf bhasha me bole."""
    import re

    # Remove bold/italic markers (* and _)
    text = re.sub(r"[*_~`#]", " ", text)
    # Remove bullet dashes and symbols at start of lines
    text = re.sub(r"^\s*[-•]\s*", "", text, flags=re.MULTILINE)
    # Replace Rupee symbol with 'rupaye' for clear voice readout
    text = text.replace("₹", "रुपये ").replace("Rs.", "रुपये ")
    # Replace multiple hyphens/dashes with space
    text = re.sub(r"[-–—]", " ", text)
    # Collapse multiple spaces and newlines
    text = re.sub(r"\s+", " ", text).strip()
    return text


def text_to_speech(text):
    """Convert text to speech audio bytes using gTTS.
    Returns bytes (MP3) or None if failed."""
    try:
        from gtts import gTTS
    except ImportError:
        return None

    try:
        # Markdown aur asterisks ko pehle clean karo
        speech_text = clean_text_for_speech(text)
        if not speech_text:
            return None

        # Detect if text is primarily Hindi / Devanagari
        hindi_chars = sum(1 for c in speech_text if "\u0900" <= c <= "\u097f")
        lang = "hi" if hindi_chars > len(speech_text) * 0.25 else "en"

        # Limit to first ~600 characters for snappy playback
        tts = gTTS(text=speech_text[:600], lang=lang)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception:
        return None
