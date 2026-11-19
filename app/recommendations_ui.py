"""
Recommendations Dashboard UI Module for Schemate AI.
Renders the premium dark-themed 'Your Recommended Government Schemes' page
with deterministic eligibility statuses, matching rationale, and deep-links to chatbot.
Uses native Streamlit containers and components for clean, robust rendering.
"""

from typing import Dict, Any, List
import streamlit as st

from app.translations import t, localize_scheme_data
from app.db import get_saved_scheme_ids, save_scheme, unsave_scheme
from eligibility.profile_service import get_profile, get_profile_summary
from eligibility.recommendation_service import get_recommendations_for_user


def render_recommendations_view(user: Dict[str, Any]):
    """Renders the recommendation dashboard."""
    user_id = user["id"]
    profile = get_profile(user_id) or {}
    lang = profile.get("preferred_language", "en")

    # Header
    st.markdown(f"## 🏛️ {t('rec_title', lang)}")
    st.caption(t("rec_subtitle", lang))

    # Top Controls Row: Profile Summary + Actions
    col_summary, col_refresh, col_edit = st.columns([0.64, 0.18, 0.18])

    with col_summary:
        summary_text = get_profile_summary(profile, lang=lang)
        st.info(f"👤 **Profile:** {summary_text}", icon="ℹ️")

    with col_refresh:
        if st.button(t("btn_refresh", lang), key="rec_btn_recalc", use_container_width=True):
            st.toast("Recalculating personalized scheme recommendations...", icon="🔄")
            st.rerun()

    with col_edit:
        if st.button(t("btn_edit_profile", lang), key="rec_btn_edit_prof", use_container_width=True):
            st.session_state.active_view = "profile"
            st.rerun()

    # Search and Filter Controls
    col_search, col_filter = st.columns([0.6, 0.4])

    with col_search:
        rec_search = st.text_input(
            "Search within recommended schemes",
            placeholder="🔍 Search by scheme name, benefits, or keyword...",
            label_visibility="collapsed",
            key="rec_search_query",
        )

    with col_filter:
        status_filter_options = [
            t("filter_all", lang),
            t("filter_eligible", lang),
            t("filter_verification", lang),
            t("filter_not_eligible", lang),
        ]
        chosen_filter_display = st.selectbox(
            "Filter by Eligibility Status",
            options=status_filter_options,
            index=0,
            label_visibility="collapsed",
            key="rec_status_filter_select",
        )

    # Map localized filter to engine keyword
    engine_filter = None
    if "eligible" in chosen_filter_display.lower() and "not" not in chosen_filter_display.lower() and "नहीं" not in chosen_filter_display:
        engine_filter = "Potentially Eligible"
    elif "verification" in chosen_filter_display.lower() or "सत्यापन" in chosen_filter_display:
        engine_filter = "Needs Verification"
    elif "not" in chosen_filter_display.lower() or "नहीं" in chosen_filter_display:
        engine_filter = "Not Eligible"

    # Fetch ranked recommendations deterministically
    recommendations = get_recommendations_for_user(
        user_id,
        top_n=50,
        filter_status=engine_filter,
        search_query=rec_search.strip() if rec_search else None,
    )

    # Stat counts
    total_count = len(recommendations)
    pot_count = sum(1 for r in recommendations if r["status"] == "Potentially Eligible")
    ver_count = sum(1 for r in recommendations if r["status"] == "Needs Verification")

    st.caption(
        f"Showing **{total_count}** schemes &bull; "
        f"✅ **{pot_count}** Potentially Eligible &bull; "
        f"⚠️ **{ver_count}** Verification Needed"
    )

    if not recommendations:
        st.info(t("empty_recommendations", lang))
        return

    # Fetch currently saved schemes for this user
    saved_scheme_ids = set(get_saved_scheme_ids(user_id))

    # Render Scheme Cards using native Streamlit containers
    for idx, raw_scheme in enumerate(recommendations):
        scheme = localize_scheme_data(raw_scheme, lang=lang)
        _render_scheme_card(scheme, idx, lang, user_id, saved_scheme_ids)

    # Legal Disclaimer at bottom
    st.info(t("disclaimer_text", lang), icon="⚠️")


def _render_scheme_card(scheme: Dict[str, Any], idx: int, lang: str, user_id: int, saved_scheme_ids: set):
    """Renders a single scheme card using clean native Streamlit bordered container."""
    status = scheme["status"]
    level = scheme.get("level", "central").lower()
    name = scheme["name"]
    region = scheme.get("region", "India")
    official_link = scheme.get("official_link") or "https://www.myscheme.gov.in"
    score = scheme.get("score", 0.0)

    with st.container(border=True):
        # Header Row: Title & Region on left, Central/State tag on right
        c_title, c_tag = st.columns([0.76, 0.24])
        with c_title:
            st.markdown(f"#### {name}")
            st.caption(f"📍 {region}")
        with c_tag:
            tag_label = t("tag_central", lang) if level == "central" else f"{t('tag_state', lang)}"
            st.caption(f"🏛️ **{tag_label}**")

        # Status Banner
        if status == "Potentially Eligible":
            st.success(f"✓ {t('badge_eligible', lang)} — {int(score)}% Match", icon="✅")
        elif status == "Needs Verification":
            st.warning(f"⚠ {t('badge_verification', lang)} — {int(score)}% Match", icon="⚠️")
        else:
            st.error(f"✕ {t('badge_not_eligible', lang)}", icon="❌")

        # Overview Description
        desc = scheme.get("description", "").strip()
        if desc:
            display_desc = desc[:240] + ("..." if len(desc) > 240 else "")
            st.markdown(display_desc)

        # Why This Scheme Matches You
        if scheme.get("match_reasons"):
            st.markdown(f"**:green[🎯 {t('why_matches_title', lang)}:]**")
            for r in scheme["match_reasons"][:4]:
                st.markdown(f"&bull; {r}")

        # Missing Information / Verification Required
        if scheme.get("missing_criteria") and status != "Not Eligible":
            st.markdown(f"**:orange[⚠️ {t('missing_info_title', lang)}:]**")
            for m in scheme["missing_criteria"][:3]:
                st.markdown(f"&bull; {m}")

        # Disqualification Reasons if Not Eligible
        if scheme.get("disqualification_reasons") and status == "Not Eligible":
            st.markdown("**:red[✕ Ineligibility Factors:]**")
            for d in scheme["disqualification_reasons"][:3]:
                st.markdown(f"&bull; {d}")

        # Key Benefits
        benefits_text = scheme.get("benefits", "").strip()
        if benefits_text:
            display_benefits = benefits_text[:240] + ("..." if len(benefits_text) > 240 else "")
            st.markdown(f"**🎁 {t('benefits_title', lang)}:** {display_benefits}")

        # Required Documents
        if scheme.get("required_documents"):
            docs_pills = "  •  ".join(f"`📄 {d}`" for d in scheme["required_documents"][:5])
            st.markdown(f"**📋 {t('documents_title', lang)}:** {docs_pills}")

        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

        # Action Buttons
        col_ask, col_link, col_save, col_expand = st.columns([0.34, 0.26, 0.22, 0.18])

        with col_ask:
            if st.button(
                t("btn_ask_schemate", lang),
                key=f"card_ask_btn_{idx}_{scheme['scheme_id']}",
                use_container_width=True,
            ):
                prompt_query = f"Can you explain the scheme '{name}' ({region}) and my eligibility for it?"
                st.session_state["pending_query"] = prompt_query
                st.session_state.active_view = "chat"
                st.rerun()

        with col_link:
            st.link_button(
                t("btn_official_link", lang),
                url=official_link,
                use_container_width=True,
            )

        with col_save:
            s_id = str(scheme["scheme_id"])
            is_saved = s_id in saved_scheme_ids
            if is_saved:
                if st.button(
                    t("saved_btn_saved", lang),
                    key=f"card_saved_{idx}_{s_id}",
                    type="secondary",
                    use_container_width=True,
                    help="Click to unsave"
                ):
                    unsave_scheme(user_id, s_id)
                    st.toast(t("saved_toast_removed", lang), icon="🗑️")
                    st.rerun()
            else:
                if st.button(
                    t("saved_btn_save", lang),
                    key=f"card_save_{idx}_{s_id}",
                    type="secondary",
                    use_container_width=True,
                    help="Save scheme to your dashboard"
                ):
                    save_scheme(user_id, s_id, status=status)
                    st.toast(t("saved_toast_saved", lang), icon="⭐")
                    st.rerun()

        with col_expand:
            with st.popover("ℹ️ Details", use_container_width=True):
                st.markdown(f"#### {name}")
                st.markdown(f"**Jurisdiction:** {region} ({level.title()})")
                st.markdown(f"**Official Sources:** {', '.join(scheme.get('official_sources', ['myScheme.gov.in']))}")
                st.markdown("---")
                st.markdown("**Overview:**")
                st.markdown(scheme.get("description", "No additional details provided."))
                st.markdown("**Key Benefits:**")
                st.markdown(scheme.get("benefits", "Subject to official rules."))
                st.markdown("**Required Documents:**")
                for d in scheme.get("required_documents", []):
                    st.markdown(f"- {d}")
                st.markdown(f"[Visit Official Portal]({official_link})")
