import sys
import uuid
from pathlib import Path

# Add project root to sys.path so retrieval.rag and app imports work seamlessly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from app.components import apply_custom_css, render_sources, render_welcome
from app.auth import render_auth_view
from app.sidebar import render_sidebar
from app.voice import text_to_speech, transcribe_audio
from app.db import (
    create_conversation,
    add_message,
    get_conversation_messages,
    update_conversation_title,
    get_user_profile,
    is_onboarding_completed,
)
from app.onboarding_ui import render_onboarding_view
from app.recommendations_ui import render_recommendations_view
from app.profile_ui import render_profile_view
from app.saved_schemes_ui import render_saved_schemes_view

# ---------------------------------------------------------------------------
# RAG Engine loader with caching
# ---------------------------------------------------------------------------
try:
    from retrieval.rag import ask
except ImportError:
    def ask(query: str, level_filter: str | None = None, user_profile: dict | None = None):
        return {
            "answer": "RAG module not found. Please verify `retrieval/rag.py`.",
            "sources": [],
        }


@st.cache_resource(show_spinner="Initializing Schemate AI models...")
def get_rag_engine():
    """Cache the RAG ask pipeline to avoid re-initializing models on every rerun."""
    try:
        from retrieval.rag import ask as _ask
        return _ask
    except ImportError:
        return ask


# ---------------------------------------------------------------------------
# Streamlit Page Setup & Styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Schemate AI - Personalized Government Scheme Discovery",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styling
apply_custom_css()

# ---------------------------------------------------------------------------
# Authentication Gate
# ---------------------------------------------------------------------------
if "user" not in st.session_state or not st.session_state.user:
    render_auth_view()
    st.stop()

# Authenticated User Context
current_user = st.session_state.user

# ---------------------------------------------------------------------------
# Onboarding Gate
# ---------------------------------------------------------------------------
user_profile = get_user_profile(current_user["id"])
onboarding_done = is_onboarding_completed(current_user["id"])

# If user has not completed onboarding, route directly to the onboarding workflow
if not onboarding_done:
    render_onboarding_view(current_user)
    st.stop()

# Set active profile in session state
st.session_state.user_profile = user_profile

# Default active view for onboarded users is recommendations unless switched to chat or profile
if "active_view" not in st.session_state:
    st.session_state.active_view = "recommendations"

# ---------------------------------------------------------------------------
# Sidebar (ChatGPT-style with history, new chat, filters, and user account)
# ---------------------------------------------------------------------------
render_sidebar(current_user)

# ---------------------------------------------------------------------------
# View Routing: Recommendations | Saved Schemes | Profile | Chat
# ---------------------------------------------------------------------------
active_view = st.session_state.get("active_view", "recommendations")

if active_view == "recommendations":
    render_recommendations_view(current_user)

elif active_view == "saved_schemes":
    render_saved_schemes_view(current_user)

elif active_view == "profile":
    render_profile_view(current_user)

elif active_view == "chat":
    # ---------------------------------------------------------------------------
    # Main Chat Area
    # ---------------------------------------------------------------------------
    # Initialize active messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # If an existing conversation is active, ensure messages are loaded if empty
    current_cid = st.session_state.get("current_conversation_id")
    if current_cid and not st.session_state.messages:
        st.session_state.messages = get_conversation_messages(current_cid, current_user["id"])

    # Show welcome screen if no messages in current view
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

    # ---------------------------------------------------------------------------
    # Chat Composer: Text Input + Fixed 🎙️ Microphone + Send Button
    # ---------------------------------------------------------------------------
    pending_query = st.session_state.pop("pending_query", None)
    voice_query = None

    # Native Chat Input
    text_query = st.chat_input("Ask anything about Indian Government Schemes...")

    # Microphone Popover positioned directly inside the chat bar left of Send button
    st.markdown('<div class="st-chat-mic-anchor">', unsafe_allow_html=True)
    with st.popover("🎙️", help="Voice Input (Click to speak)"):
        st.markdown("##### 🎙️ Voice Input")
        v_lang = st.selectbox(
            "Speaking Language",
            options=["English", "Auto (English / Hindi)", "Hindi"],
            index=0,
            key="chat_mic_lang"
        )
        audio_val = st.audio_input("Record voice query", label_visibility="collapsed", key="chat_mic_rec")
        if audio_val is not None:
            audio_bytes_val = audio_val.getvalue() if hasattr(audio_val, "getvalue") else None
            audio_hash = hash(audio_bytes_val) if audio_bytes_val is not None else id(audio_val)
            if st.session_state.get("last_audio_hash") != audio_hash:
                st.session_state["last_audio_hash"] = audio_hash
                if hasattr(audio_val, "seek"):
                    audio_val.seek(0)
                with st.spinner("Transcribing voice audio..."):
                    transcribed = transcribe_audio(audio_val, language_mode=v_lang)
                if transcribed:
                    st.success(f"Recognized: {transcribed}")
                    voice_query = transcribed
                else:
                    st.warning("Speech not recognized, please speak clearly.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Determine final query to process
    query = pending_query if pending_query else (voice_query if voice_query else text_query)

    if query and query.strip():
        user_text = query.strip()

        # 1. Ensure a conversation exists for persistent storage
        if not current_cid:
            current_cid = str(uuid.uuid4())
            conv_title = user_text[:35] + ("..." if len(user_text) > 35 else "")
            create_conversation(current_user["id"], current_cid, conv_title)
            st.session_state.current_conversation_id = current_cid

        # 2. Add user message to UI and save to persistent database
        st.session_state.messages.append({"role": "user", "content": user_text})
        add_message(current_user["id"], current_cid, "user", user_text)

        with st.chat_message("user"):
            st.markdown(user_text)

        # 3. Retrieve and Generate answer via personalized RAG pipeline
        with st.chat_message("assistant"):
            level_filter = st.session_state.get("level_filter")
            with st.spinner("Searching official government schemes & evaluating eligibility..."):
                rag_ask = get_rag_engine()
                # Pass user_profile into rag_ask
                result = rag_ask(
                    user_text,
                    level_filter=level_filter,
                    user_profile=user_profile
                )

            answer = result.get("answer", "") if isinstance(result, dict) else str(result)
            sources = result.get("sources", []) if isinstance(result, dict) else []

            # Display answer
            st.markdown(answer)

            # Display sources
            if sources:
                render_sources(sources)

            # Generate audio output via existing voice integration
            audio_bytes = text_to_speech(answer)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")

            # Save assistant message to persistent DB
            add_message(
                current_user["id"],
                current_cid,
                "assistant",
                answer,
                sources=sources,
                audio_blob=audio_bytes
            )

            # Append to active session messages
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources,
                "audio": audio_bytes,
            })
