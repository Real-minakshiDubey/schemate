import streamlit as st


def apply_custom_css():
    """Apply Deep Indigo + Electric Blue futuristic AI SaaS styling."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        /* Root color variables */
        :root {
            --bg-main: #0A0F1F;
            --bg-sidebar: #11162A;
            --bg-card: #171D35;
            --bg-card-secondary: #1C2442;
            --primary-accent: #6366F1;
            --electric-blue: #38BDF8;
            --text-primary: #F1F5F9;
            --text-secondary: #94A3B8;
            --border-color: #293352;
            --input-bg: #141A30;
            --hover-bg: #222B49;
            --success: #22C55E;
            --warning: #F59E0B;
            --error: #EF4444;
        }

        /* Global Application Background and Font */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0A0F1F !important;
            color: #F1F5F9 !important;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #0A0F1F;
        }
        ::-webkit-scrollbar-thumb {
            background: #293352;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #6366F1;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #11162A !important;
            border-right: 1px solid #293352 !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: #293352 !important;
            margin: 1.2rem 0 !important;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #F1F5F9 !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }

        /* Sidebar Brand Header */
        .sidebar-brand-box {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 14px;
            background: #171D35;
            border: 1px solid #293352;
            border-radius: 14px;
            margin-bottom: 20px;
        }
        .sidebar-brand-icon {
            font-size: 1.6rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 10px;
        }
        .sidebar-brand-text {
            font-size: 1.15rem;
            font-weight: 800;
            color: #F1F5F9;
            letter-spacing: -0.02em;
        }
        .sidebar-brand-tag {
            font-size: 0.7rem;
            color: #38BDF8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Modern Radio Buttons in Sidebar */
        div[data-testid="stRadio"] > div {
            background-color: #141A30;
            border: 1px solid #293352;
            border-radius: 12px;
            padding: 6px;
            gap: 4px;
        }
        div[data-testid="stRadio"] label {
            color: #94A3B8 !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            padding: 6px 12px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stRadio"] label:hover {
            color: #F1F5F9 !important;
            background-color: #222B49 !important;
        }

        /* Selectbox styling */
        div[data-baseweb="select"] > div {
            background-color: #141A30 !important;
            border: 1px solid #293352 !important;
            border-radius: 12px !important;
            color: #F1F5F9 !important;
        }
        div[data-baseweb="select"] > div:hover {
            border-color: #38BDF8 !important;
        }

        /* Hero Card Header */
        .hero-container {
            background: linear-gradient(135deg, rgba(23, 29, 53, 0.9) 0%, rgba(28, 36, 66, 0.9) 100%);
            border: 1px solid #293352;
            border-radius: 18px;
            padding: 26px 30px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px -10px rgba(10, 15, 31, 0.8), 0 0 1px 1px rgba(99, 102, 241, 0.15);
            position: relative;
            overflow: hidden;
        }
        .hero-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #6366F1 0%, #38BDF8 50%, transparent 100%);
        }
        .hero-title-row {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 6px;
        }
        .hero-icon {
            font-size: 2.2rem;
            filter: drop-shadow(0 2px 8px rgba(56, 189, 248, 0.3));
        }
        .hero-title {
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em !important;
            background: linear-gradient(135deg, #F1F5F9 20%, #38BDF8 100%);
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin: 0 !important;
        }
        .hero-sub {
            font-size: 1rem !important;
            color: #94A3B8 !important;
            margin-bottom: 16px !important;
            font-weight: 500 !important;
        }

        /* Feature Badges */
        .feature-badge-row {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .feature-badge {
            background: #1C2442;
            border: 1px solid #293352;
            color: #F1F5F9;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 20px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
        }
        .feature-badge:hover {
            border-color: #38BDF8;
            color: #38BDF8;
            background: #222B49;
        }

        /* Welcome Card */
        .welcome-card-saas {
            background: #171D35;
            border: 1px solid #293352;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }
        .welcome-title {
            font-size: 1.28rem;
            font-weight: 700;
            color: #38BDF8;
            margin-bottom: 8px;
            letter-spacing: -0.01em;
        }
        .welcome-desc {
            font-size: 0.95rem;
            color: #94A3B8;
            line-height: 1.5;
            margin-bottom: 18px;
        }
        .prompt-section-label {
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #6366F1;
            margin-bottom: 10px;
        }

        /* Streamlit Button Styling for Clickable Prompts */
        div.stButton > button {
            background: #1C2442 !important;
            border: 1px solid #293352 !important;
            border-left: 3px solid #38BDF8 !important;
            color: #F1F5F9 !important;
            border-radius: 12px !important;
            padding: 12px 18px !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            text-align: left !important;
            width: 100% !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
        }
        div.stButton > button:hover {
            background: #222B49 !important;
            border-color: #38BDF8 !important;
            color: #38BDF8 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 14px rgba(56, 189, 248, 0.15) !important;
        }

        /* Chat Message Styling */
        [data-testid="stChatMessage"] {
            border-radius: 16px !important;
            padding: 16px 20px !important;
            margin-bottom: 14px !important;
            border: 1px solid #293352 !important;
            font-size: 0.96rem !important;
            line-height: 1.6 !important;
        }
        /* User message container */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
        div[data-testid="stChatMessage"][aria-label="Chat message from user"] {
            background-color: #1C2442 !important;
            border-color: rgba(99, 102, 241, 0.35) !important;
        }
        /* Assistant message container */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]),
        div[data-testid="stChatMessage"][aria-label="Chat message from assistant"] {
            background-color: #171D35 !important;
            border-color: #293352 !important;
        }

        /* Code blocks & Pre tags */
        code {
            background-color: #141A30 !important;
            color: #38BDF8 !important;
            border: 1px solid #293352 !important;
            border-radius: 6px !important;
            padding: 2px 6px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.88em !important;
        }
        pre {
            background-color: #141A30 !important;
            border: 1px solid #293352 !important;
            border-radius: 12px !important;
            padding: 14px !important;
        }

        /* Source Citation Cards */
        .source-card {
            background: #1C2442;
            border: 1px solid #293352;
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 10px;
            transition: all 0.2s ease;
        }
        .source-card:hover {
            border-color: #38BDF8;
            background: #222B49;
            transform: translateY(-1px);
        }
        .badge-central {
            background: rgba(99, 102, 241, 0.2);
            color: #818CF8;
            border: 1px solid rgba(99, 102, 241, 0.4);
            padding: 2px 8px;
            border-radius: 8px;
            font-size: 0.72rem;
            font-weight: 700;
            margin-left: 8px;
            text-transform: uppercase;
        }
        .badge-state {
            background: rgba(56, 189, 248, 0.15);
            color: #38BDF8;
            border: 1px solid rgba(56, 189, 248, 0.4);
            padding: 2px 8px;
            border-radius: 8px;
            font-size: 0.72rem;
            font-weight: 700;
            margin-left: 8px;
            text-transform: uppercase;
        }
        .badge-score {
            background: rgba(34, 197, 94, 0.12);
            color: #22C55E;
            border: 1px solid rgba(34, 197, 94, 0.35);
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
        }

        /* Chat Input Styling */
        [data-testid="stChatInput"] {
            background-color: transparent !important;
        }
        [data-testid="stChatInput"] > div {
            background-color: #141A30 !important;
            border: 1px solid #293352 !important;
            border-radius: 16px !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35) !important;
        }
        [data-testid="stChatInput"] > div:focus-within {
            border-color: #38BDF8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25), 0 4px 20px rgba(0, 0, 0, 0.4) !important;
        }
        [data-testid="stChatInput"] textarea {
            color: #F1F5F9 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: #64748B !important;
        }
        [data-testid="stChatInput"] button {
            background: linear-gradient(135deg, #6366F1, #38BDF8) !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            transition: opacity 0.2s ease !important;
        }
        [data-testid="stChatInput"] button:hover {
            opacity: 0.9 !important;
        }

        /* Streamlit Expander */
        [data-testid="stExpander"] {
            background-color: #171D35 !important;
            border: 1px solid #293352 !important;
            border-radius: 14px !important;
        }
        [data-testid="stExpander"] details summary {
            color: #F1F5F9 !important;
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sources(sources):
    """Show source citations with futuristic cards, badges, and similarity scores."""
    if not sources:
        return
    with st.expander(f"📚 Verified Sources ({len(sources)} schemes identified)", expanded=False):
        for i, s in enumerate(sources, 1):
            level = s.get("level", "").lower()
            badge_html = (
                '<span class="badge-central">🏛️ Central</span>'
                if level == "central"
                else '<span class="badge-state">🗺️ State (MP)</span>'
            )
            region = s.get("region") or "All India"
            section = s.get("section", "details").capitalize()
            score = s.get("score", 0.0)

            st.markdown(
                f"""
                <div class="source-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-weight: 700; font-size: 0.98rem; color: #F1F5F9;">{i}. {s['name']} {badge_html}</span>
                        <span class="badge-score">Match: {score:.1%}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 4px;">
                        📍 <span style="color: #F1F5F9;">{region}</span> &nbsp;•&nbsp; 📄 Section: <code style="color: #38BDF8;">{section}</code>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_welcome():
    """Show Deep Indigo + Electric Blue futuristic welcome banner with clickable example prompts."""
    st.markdown(
        """
        <div class="welcome-card-saas">
            <div class="welcome-title">👋 Namaste & Welcome to SchemeSense!</div>
            <div class="welcome-desc">
                Your intelligent copilot for Indian welfare policies. Discover government schemes for 
                <b>students, farmers, women, and workers</b> in seconds with source citations. 
                Ask your question below or use the <b>🎤 Voice Input</b> in the sidebar.
            </div>
            <div class="prompt-section-label">⚡ Example Questions (Click to Ask)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    prompts = [
        ("🇬🇧", "Tell me about student scholarship schemes in Madhya Pradesh"),
        ("🇮🇳", "गरीब परिवार की बेटी की शादी के लिए कौन सी योजना है?"),
        ("🔀", "Ladli Behna yojana mein kitne paise milte hain aur eligibility kya hai?"),
    ]

    for emoji, text in prompts:
        if st.button(f"{emoji}  {text}", key=f"sample_prompt_{hash(text)}"):
            st.session_state["pending_query"] = text
            st.rerun()

