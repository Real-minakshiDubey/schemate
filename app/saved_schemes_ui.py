"""
Saved Schemes Dashboard for Schemate AI.
Provides saved scheme tracking, deterministic stats, search & filtering,
document collection checklist, editable personal notes, details popover,
and seamless chat integration.
Uses native Streamlit components and containers for clean, bug-free rendering.
"""

from typing import Dict, Any, List
import json
import streamlit as st

from app.db import (
    get_user_profile,
    get_user_saved_schemes,
    save_scheme,
    unsave_scheme,
    update_saved_scheme_notes,
    update_saved_scheme_checklist,
)
from app.translations import t
from eligibility.scheme_rules import get_scheme_full_details, get_scheme_rule_by_id


def render_saved_schemes_view(user: Dict[str, Any]):
    """
    Renders the 'My Saved Schemes' view for an authenticated user.
    """
    user_id = user["id"]
    profile = get_user_profile(user_id) or {}
    lang = profile.get("preferred_language", "en")

    # Header section
    st.markdown(f"## ⭐ {t('saved_title', lang)}")
    st.caption(t("saved_subtitle", lang))
    st.markdown("---")

    # Fetch saved schemes from SQLite
    saved_records = get_user_saved_schemes(user_id)

    # Empty State check
    if not saved_records:
        with st.container(border=True):
            st.markdown(f"### 📭 {t('saved_empty_title', lang)}")
            st.info(t("saved_empty_subtitle", lang), icon="💡")
            if st.button(t("saved_btn_explore", lang), type="primary", key="saved_explore_btn"):
                st.session_state.active_view = "recommendations"
                st.rerun()
        return

    # Augment saved schemes with full scheme information from schemes_sections
    enriched_schemes = []
    for item in saved_records:
        s_id = str(item["scheme_id"])
        full_info = get_scheme_full_details(s_id)
        rule = get_scheme_rule_by_id(s_id)

        # Merge database status and notes
        scheme_obj = {
            "id": item["id"],
            "scheme_id": s_id,
            "saved_at": item["saved_at"],
            "status": item.get("status") or (rule.level if rule else "Potentially Eligible"),
            "notes": item.get("notes") or "",
            "checklist": item.get("checklist_json") or {},
            "name": full_info.get("name") or (rule.scheme_name if rule else f"Scheme #{s_id}"),
            "description": full_info.get("description") or (rule.description if rule else ""),
            "level": full_info.get("level") or (rule.level if rule else "central"),
            "region": full_info.get("state") or (rule.region if rule else "India"),
            "category": full_info.get("category", "General Welfare"),
            "benefits": full_info.get("benefits", ""),
            "eligibility": full_info.get("eligibility", ""),
            "application": full_info.get("application", ""),
            "documents": full_info.get("documents", []),
            "official_sources": full_info.get("sources", ["myScheme.gov.in"]),
            "official_link": full_info.get("link") or "https://www.myscheme.gov.in",
        }

        # Normalize status if stored as level or other
        if scheme_obj["status"] not in ["Potentially Eligible", "Needs Verification", "Not Eligible"]:
            scheme_obj["status"] = "Potentially Eligible"

        enriched_schemes.append(scheme_obj)

    # ---------------------------------------------------------------------------
    # Summary Statistics Cards
    # ---------------------------------------------------------------------------
    total_saved = len(enriched_schemes)
    total_eligible = sum(1 for s in enriched_schemes if s["status"] == "Potentially Eligible")
    total_verify = sum(1 for s in enriched_schemes if s["status"] == "Needs Verification")

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        with st.container(border=True):
            st.metric(label=t("saved_stat_total", lang), value=total_saved)
    with stat_col2:
        with st.container(border=True):
            st.metric(label=t("saved_stat_eligible", lang), value=total_eligible)
    with stat_col3:
        with st.container(border=True):
            st.metric(label=t("saved_stat_verify", lang), value=total_verify)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------------
    # Search and Filter Toolbar
    # ---------------------------------------------------------------------------
    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([0.32, 0.17, 0.17, 0.17, 0.17])

    with f_col1:
        search_query = st.text_input(
            "Search",
            placeholder=t("saved_search_placeholder", lang),
            label_visibility="collapsed",
            key="saved_search_input"
        ).strip().lower()

    with f_col2:
        type_filter = st.selectbox(
            "Jurisdiction",
            options=[t("saved_filter_all_types", lang), t("saved_filter_central", lang), t("saved_filter_state", lang)],
            label_visibility="collapsed",
            key="saved_type_filter"
        )

    with f_col3:
        categories = sorted(list({s["category"] for s in enriched_schemes if s.get("category")}))
        cat_options = [t("saved_filter_all_cats", lang)] + categories
        category_filter = st.selectbox(
            "Category",
            options=cat_options,
            label_visibility="collapsed",
            key="saved_category_filter"
        )

    with f_col4:
        status_options = [
            t("filter_all", lang),
            t("filter_eligible", lang),
            t("filter_verification", lang)
        ]
        status_filter = st.selectbox(
            "Status",
            options=status_options,
            label_visibility="collapsed",
            key="saved_status_filter"
        )

    with f_col5:
        sort_options = [t("saved_sort_recent", lang), t("saved_sort_az", lang)]
        sort_choice = st.selectbox(
            "Sort",
            options=sort_options,
            label_visibility="collapsed",
            key="saved_sort_choice"
        )

    # Apply Filters
    filtered = enriched_schemes

    if search_query:
        filtered = [
            s for s in filtered
            if search_query in s["name"].lower()
            or search_query in s["description"].lower()
            or search_query in s["category"].lower()
            or search_query in s["region"].lower()
        ]

    if type_filter == t("saved_filter_central", lang):
        filtered = [s for s in filtered if s["level"].lower() == "central"]
    elif type_filter == t("saved_filter_state", lang):
        filtered = [s for s in filtered if s["level"].lower() != "central"]

    if category_filter != t("saved_filter_all_cats", lang):
        filtered = [s for s in filtered if s["category"] == category_filter]

    if status_filter == t("filter_eligible", lang):
        filtered = [s for s in filtered if s["status"] == "Potentially Eligible"]
    elif status_filter == t("filter_verification", lang):
        filtered = [s for s in filtered if s["status"] == "Needs Verification"]

    # Sorting
    if sort_choice == t("saved_sort_az", lang):
        filtered = sorted(filtered, key=lambda x: x["name"].lower())
    else:
        # Recently saved (default descending by saved_at)
        filtered = sorted(filtered, key=lambda x: x.get("saved_at", ""), reverse=True)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    if not filtered:
        st.info("No saved schemes match your current search or filter criteria.", icon="🔍")
        return

    # ---------------------------------------------------------------------------
    # Render Saved Scheme Cards
    # ---------------------------------------------------------------------------
    for idx, scheme in enumerate(filtered):
        _render_saved_card(scheme, idx, user_id, lang)


def _render_saved_card(scheme: Dict[str, Any], idx: int, user_id: int, lang: str):
    """Renders a single saved scheme card with full actions, notes, and checklist."""
    s_id = scheme["scheme_id"]
    name = scheme["name"]
    level = scheme.get("level", "central").lower()
    region = scheme.get("region", "India")
    status = scheme.get("status", "Potentially Eligible")
    category = scheme.get("category", "General Welfare")
    saved_at = scheme.get("saved_at", "")[:10]  # YYYY-MM-DD
    official_link = scheme.get("official_link") or "https://www.myscheme.gov.in"

    with st.container(border=True):
        # Header Row
        c_title, c_meta = st.columns([0.72, 0.28])
        with c_title:
            st.markdown(f"#### {name}")
            st.caption(f"📍 {region} &nbsp;|&nbsp; 🏷️ {category}")
        with c_meta:
            tag_label = t("tag_central", lang) if level == "central" else t("tag_state", lang)
            st.markdown(f"**{tag_label}**")
            if saved_at:
                st.caption(f"📅 Saved on {saved_at}")

        # Status badge
        if status == "Potentially Eligible":
            st.success(f"✓ {t('badge_eligible', lang)}", icon="✅")
        elif status == "Needs Verification":
            st.warning(f"⚠ {t('badge_verification', lang)}", icon="⚠️")
        else:
            st.error(f"✕ {t('badge_not_eligible', lang)}", icon="❌")

        # Description
        desc = scheme.get("description", "").strip()
        if desc:
            display_desc = desc[:220] + ("..." if len(desc) > 220 else "")
            st.markdown(display_desc)

        # Primary Action Bar
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([0.34, 0.22, 0.22, 0.22])

        with btn_col1:
            if st.button(
                t("btn_ask_schemate", lang),
                key=f"saved_ask_{s_id}_{idx}",
                use_container_width=True
            ):
                prompt_query = f"Can you explain the scheme '{name}' ({region}) and my eligibility criteria for it?"
                st.session_state["pending_query"] = prompt_query
                st.session_state.active_view = "chat"
                st.rerun()

        with btn_col2:
            st.link_button(
                t("btn_official_link", lang),
                url=official_link,
                use_container_width=True
            )

        with btn_col3:
            with st.popover(f"ℹ️ {t('btn_view_details', lang)}", use_container_width=True):
                st.markdown(f"### {name}")
                st.markdown(f"**Jurisdiction:** {region} ({level.title()})")
                st.markdown(f"**Category:** {category}")
                st.markdown(f"**Official Sources:** {', '.join(scheme.get('official_sources', ['myScheme.gov.in']))}")
                st.markdown("---")
                st.markdown("#### Overview")
                st.markdown(scheme.get("description") or "No description provided.")
                st.markdown("#### Key Benefits")
                st.markdown(scheme.get("benefits") or "Subject to official rules.")
                st.markdown("#### Eligibility Criteria")
                st.markdown(scheme.get("eligibility") or "Subject to guidelines.")
                st.markdown("#### Application Process")
                st.markdown(scheme.get("application") or "Apply online on the official portal.")
                st.markdown("#### Required Documents")
                for doc in scheme.get("documents", []):
                    st.markdown(f"- {doc}")
                st.markdown(f"[Visit Official Application Portal]({official_link})")

        with btn_col4:
            if st.button(
                f"🗑️ {t('saved_btn_remove', lang)}",
                key=f"saved_remove_{s_id}_{idx}",
                type="secondary",
                use_container_width=True
            ):
                unsave_scheme(user_id, s_id)
                st.toast(t("saved_toast_removed", lang), icon="🗑️")
                st.rerun()

        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

        # -----------------------------------------------------------------------
        # Expandable: Document Checklist & Personal Notes
        # -----------------------------------------------------------------------
        with st.expander("📝 Document Checklist & Personal Notes", expanded=False):
            sub_col1, sub_col2 = st.columns([0.55, 0.45])

            with sub_col1:
                st.markdown(f"**{t('saved_checklist_title', lang)}**")
                raw_docs = scheme.get("documents", [])
                if not raw_docs:
                    st.caption(t("saved_checklist_empty", lang))
                else:
                    checklist_state = scheme.get("checklist") or {}
                    updated_checklist = {}
                    changed = False

                    # Checklist items
                    total_docs = len(raw_docs)
                    completed_count = 0

                    for doc_idx, doc_text in enumerate(raw_docs[:8]):
                        cleaned_text = doc_text.strip()
                        doc_key = f"doc_{s_id}_{doc_idx}"
                        is_checked = checklist_state.get(cleaned_text, False)
                        
                        box_val = st.checkbox(
                            cleaned_text,
                            value=is_checked,
                            key=f"chk_{s_id}_{doc_idx}_{idx}"
                        )
                        updated_checklist[cleaned_text] = box_val
                        if box_val:
                            completed_count += 1
                        if box_val != is_checked:
                            changed = True

                    # Progress bar
                    if total_docs > 0:
                        prog_pct = completed_count / min(total_docs, 8)
                        st.progress(prog_pct, text=f"Progress: {completed_count}/{min(total_docs, 8)} collected")

                    if changed:
                        update_saved_scheme_checklist(user_id, s_id, updated_checklist)
                        st.rerun()

            with sub_col2:
                st.markdown(f"**{t('saved_notes_title', lang)}**")
                current_notes = scheme.get("notes", "")
                notes_key = f"notes_input_{s_id}_{idx}"
                new_notes = st.text_area(
                    "Notes",
                    value=current_notes,
                    placeholder=t("saved_notes_placeholder", lang),
                    height=110,
                    label_visibility="collapsed",
                    key=notes_key
                )
                if st.button(t("saved_notes_save", lang), key=f"save_notes_btn_{s_id}_{idx}"):
                    update_saved_scheme_notes(user_id, s_id, new_notes)
                    st.toast(t("saved_notes_saved_toast", lang), icon="💾")
                    st.rerun()
