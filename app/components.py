import streamlit as st


def render_sources(sources):
    """Show source citations in an expandable section."""
    if not sources:
        return
    with st.expander(f"📚 Sources ({len(sources)} schemes found)", expanded=False):
        for i, s in enumerate(sources, 1):
            level_emoji = "🏛️" if s.get("level") == "central" else "🗺️"
            st.markdown(
                f"**{i}. {s['name']}** {level_emoji}\n\n"
                f"📍 {s.get('region', 'N/A')} · 📄 {s['section']} · "
                f"Score: `{s['score']:.3f}`"
            )
            if i < len(sources):
                st.divider()


def render_welcome():
    """Show welcome message with example queries."""
    st.markdown("""
    ### 👋 Namaste! SchemeSense mein aapka swagat hai.
    
    Aap Hindi, English ya Hinglish mein apna sawal pooch sakte hain. Kuch examples:
    
    - 🇬🇧 *"Which schemes help farmers in Madhya Pradesh?"*
    - 🇮🇳 *"विधवा पेंशन योजना के लिए कौन पात्र है?"*  
    - 🔀 *"MP mein students ko scholarship kaise milegi?"*
    
    Sidebar mein 🎤 voice input bhi use kar sakte hain!
    """)
