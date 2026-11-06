import streamlit as st


def apply_custom_css():
    """Apply modern colorful styling, custom gradients, cards, and badges."""
    st.markdown(
        """
        <style>
        /* Modern vibrant header & background accent */
        .main-header-container {
            background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%);
            padding: 24px 28px;
            border-radius: 16px;
            color: white !important;
            margin-bottom: 24px;
            box-shadow: 0 8px 24px rgba(78, 205, 196, 0.25);
        }
        .main-header-title {
            font-size: 2.3rem !important;
            font-weight: 800 !important;
            color: white !important;
            margin: 0 !important;
            letter-spacing: -0.5px;
        }
        .main-header-sub {
            font-size: 1.05rem !important;
            color: rgba(255, 255, 255, 0.95) !important;
            margin-top: 6px !important;
            font-weight: 500;
        }

        /* Pill badges for multilingual support */
        .lang-pill-container {
            display: flex;
            gap: 8px;
            margin-top: 12px;
            flex-wrap: wrap;
        }
        .lang-pill {
            background: rgba(255, 255, 255, 0.22);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.35);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.82rem;
            color: white;
            font-weight: 600;
        }

        /* Welcome card */
        .welcome-card {
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.05) 0%, rgba(78, 205, 196, 0.08) 100%);
            border: 1px solid rgba(78, 205, 196, 0.25);
            border-radius: 16px;
            padding: 22px 24px;
            margin-bottom: 24px;
            backdrop-filter: blur(10px);
        }
        .welcome-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #4ECDC4;
            margin-bottom: 10px;
        }
        .sample-chip {
            background: rgba(69, 183, 209, 0.12);
            border-left: 3px solid #45B7D1;
            padding: 8px 14px;
            border-radius: 8px;
            margin: 6px 0;
            font-size: 0.92rem;
        }

        /* Source citation cards */
        .source-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 12px 16px;
            margin-bottom: 10px;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .source-card:hover {
            border-color: #4ECDC4;
            transform: translateY(-2px);
        }
        .badge-central {
            background: #FF6B6B;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-left: 6px;
        }
        .badge-state {
            background: #4ECDC4;
            color: #1a1a1a;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-left: 6px;
        }
        .badge-score {
            background: rgba(69, 183, 209, 0.2);
            color: #45B7D1;
            border: 1px solid #45B7D1;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        /* Sidebar cool accent */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(78, 205, 196, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sources(sources):
    """Show source citations with colorful cards, badges, and similarity scores."""
    if not sources:
        return
    with st.expander(f"📚 Sources ({len(sources)} verified schemes found)", expanded=False):
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
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-weight: 700; font-size: 1rem;">{i}. {s['name']} {badge_html}</span>
                        <span class="badge-score">Match: {score:.1%}</span>
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.85; margin-top: 4px;">
                        📍 <b>Region:</b> {region} &nbsp;·&nbsp; 📄 <b>Section:</b> <code>{section}</code>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_welcome():
    """Show rich, colorful welcome banner with interactive sample queries."""
    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-title">👋 Namaste & Welcome to SchemeSense!</div>
            <div style="font-size: 0.95rem; margin-bottom: 12px; opacity: 0.9;">
                Discover government welfare schemes for <b>farmers, students, women, and workers</b> in seconds. 
                Type in the box below or click the <b>🎤 Voice Input</b> in the sidebar!
            </div>
            <div style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; margin-bottom: 6px;">
                💡 Try asking:
            </div>
            <div class="sample-chip">🇬🇧 <i>"Tell me about student scholarship schemes in Madhya Pradesh"</i></div>
            <div class="sample-chip">🇮🇳 <i>"गरीब परिवार की बेटी की शादी के लिए कौन सी योजना है?"</i></div>
            <div class="sample-chip">🔀 <i>"Ladli Behna yojana mein kitne paise milte hain aur eligibility kya hai?"</i></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

