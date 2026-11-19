import streamlit as st


def apply_custom_css():
    """Apply ChatGPT/Claude/Perplexity inspired Dark AI SaaS aesthetic without any white boxes."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        /* Color System:
           Main Background: #0B0F19
           Sidebar Background: #101522
           Chat Surface: #0B0F19
           Input & Card Background: #171D2B
           Hover Background: #222A3B
           Border: #252D40
           Primary: #7C5CFC
           Primary Hover: #6D4AFF
           Accent: #A5B4FC
           Main Text: #F1F5F9
           Secondary Text: #94A3B8
           Muted Text: #64748B
        */
        :root {
            --bg-main: #0B0F19;
            --bg-sidebar: #101522;
            --bg-card: #171D2B;
            --bg-hover: #222A3B;
            --border: #252D40;
            --primary: #7C5CFC;
            --primary-hover: #6D4AFF;
            --accent: #A5B4FC;
            --text-main: #F1F5F9;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
        }

        /* 1. Global Background & Typography */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main {
            background-color: var(--bg-main) !important;
            color: var(--text-main) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            -webkit-font-smoothing: antialiased;
        }

        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* 2. Global Scrollbars */
        ::-webkit-scrollbar {
            width: 5px;
            height: 5px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-main);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary);
        }

        /* 3. Global Button & Card Styling */
        button, div[data-testid="stButton"] > button {
            background-color: var(--bg-card) !important;
            color: var(--text-main) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            font-weight: 500 !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: none !important;
        }
        button:hover, div[data-testid="stButton"] > button:hover {
            background-color: var(--bg-hover) !important;
            border-color: var(--primary) !important;
            color: #FFFFFF !important;
        }

        /* 4. Inputs & BaseWeb Dropdowns Dark Rules */
        input, textarea, [data-baseweb="input"], [data-baseweb="base-input"] {
            background-color: var(--bg-card) !important;
            color: var(--text-main) !important;
            border-color: var(--border) !important;
        }
        input:focus, textarea:focus, [data-baseweb="input"]:focus-within {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 1px var(--primary) !important;
        }

        div[data-baseweb="select"] > div {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            color: var(--text-main) !important;
        }
        div[data-baseweb="select"] > div:hover {
            border-color: var(--primary) !important;
        }
        ul[data-baseweb="menu"], [data-baseweb="popover"], div[data-testid="stPopoverBody"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-main) !important;
            border-radius: 10px !important;
        }
        li[data-baseweb="menu-item"] {
            color: var(--text-main) !important;
            background-color: var(--bg-card) !important;
        }
        li[data-baseweb="menu-item"]:hover {
            background-color: var(--bg-hover) !important;
            color: var(--accent) !important;
        }

        /* 5. Radio Buttons in Filters */
        div[data-testid="stRadio"] > div {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            padding: 4px !important;
        }
        div[data-testid="stRadio"] label {
            color: var(--text-secondary) !important;
            font-size: 0.85rem !important;
            border-radius: 6px !important;
            padding: 4px 10px !important;
        }
        div[data-testid="stRadio"] label:hover {
            color: var(--text-main) !important;
            background-color: var(--bg-hover) !important;
        }

        /* 6. Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: var(--bg-sidebar) !important;
            border-right: 1px solid var(--border) !important;
            padding-top: 1rem !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: var(--border) !important;
            margin: 0.75rem 0 !important;
            opacity: 0.5;
        }
        .sidebar-brand-compact {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 6px 8px;
            margin-bottom: 10px;
        }
        .sidebar-brand-icon {
            width: 30px;
            height: 30px;
            border-radius: 8px;
            background: var(--primary);
            color: #FFFFFF;
            font-size: 1.05rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .sidebar-brand-name {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-main);
            letter-spacing: -0.02em;
        }
        .sidebar-brand-badge {
            font-size: 0.65rem;
            color: var(--accent);
            font-weight: 500;
            background: rgba(124, 92, 252, 0.15);
            padding: 2px 6px;
            border-radius: 4px;
            margin-left: 4px;
        }

        .new-chat-btn div.stButton > button {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-main) !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            border-radius: 10px !important;
            padding: 10px 14px !important;
            width: 100% !important;
            text-align: left !important;
            justify-content: flex-start !important;
        }
        .new-chat-btn div.stButton > button:hover {
            background-color: var(--bg-hover) !important;
            border-color: var(--primary) !important;
            color: #FFFFFF !important;
            transform: translateY(-1px) !important;
        }

        [data-testid="stSidebar"] [data-testid="stTextInput"] input {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            color: var(--text-main) !important;
            font-size: 0.86rem !important;
        }

        .history-section-header {
            font-size: 0.72rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin: 12px 6px 6px 6px;
        }

        .history-btn div.stButton > button {
            background-color: transparent !important;
            border: 1px solid transparent !important;
            color: var(--text-secondary) !important;
            border-radius: 8px !important;
            padding: 7px 10px !important;
            font-size: 0.86rem !important;
            font-weight: 400 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            width: 100% !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }
        .history-btn div.stButton > button:hover {
            background-color: var(--bg-hover) !important;
            color: var(--text-main) !important;
        }
        .history-btn-active div.stButton > button {
            background-color: var(--bg-card) !important;
            border-color: var(--border) !important;
            color: var(--text-main) !important;
            font-weight: 600 !important;
        }

        /* 7. Welcome Hero & Suggested Cards */
        .welcome-compact-hero {
            max-width: 860px;
            margin: 28px auto 16px auto;
            text-align: center;
        }
        .welcome-icon-box {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: rgba(124, 92, 252, 0.15);
            border: 1px solid rgba(124, 92, 252, 0.35);
            color: var(--accent);
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px auto;
        }
        .welcome-hero-heading {
            font-size: 1.65rem;
            font-weight: 700;
            color: var(--text-main);
            letter-spacing: -0.025em;
            margin-bottom: 6px;
        }
        .welcome-hero-sub {
            font-size: 0.94rem;
            color: var(--text-secondary);
            max-width: 580px;
            margin: 0 auto 24px auto;
            line-height: 1.5;
            font-weight: 400;
        }

        .suggestions-wrapper {
            max-width: 860px;
            margin: 0 auto 24px auto;
        }
        .prompt-card div.stButton > button {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-main) !important;
            border-radius: 12px !important;
            padding: 14px 16px !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            width: 100% !important;
            min-height: 64px !important;
            line-height: 1.4 !important;
            box-shadow: none !important;
        }
        .prompt-card div.stButton > button:hover {
            background-color: var(--bg-hover) !important;
            border-color: var(--primary) !important;
            color: #FFFFFF !important;
            transform: translateY(-2px) !important;
        }

        /* 8. Chat Message Bubbles */
        .main-chat-container {
            max-width: 880px;
            margin: 0 auto;
            padding-bottom: 120px;
        }
        [data-testid="stChatMessage"] {
            background-color: transparent !important;
            border: none !important;
            padding: 14px 0 !important;
            margin-bottom: 10px !important;
            font-size: 0.95rem !important;
            line-height: 1.65 !important;
            max-width: 880px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
        div[data-testid="stChatMessage"][aria-label="Chat message from user"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 16px !important;
            padding: 14px 18px !important;
        }

        /* 9. NATIVE CHAT INPUT CONTAINER & FIXED MIC BUTTON
           Position: inside [data-testid="stChatInput"] immediately to the left of the send button
        */
        [data-testid="stChatInput"] {
            background-color: transparent !important;
            padding: 0 !important;
            max-width: 880px !important;
            margin: 0 auto !important;
        }
        [data-testid="stChatInput"] > div {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
            padding: 4px 8px !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45) !important;
            transition: all 0.2s ease !important;
        }
        [data-testid="stChatInput"] > div:focus-within {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(124, 92, 252, 0.25) !important;
        }
        [data-testid="stChatInput"] textarea {
            color: var(--text-main) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.94rem !important;
            line-height: 1.5 !important;
            padding: 8px 60px 8px 12px !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: var(--text-muted) !important;
        }

        /* Send button at right */
        [data-testid="stChatInput"] button {
            background-color: var(--primary) !important;
            color: #FFFFFF !important;
            border-radius: 10px !important;
            border: none !important;
            width: 32px !important;
            height: 32px !important;
            transition: background 0.2s ease !important;
        }
        [data-testid="stChatInput"] button:hover {
            background-color: var(--primary-hover) !important;
        }

        /* FIXED MICROPHONE BUTTON INSIDE CHAT INPUT (Immediately left of send button) */
        .st-chat-mic-anchor {
            position: fixed;
            bottom: 28px;
            right: calc((100vw - 880px) / 2 + 56px);
            z-index: 9999999;
        }
        @media (max-width: 1200px) {
            .st-chat-mic-anchor {
                right: calc((100vw - 700px) / 2 + 56px);
            }
        }
        @media (max-width: 900px) {
            .st-chat-mic-anchor {
                right: 76px;
            }
        }

        .st-chat-mic-anchor div[data-testid="stPopover"] > button {
            background: transparent !important;
            border: none !important;
            color: var(--accent) !important;
            width: 32px !important;
            height: 32px !important;
            padding: 0 !important;
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 1.25rem !important;
            box-shadow: none !important;
            border-radius: 8px !important;
            transition: all 0.15s ease !important;
        }
        .st-chat-mic-anchor div[data-testid="stPopover"] > button:hover {
            background: rgba(124, 92, 252, 0.2) !important;
            color: #FFFFFF !important;
            transform: scale(1.1) !important;
        }

        /* 10. Authentication Card & Branding */
        .auth-page-container {
            max-width: 460px;
            margin: 20px auto 40px auto;
            padding: 28px 30px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 18px;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45);
        }
        @media (max-width: 600px) {
            .auth-page-container {
                margin: 10px 8px;
                padding: 20px 14px;
            }
        }
        .auth-wrapper {
            text-align: center;
            margin-bottom: 20px;
        }
        .auth-brand-logo {
            width: 52px;
            height: 52px;
            line-height: 52px;
            margin: 0 auto 10px auto;
            background: rgba(124, 92, 252, 0.15);
            border: 1px solid rgba(124, 92, 252, 0.35);
            border-radius: 14px;
            font-size: 1.6rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .auth-title {
            font-size: 1.55rem;
            font-weight: 700;
            color: var(--text-main);
            letter-spacing: -0.02em;
            margin-bottom: 4px;
        }
        .auth-subtitle {
            font-size: 0.88rem;
            color: var(--text-secondary);
        }

        /* Tabs Dark Styling */
        div[data-baseweb="tab-list"] {
            background-color: var(--bg-main) !important;
            border-radius: 10px !important;
            padding: 4px !important;
            border: 1px solid var(--border) !important;
            gap: 6px !important;
        }
        div[data-baseweb="tab"] {
            border-radius: 8px !important;
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            padding: 8px 16px !important;
            transition: all 0.2s ease !important;
        }
        div[data-baseweb="tab"][aria-selected="true"] {
            background-color: var(--bg-card) !important;
            color: #FFFFFF !important;
            border-bottom: 2px solid var(--primary) !important;
        }

        /* 11. Language & Onboarding Cards */
        .onboarding-page-container {
            max-width: 680px;
            margin: 20px auto 40px auto;
            padding: 26px 30px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 18px;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45);
        }
        @media (max-width: 600px) {
            .onboarding-page-container {
                margin: 10px 8px;
                padding: 18px 14px;
            }
        }
        .lang-card-wrap {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px 20px;
            transition: all 0.2s ease;
            margin-bottom: 12px;
        }
        .lang-card-wrap:hover {
            border-color: var(--primary);
            background: var(--bg-hover);
        }
        .lang-title-text {
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 4px;
        }
        .lang-desc-text {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }
        .onboarding-progress-badge {
            display: inline-block;
            background: rgba(124, 92, 252, 0.15);
            color: var(--accent);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
            margin-bottom: 12px;
        }
        .sensitive-info-callout {
            background: rgba(124, 92, 252, 0.08);
            border-left: 3px solid var(--primary);
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0 20px 0;
            font-size: 0.86rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        /* 12. Recommendation Dashboard & Scheme Cards */
        .rec-dashboard-header {
            margin-bottom: 24px;
        }
        .rec-profile-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 6px 16px;
            font-size: 0.84rem;
            color: var(--text-secondary);
            margin-bottom: 16px;
        }
        .rec-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 22px 24px;
            margin-bottom: 20px;
            transition: all 0.2s ease;
        }
        .rec-card:hover {
            border-color: rgba(124, 92, 252, 0.5);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        }
        .rec-card-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 12px;
        }
        .rec-scheme-name {
            font-size: 1.22rem;
            font-weight: 700;
            color: var(--text-main);
            line-height: 1.35;
        }
        .rec-badges-row {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 14px;
        }
        .rec-badge-eligible {
            background: rgba(16, 185, 129, 0.16);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.35);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
        }
        .rec-badge-verify {
            background: rgba(245, 158, 11, 0.16);
            color: #FBBF24;
            border: 1px solid rgba(245, 158, 11, 0.35);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
        }
        .rec-badge-not-eligible {
            background: rgba(239, 68, 68, 0.16);
            color: #F87171;
            border: 1px solid rgba(239, 68, 68, 0.35);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
        }
        .tag-central {
            background: rgba(99, 102, 241, 0.15);
            color: #A5B4FC;
            border: 1px solid rgba(99, 102, 241, 0.3);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        .tag-state {
            background: rgba(168, 85, 247, 0.15);
            color: #C084FC;
            border: 1px solid rgba(168, 85, 247, 0.3);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        .rec-reason-box {
            background: rgba(16, 185, 129, 0.06);
            border-left: 3px solid #10B981;
            padding: 10px 14px;
            border-radius: 0 8px 8px 0;
            margin: 10px 0;
            font-size: 0.86rem;
            color: #D1FAE5;
            line-height: 1.5;
        }
        .rec-missing-box {
            background: rgba(245, 158, 11, 0.06);
            border-left: 3px solid #F59E0B;
            padding: 10px 14px;
            border-radius: 0 8px 8px 0;
            margin: 10px 0;
            font-size: 0.86rem;
            color: #FEF3C7;
            line-height: 1.5;
        }
        .rec-disqualify-box {
            background: rgba(239, 68, 68, 0.06);
            border-left: 3px solid #EF4444;
            padding: 10px 14px;
            border-radius: 0 8px 8px 0;
            margin: 10px 0;
            font-size: 0.86rem;
            color: #FECACA;
            line-height: 1.5;
        }
        .rec-section-subhead {
            font-size: 0.82rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin: 12px 0 6px 0;
        }
        .doc-pill {
            display: inline-block;
            background: var(--bg-hover);
            color: var(--text-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 3px 8px;
            font-size: 0.78rem;
            margin: 3px 4px 3px 0;
        }
        .disclaimer-banner {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px 18px;
            margin-top: 30px;
            font-size: 0.82rem;
            color: var(--text-muted);
            line-height: 1.5;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sources(sources):
    """Show verified source citations with modern badges, official links, and relevance scores."""
    if not sources:
        return
    with st.expander(f"📚 Verified Scheme Sources ({len(sources)} identified)", expanded=False):
        for i, s in enumerate(sources, 1):
            level = s.get("level", "").lower()
            region = s.get("region") or "All India"
            badge = "🏛️ Central" if level == "central" else f"🗺️ State ({region})"
            section = s.get("section", "details").capitalize()
            score = s.get("score", 0.0)
            link_md = f" • [Official Portal ↗]({s['official_link']})" if s.get("official_link") else ""

            with st.container(border=True):
                st.markdown(f"**{i}. {s['name']}**  `:violet[{badge}]` &nbsp; Match: `{score:.1%}`")
                st.caption(f"📍 {region} • 📄 Section: `{section}`{link_md}")


def render_welcome():
    """Welcome Hero with interactive suggestion cards in a 2-column layout."""
    st.markdown("### 🏛️ Your Government Scheme Copilot")
    st.caption("Discover government schemes, check eligibility, and understand benefits — in your language.")
    st.markdown("")

    col1, col2 = st.columns(2)
    prompts = [
        ("🎓", "Find scholarships for students in Madhya Pradesh"),
        ("💼", "Which schemes support women entrepreneurs?"),
        ("🌾", "What benefits does PM-KISAN provide?"),
        ("🤝", "Find schemes for low-income families"),
    ]

    for idx, (emoji, prompt_text) in enumerate(prompts):
        col = col1 if idx % 2 == 0 else col2
        with col:
            btn_label = f"{emoji}  {prompt_text}"
            if st.button(btn_label, key=f"welcome_prompt_{idx}", use_container_width=True):
                st.session_state["pending_query"] = prompt_text
                st.rerun()
