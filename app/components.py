import streamlit as st


def apply_custom_css():
    """Apply ultra-premium Deep Indigo + Electric Blue futuristic AI SaaS styling."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* Strict Design System Palette */
        :root {
            --bg-main: #0A0F1F;
            --bg-sidebar: #0D1326;
            --surface-primary: #111A30;
            --surface-secondary: #17213A;
            --surface-elevated: #1C2745;
            --accent-primary: #6366F1;
            --electric-blue: #38BDF8;
            --gradient-accent: linear-gradient(135deg, #6366F1 0%, #38BDF8 100%);
            --text-primary: #F1F5F9;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            --border-glass: rgba(148, 163, 184, 0.14);
            --surface-glass: rgba(255, 255, 255, 0.035);
            --input-bg: #141A30;
            --hover-bg: #222B49;
            --success: #22C55E;
            --warning: #F59E0B;
            --error: #EF4444;
        }

        /* Global Application Canvas */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0A0F1F !important;
            color: #F1F5F9 !important;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            -webkit-font-smoothing: antialiased;
        }

        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Sleek Modern Scrollbar */
        ::-webkit-scrollbar {
            width: 5px;
            height: 5px;
        }
        ::-webkit-scrollbar-track {
            background: #0A0F1F;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(148, 163, 184, 0.2);
            border-radius: 9999px;
            transition: background 0.2s ease;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #6366F1;
        }

        /* Premium Sidebar Panel */
        [data-testid="stSidebar"] {
            background-color: #0D1326 !important;
            border-right: 1px solid rgba(148, 163, 184, 0.14) !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.35);
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(148, 163, 184, 0.14) !important;
            margin: 1.1rem 0 !important;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #F1F5F9 !important;
            font-size: 0.88rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.04em !important;
            text-transform: uppercase !important;
            margin-bottom: 0.6rem !important;
        }
        [data-testid="stSidebar"] .stCaption {
            color: #94A3B8 !important;
            font-size: 0.8rem !important;
        }

        /* Sidebar Branding Card */
        .sidebar-brand-box {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 14px;
            background: rgba(255, 255, 255, 0.035);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 14px;
            margin-bottom: 20px;
            transition: border-color 0.2s ease, transform 0.2s ease;
        }
        .sidebar-brand-box:hover {
            border-color: rgba(56, 189, 248, 0.4);
            transform: translateY(-1px);
        }
        .sidebar-brand-icon {
            font-size: 1.4rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(56, 189, 248, 0.15));
            border: 1px solid rgba(99, 102, 241, 0.45);
            border-radius: 10px;
        }
        .sidebar-brand-text {
            font-size: 1.1rem;
            font-weight: 800;
            color: #F1F5F9;
            letter-spacing: -0.02em;
        }
        .sidebar-brand-tag {
            font-size: 0.68rem;
            color: #38BDF8;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        /* Sidebar Radio Pill Controls */
        div[data-testid="stRadio"] > div {
            background-color: #111A30;
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 12px;
            padding: 5px;
            gap: 4px;
        }
        div[data-testid="stRadio"] label {
            color: #94A3B8 !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            padding: 6px 12px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stRadio"] label:hover {
            color: #F1F5F9 !important;
            background-color: #17213A !important;
        }

        /* Selectbox styling */
        div[data-baseweb="select"] > div {
            background-color: #111A30 !important;
            border: 1px solid rgba(148, 163, 184, 0.14) !important;
            border-radius: 12px !important;
            color: #F1F5F9 !important;
            transition: border-color 0.2s ease !important;
        }
        div[data-baseweb="select"] > div:hover, div[data-baseweb="select"] > div:focus-within {
            border-color: #38BDF8 !important;
            box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.3) !important;
        }

        /* Hero Header (Glassmorphism & Animated Glow) */
        .hero-container {
            background: rgba(17, 26, 48, 0.75);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 20px;
            padding: 28px 32px;
            margin-bottom: 24px;
            box-shadow: 0 14px 40px -10px rgba(10, 15, 31, 0.9), 0 0 1px 1px rgba(99, 102, 241, 0.15);
            position: relative;
            overflow: hidden;
            transition: transform 0.25s ease, border-color 0.25s ease;
        }
        .hero-container:hover {
            border-color: rgba(56, 189, 248, 0.3);
        }
        .hero-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #6366F1 0%, #38BDF8 50%, rgba(99, 102, 241, 0) 100%);
            animation: glowSweep 6s infinite linear;
        }
        @keyframes glowSweep {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
        .hero-title-row {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 6px;
        }
        .hero-icon {
            font-size: 2.2rem;
            filter: drop-shadow(0 2px 10px rgba(56, 189, 248, 0.35));
        }
        .hero-title {
            font-size: 2.3rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em !important;
            background: linear-gradient(135deg, #F1F5F9 25%, #38BDF8 100%);
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin: 0 !important;
            line-height: 1.15 !important;
        }
        .hero-sub {
            font-size: 0.98rem !important;
            color: #94A3B8 !important;
            margin-bottom: 16px !important;
            font-weight: 500 !important;
        }

        /* Glassmorphic Feature Badges */
        .feature-badge-row {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .feature-badge {
            background: rgba(255, 255, 255, 0.035);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(148, 163, 184, 0.14);
            color: #F1F5F9;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 9999px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .feature-badge:hover {
            border-color: #38BDF8;
            color: #38BDF8;
            background: rgba(56, 189, 248, 0.08);
            transform: translateY(-1px);
        }

        /* Welcome Section Card */
        .welcome-card-saas {
            background: #111A30;
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 18px;
            padding: 24px 28px;
            margin-bottom: 24px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
            position: relative;
        }
        .welcome-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #38BDF8;
            margin-bottom: 8px;
            letter-spacing: -0.01em;
        }
        .welcome-desc {
            font-size: 0.94rem;
            color: #94A3B8;
            line-height: 1.55;
            margin-bottom: 18px;
        }
        .prompt-section-label {
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #6366F1;
            margin-bottom: 10px;
        }

        /* Clickable Example Prompts */
        div.stButton > button {
            background: #17213A !important;
            border: 1px solid rgba(148, 163, 184, 0.14) !important;
            border-left: 3px solid #38BDF8 !important;
            color: #F1F5F9 !important;
            border-radius: 12px !important;
            padding: 12px 18px !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            text-align: left !important;
            width: 100% !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
        }
        div.stButton > button:hover {
            background: #1C2745 !important;
            border-color: #38BDF8 !important;
            color: #38BDF8 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 18px rgba(56, 189, 248, 0.15) !important;
        }

        /* Chat Message Surface Containers */
        [data-testid="stChatMessage"] {
            border-radius: 18px !important;
            padding: 18px 22px !important;
            margin-bottom: 14px !important;
            border: 1px solid rgba(148, 163, 184, 0.14) !important;
            font-size: 0.96rem !important;
            line-height: 1.65 !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
            transition: border-color 0.2s ease;
        }
        /* User message: subtle indigo surface */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
        div[data-testid="stChatMessage"][aria-label="Chat message from user"] {
            background-color: #17213A !important;
            border-color: rgba(99, 102, 241, 0.35) !important;
        }
        /* Assistant message: dark elevated surface */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]),
        div[data-testid="stChatMessage"][aria-label="Chat message from assistant"] {
            background-color: #111A30 !important;
            border-color: rgba(148, 163, 184, 0.14) !important;
        }

        /* Modern Code Blocks */
        code {
            background-color: #141A30 !important;
            color: #38BDF8 !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
            border-radius: 6px !important;
            padding: 2px 7px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.88em !important;
        }
        pre {
            background-color: #141A30 !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
            border-radius: 14px !important;
            padding: 16px !important;
        }

        /* Source Citation Cards */
        .source-card {
            background: #17213A;
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 14px;
            padding: 14px 18px;
            margin-bottom: 10px;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .source-card:hover {
            border-color: #38BDF8;
            background: #1C2745;
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        .badge-central {
            background: rgba(99, 102, 241, 0.18);
            color: #818CF8;
            border: 1px solid rgba(99, 102, 241, 0.45);
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
            border: 1px solid rgba(56, 189, 248, 0.45);
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

        /* Chat Input: Glass-like Composer */
        [data-testid="stChatInput"] {
            background-color: transparent !important;
        }
        [data-testid="stChatInput"] > div {
            background-color: rgba(20, 26, 48, 0.85) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
            border-radius: 18px !important;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4) !important;
        }
        [data-testid="stChatInput"] > div:focus-within {
            border-color: #38BDF8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.3), 0 8px 32px rgba(0, 0, 0, 0.5) !important;
        }
        [data-testid="stChatInput"] textarea {
            color: #F1F5F9 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.95rem !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: #64748B !important;
        }
        [data-testid="stChatInput"] button {
            background: linear-gradient(135deg, #6366F1 0%, #38BDF8 100%) !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 10px rgba(99, 102, 241, 0.35) !important;
        }
        [data-testid="stChatInput"] button:hover {
            opacity: 0.92 !important;
            transform: scale(1.04) !important;
            box-shadow: 0 4px 14px rgba(56, 189, 248, 0.45) !important;
        }

        /* Expander Surface */
        [data-testid="stExpander"] {
            background-color: #111A30 !important;
            border: 1px solid rgba(148, 163, 184, 0.14) !important;
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
            st.session_state["pending_query"] = text
            st.rerun()


