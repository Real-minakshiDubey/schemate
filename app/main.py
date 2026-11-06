import sys
from pathlib import Path

# Add project root to sys.path so retrieval.rag and app imports work properly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from app.components import apply_custom_css, render_sources, render_welcome
from app.voice import transcribe_audio, text_to_speech

try:
    from retrieval.rag import ask
except ImportError:
    # Graceful fallback agar retrieval/rag.py abhi ready na ho
    def ask(query: str, level_filter: str | None = None):
        return {
            "answer": "RAG module abhi load nahi hua. Kripya `retrieval/rag.py` check karein.",
            "sources": [],
        }


# Handle model loading / RAG pipeline with @st.cache_resource
@st.cache_resource(show_spinner="AI models initialize ho rahe hain...")
def get_rag_engine():
    """Cache the RAG ask function or pipeline to avoid re-initializing models on every rerun."""
    try:
        from retrieval.rag import ask as _ask
        return _ask
    except ImportError:
        return ask


# Page configuration
st.set_page_config(page_title="SchemeSense", page_icon="🏛️", layout="wide")

# Apply modern colorful styling
apply_custom_css()

# Main Vibrant Header Banner
st.markdown(
    """
    <div class="main-header-container">
        <h1 class="main-header-title">🏛️ SchemeSense</h1>
        <div class="main-header-sub">
            AI-powered Government Scheme Discovery & Eligibility Assistant
        </div>
        <div class="lang-pill-container">
            <span class="lang-pill">🌐 Hindi / हिन्दी</span>
            <span class="lang-pill">🇬🇧 English</span>
            <span class="lang-pill">🔀 Hinglish</span>
            <span class="lang-pill">🎙️ Voice Input & Audio Output</span>
            <span class="lang-pill">⚡ Multilingual E5 + Gemini 2.5</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Filter")
    level_option = st.radio(
        "Scheme Level",
        options=["All", "State", "Central"],
        index=0,
        help="Filter schemes by government level",
    )
    level_filter_map = {
        "All": None,
        "State": "state",
        "Central": "central",
    }
    level_filter = level_filter_map[level_option]

    st.markdown("---")
    st.subheader("🎤 Voice Input")
    voice_lang = st.selectbox(
        "Speaking Language",
        options=["English", "Auto (English / Hindi)", "Hindi"],
        index=0,
        help="Select English if speaking in English, or Hindi for pure Hindi",
    )
    st.caption("Apna sawal bolkar poochiye:")
    audio_value = st.audio_input("Apna sawal boliye...")

    voice_query = None
    if audio_value is not None:
        # Track processed audio using content hash to prevent re-querying on rerun
        audio_bytes_val = audio_value.getvalue() if hasattr(audio_value, "getvalue") else None
        audio_hash = hash(audio_bytes_val) if audio_bytes_val is not None else id(audio_value)
        if st.session_state.get("last_audio_hash") != audio_hash:
            st.session_state["last_audio_hash"] = audio_hash
            if hasattr(audio_value, "seek"):
                audio_value.seek(0)
            with st.spinner("Voice audio transcribe ho raha hai..."):
                transcribed = transcribe_audio(audio_value, language_mode=voice_lang)
            if transcribed:
                st.success(f"Transcript: {transcribed}")
                voice_query = transcribed
            else:
                st.warning("Voice samajh nahi aayi, kripya dobara bole ya type karein.")

    st.markdown("---")
    st.subheader("ℹ️ About SchemeSense")
    st.markdown(
        """
        **SchemeSense** ek RAG-based multilingual assistant hai jo nagrikon ko 
        sarkari yojanaon (Central aur Madhya Pradesh) ki sahi jaankari deta hai.
        
        - 🌐 **Bhashayein**: Hindi, English, Hinglish
        - 📚 **Data**: Verified Central & MP government schemes
        - 🤖 **Models**: Multilingual E5 + Gemini 2.5 Flash
        - 🎤 **Voice**: Speech Recognition & TTS
        """
    )

# --- Main Chat Area ---
# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show welcome screen if no messages yet
if not st.session_state.messages:
    render_welcome()

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            render_sources(msg["sources"])
        if msg.get("audio"):
            st.audio(msg["audio"], format="audio/mp3")

# Chat input
text_query = st.chat_input("Apna sawal poochiye...")

# Use query from voice if transcribed, otherwise from text input
query = voice_query if voice_query else text_query

if query:
    # 1. Add user message to session state
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # 2. Get response from assistant
    with st.chat_message("assistant"):
        with st.spinner("Schemes dhoond raha hoon..."):
            rag_ask = get_rag_engine()
            result = rag_ask(query, level_filter=level_filter)

        answer = result.get("answer", "") if isinstance(result, dict) else str(result)
        sources = result.get("sources", []) if isinstance(result, dict) else []

        # Display answer with st.markdown
        st.markdown(answer)

        # Call render_sources(result['sources'])
        render_sources(sources)

        # Optionally play TTS audio with st.audio
        audio_bytes = text_to_speech(answer)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")

        # Add assistant message to session state
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "audio": audio_bytes,
        })
