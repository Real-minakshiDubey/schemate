"""
Sidebar component for Schemate AI.
Provides navigation between Recommendations, AI Chatbot, and Profile editing,
instant language switcher, search, persistent conversation history,
jurisdiction filter, and anchored user profile.
Uses native Streamlit components for clean, robust rendering.
"""

import uuid
import streamlit as st
from app.db import (
    get_user_conversations,
    create_conversation,
    delete_conversation,
    update_conversation_title,
    get_conversation_messages,
    set_user_language,
    get_user_profile,
)
from app.translations import t


def render_sidebar(user: dict):
    """
    Renders sidebar with navigation, language toggle, new chat,
    conversation history, scheme filter, and anchored user profile.
    """
    user_id = user["id"]
    profile = get_user_profile(user_id) or {}
    cur_lang = profile.get("preferred_language", "en")
    active_view = st.session_state.get("active_view", "recommendations")

    with st.sidebar:
        # Header: Compact Schemate AI Branding
        st.markdown("### 🏛️ Schemate AI :violet-background[PRO]")

        # -------------------------------------------------------------
        # 1. Main Navigation: Recommendations | Saved | Chat | Profile
        # -------------------------------------------------------------
        rec_style = "primary" if active_view == "recommendations" else "secondary"
        if st.button(
            t("nav_recommendations", cur_lang),
            use_container_width=True,
            type=rec_style,
            key="nav_btn_recs"
        ):
            st.session_state.active_view = "recommendations"
            st.rerun()

        saved_style = "primary" if active_view == "saved_schemes" else "secondary"
        if st.button(
            t("nav_saved_schemes", cur_lang),
            use_container_width=True,
            type=saved_style,
            key="nav_btn_saved_schemes"
        ):
            st.session_state.active_view = "saved_schemes"
            st.rerun()

        chat_style = "primary" if active_view == "chat" else "secondary"
        if st.button(
            t("nav_chat", cur_lang),
            use_container_width=True,
            type=chat_style,
            key="nav_btn_chat"
        ):
            st.session_state.active_view = "chat"
            st.rerun()

        prof_style = "primary" if active_view == "profile" else "secondary"
        if st.button(
            t("nav_profile", cur_lang),
            use_container_width=True,
            type=prof_style,
            key="nav_btn_profile"
        ):
            st.session_state.active_view = "profile"
            st.rerun()

        st.markdown("")

        # -------------------------------------------------------------
        # 2. Language Switcher (Quick Toggle)
        # -------------------------------------------------------------
        with st.expander(f"🌐 {t('nav_language', cur_lang)}: {cur_lang.upper()}", expanded=False):
            lang_options = ["English", "हिंदी", "Hinglish"]
            lang_code_map = {"English": "en", "हिंदी": "hi", "Hinglish": "hinglish"}
            inv_map = {"en": "English", "hi": "हिंदी", "hinglish": "Hinglish"}

            cur_label = inv_map.get(cur_lang, "English")
            chosen_label = st.radio(
                "Interface Language",
                options=lang_options,
                index=lang_options.index(cur_label) if cur_label in lang_options else 0,
                label_visibility="collapsed",
                key="sidebar_lang_radio"
            )
            selected_code = lang_code_map[chosen_label]
            if selected_code != cur_lang:
                set_user_language(user_id, selected_code)
                if "user_profile" in st.session_state and st.session_state.user_profile:
                    st.session_state.user_profile["preferred_language"] = selected_code
                st.rerun()

        # -------------------------------------------------------------
        # 3. New Chat & Chat History
        # -------------------------------------------------------------
        if st.button("➕  New Chat", use_container_width=True, key="new_chat_btn"):
            st.session_state.current_conversation_id = None
            st.session_state.messages = []
            st.session_state.active_view = "chat"
            st.rerun()

        # Search History Input
        search_query = st.text_input(
            "Search chats",
            placeholder="🔍 Search conversations...",
            label_visibility="collapsed",
            key="chat_search_input"
        )

        # Fetch user's persistent conversations
        conversations = get_user_conversations(user["id"])

        if search_query.strip():
            conversations = [
                c for c in conversations
                if search_query.strip().lower() in c["title"].lower()
            ]

        # Chat History List
        st.markdown("##### 💬 Recent Chats")

        if not conversations:
            st.caption("No conversations yet.")
        else:
            current_cid = st.session_state.get("current_conversation_id")
            for conv in conversations:
                cid = conv["id"]
                title = conv["title"]
                is_active = (cid == current_cid and active_view == "chat")

                col_item, col_menu = st.columns([0.82, 0.18])

                with col_item:
                    display_title = title if len(title) <= 24 else title[:22] + "..."
                    btn_type = "primary" if is_active else "secondary"
                    if st.button(f"💬 {display_title}", key=f"conv_select_{cid}", use_container_width=True, type=btn_type):
                        st.session_state.current_conversation_id = cid
                        st.session_state.messages = get_conversation_messages(cid, user["id"])
                        st.session_state.active_view = "chat"
                        st.rerun()

                with col_menu:
                    with st.popover("⋮", help="Options"):
                        st.markdown("**Chat Options**")
                        # Rename option
                        new_name = st.text_input("Rename title", value=title, key=f"rename_input_{cid}")
                        if st.button("Save Title", key=f"save_title_{cid}", use_container_width=True):
                            if new_name.strip():
                                update_conversation_title(cid, user["id"], new_name.strip())
                                st.rerun()

                        st.markdown("---")
                        # Delete option
                        if st.button("🗑️ Delete Chat", key=f"pop_del_{cid}", use_container_width=True):
                            delete_conversation(cid, user["id"])
                            if st.session_state.get("current_conversation_id") == cid:
                                st.session_state.current_conversation_id = None
                                st.session_state.messages = []
                            st.rerun()

        # Collapsible Scheme Filter Section
        with st.expander("⚙️ Scheme Jurisdiction Filter", expanded=False):
            level_option = st.radio(
                "Filter by Level",
                options=["All", "State", "Central"],
                index=0,
                help="Filter schemes by government jurisdiction level",
                label_visibility="collapsed",
                key="sidebar_level_filter"
            )
            level_filter_map = {"All": None, "State": "state", "Central": "central"}
            st.session_state["level_filter"] = level_filter_map[level_option]

        st.markdown("---")

        # User Profile Section Anchored at Bottom
        user_name = user.get("name", "User")
        user_email = user.get("email", "")

        st.markdown(f"**👤 {user_name}**")
        st.caption(f"{user_email}")

        with st.expander("👤 My Account & Settings", expanded=False):
            st.markdown(f"**Name:** {user_name}")
            st.markdown(f"**Email:** `{user_email}`")
            if profile.get("state"):
                st.markdown(f"**State:** {profile['state']}")
            if profile.get("occupation"):
                st.markdown(f"**Occupation:** {profile['occupation']}")
            st.markdown(f"**Language:** {cur_lang.upper()}")
            st.markdown(f"**Plan:** Schemate Standard")
            st.markdown("---")
            if st.button("🚪 Log Out", use_container_width=True, key="sidebar_logout_btn"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
