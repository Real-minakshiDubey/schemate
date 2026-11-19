"""
Onboarding UI Module for Schemate AI.
Provides a premium, step-based onboarding workflow with language selection,
personal information capture, conditional occupation forms, and validation.
Uses native Streamlit components for clean, robust rendering.
"""

from datetime import date
from typing import Dict, Any
import streamlit as st

from app.translations import t
from app.db import save_user_profile, get_user_profile, set_user_language
from eligibility.scheme_rules import STATES_AND_UTS


def render_onboarding_view(user: Dict[str, Any]):
    """Main entrypoint for rendering the onboarding experience."""
    user_id = user["id"]

    # Initialize current onboarding step in session state if not present
    if "onboarding_step" not in st.session_state:
        st.session_state.onboarding_step = 1

    # Load existing profile draft from DB or session state
    if "profile_draft" not in st.session_state:
        existing = get_user_profile(user_id)
        if existing:
            st.session_state.profile_draft = existing
        else:
            st.session_state.profile_draft = {
                "preferred_language": "en",
                "age": 22,
                "gender": "Male",
                "state": "Madhya Pradesh",
                "district": "",
                "occupation": "Student",
                "annual_family_income": 150000.0,
                "education_level": "Graduate / Bachelor's Degree",
                "social_category": "General / Unreserved",
                "disability_status": "None",
                "marital_status": "Single / Unmarried",
                "additional_attributes": {},
                "onboarding_completed": 0,
            }

    current_lang = st.session_state.profile_draft.get("preferred_language", "en")
    step = st.session_state.onboarding_step

    # Center-column container for clean onboarding presentation
    _, col_center, _ = st.columns([0.05, 0.9, 0.05])

    with col_center:
        # Step progress indicator using native Streamlit progress bar
        step_titles = {
            1: t("step_1", current_lang),
            2: t("step_2", current_lang),
            3: t("step_3", current_lang),
            4: t("step_4", current_lang),
        }
        progress_val = int((step / 4) * 100)

        st.progress(progress_val)
        st.caption(f"**{t('step_indicator', current_lang, current=step, total=4, title=step_titles.get(step, ''))}**")
        st.markdown("")

        if step == 1:
            _render_step_1_language(user_id, current_lang)
        elif step == 2:
            _render_step_2_basic_info(user_id, current_lang)
        elif step == 3:
            _render_step_3_occupation(user_id, current_lang)
        elif step == 4:
            _render_step_4_social_category(user_id, current_lang)


def _render_step_1_language(user_id: int, current_lang: str):
    """Step 1: Premium Language Selection Screen with clickable cards."""
    st.markdown(f"## 🌐 {t('choose_language_title', current_lang)}")
    st.caption(t("choose_language_subtitle", current_lang))
    st.markdown("")

    languages = [
        {
            "code": "en",
            "name": t("lang_en_name", current_lang),
            "desc": t("lang_en_desc", current_lang),
            "icon": "🇬🇧",
        },
        {
            "code": "hi",
            "name": t("lang_hi_name", current_lang),
            "desc": t("lang_hi_desc", current_lang),
            "icon": "🇮🇳",
        },
        {
            "code": "hinglish",
            "name": t("lang_hinglish_name", current_lang),
            "desc": t("lang_hinglish_desc", current_lang),
            "icon": "💬",
        },
    ]

    selected_lang = st.session_state.profile_draft.get("preferred_language", "en")

    for l_info in languages:
        is_selected = (l_info["code"] == selected_lang)
        with st.container(border=True):
            col_text, col_action = st.columns([0.76, 0.24])
            with col_text:
                status_icon = " ✅" if is_selected else ""
                st.markdown(f"#### {l_info['icon']}  {l_info['name']}{status_icon}")
                st.caption(l_info["desc"])
            with col_action:
                btn_label = "✓ Active" if is_selected else "Select"
                btn_type = "primary" if is_selected else "secondary"
                if st.button(btn_label, key=f"btn_lang_{l_info['code']}", use_container_width=True, type=btn_type):
                    st.session_state.profile_draft["preferred_language"] = l_info["code"]
                    # Save language preference immediately to user profile table
                    set_user_language(user_id, l_info["code"])
                    st.rerun()

    st.markdown("")

    # Next Step button
    if st.button(t("btn_next", selected_lang), key="lang_next_btn", use_container_width=True, type="primary"):
        st.session_state.onboarding_step = 2
        st.rerun()


def _render_step_2_basic_info(user_id: int, lang: str):
    """Step 2: Basic Demographics (Age/DOB, Gender, State, District)."""
    draft = st.session_state.profile_draft

    st.markdown(f"### 📍 {t('step_2', lang)}")
    st.caption("Provide your basic demographic details for accurate regional scheme matching.")

    with st.form("form_step_2"):
        c1, c2 = st.columns(2)
        with c1:
            age_val = st.number_input(
                t("age_label", lang),
                min_value=1,
                max_value=115,
                value=int(draft.get("age") or 22),
                step=1,
                help=t("age_help", lang),
            )
        with c2:
            gender_options = [
                t("gender_male", lang),
                t("gender_female", lang),
                t("gender_transgender", lang),
                t("gender_other", lang),
            ]
            current_gender = draft.get("gender", t("gender_male", lang))
            gender_idx = 0
            for i, opt in enumerate(gender_options):
                if current_gender.lower() in opt.lower():
                    gender_idx = i
                    break
            gender_val = st.selectbox(t("gender_label", lang), options=gender_options, index=gender_idx)

        c_state, c_dist = st.columns(2)
        with c_state:
            # Dropdown with all 28 States and 8 UTs
            state_options = sorted(STATES_AND_UTS)
            current_state = draft.get("state", "Madhya Pradesh")
            state_idx = state_options.index(current_state) if current_state in state_options else 0
            state_val = st.selectbox(t("state_label", lang), options=state_options, index=state_idx)
        with c_dist:
            dist_val = st.text_input(
                t("district_label", lang),
                value=draft.get("district", ""),
                placeholder=t("district_placeholder", lang),
            )

        st.markdown("")
        col_back, col_fwd = st.columns([1, 1])
        with col_back:
            btn_prev = st.form_submit_button(t("btn_back", lang), use_container_width=True)
        with col_fwd:
            btn_continue = st.form_submit_button(t("btn_next", lang), use_container_width=True, type="primary")

        if btn_prev:
            st.session_state.onboarding_step = 1
            st.rerun()

        if btn_continue:
            # Form validation
            if not age_val or age_val < 1 or age_val > 120:
                st.error(t("val_age_required", lang))
            elif not state_val:
                st.error(t("val_state_required", lang))
            else:
                draft["age"] = int(age_val)
                # Map localized gender string back to canonical value
                if "female" in gender_val.lower() or "महिला" in gender_val:
                    draft["gender"] = "Female"
                elif "trans" in gender_val.lower():
                    draft["gender"] = "Transgender"
                elif "prefer" in gender_val.lower() or "नहीं" in gender_val:
                    draft["gender"] = "Prefer not to say"
                else:
                    draft["gender"] = "Male"

                draft["state"] = state_val
                draft["district"] = dist_val.strip()
                st.session_state.profile_draft = draft
                st.session_state.onboarding_step = 3
                st.rerun()


def _render_step_3_occupation(user_id: int, lang: str):
    """Step 3: Occupation, Income, Education and Conditional Occupation Fields."""
    draft = st.session_state.profile_draft

    st.markdown(f"### 💼 {t('step_3', lang)}")
    st.caption("Schemes are heavily tailored to your current occupation and income category.")

    occ_choices = [
        ("Student", t("occ_student", lang)),
        ("Farmer / Agriculture", t("occ_farmer", lang)),
        ("Entrepreneur / MSME / Business Owner", t("occ_entrepreneur", lang)),
        ("Salaried Employee (Private / Govt)", t("occ_salaried", lang)),
        ("Self-Employed / Freelancer / Professional", t("occ_self_employed", lang)),
        ("Daily Wage Worker / Laborer / Artisan", t("occ_daily_wage", lang)),
        ("Unemployed / Job Seeker", t("occ_unemployed", lang)),
        ("Homemaker", t("occ_homemaker", lang)),
        ("Senior Citizen / Retired", t("occ_retired", lang)),
        ("Other", t("occ_other", lang)),
    ]

    # Map current draft occupation
    cur_occ_key = draft.get("occupation", "Student")
    occ_idx = 0
    for idx, (canonical_k, display_label) in enumerate(occ_choices):
        if canonical_k == cur_occ_key or canonical_k.split()[0].lower() in cur_occ_key.lower():
            occ_idx = idx
            break

    selected_occ_display = st.selectbox(
        t("occupation_label", lang),
        options=[pair[1] for pair in occ_choices],
        index=occ_idx,
        key="onboard_occ_select",
    )

    # Determine canonical occupation key
    chosen_canonical_occ = "Student"
    for canonical_k, display_label in occ_choices:
        if display_label == selected_occ_display:
            chosen_canonical_occ = canonical_k
            break

    # Conditional Questions based on Occupation
    add_attrs = draft.get("additional_attributes") or {}

    with st.expander("🔍 " + t("student_section" if "Student" in chosen_canonical_occ else ("farmer_section" if "Farmer" in chosen_canonical_occ else "entrepreneur_section"), lang), expanded=True):
        if "Student" in chosen_canonical_occ:
            st.markdown(f"##### {t('student_section', lang)}")
            c1, c2 = st.columns(2)
            
            student_lvl_choices = [
                ("Undergraduate (B.Tech, B.Sc, B.Com, MBBS)", t("student_level_ug", lang)),
                ("Postgraduate (M.Tech, M.Sc, MBA)", t("student_level_pg", lang)),
                ("School (Class 9-12)", t("student_level_school", lang)),
                ("Ph.D. / Research Fellowship", t("student_level_phd", lang)),
                ("Diploma / ITI", t("student_level_diploma", lang)),
            ]
            
            with c1:
                cur_lvl_disp = st.selectbox(
                    t("student_level_label", lang),
                    options=[label for _, label in student_lvl_choices],
                    index=0
                )
                cur_lvl = next((k for k, label in student_lvl_choices if label == cur_lvl_disp), "Undergraduate (B.Tech, B.Sc, B.Com, MBBS)")
            with c2:
                inst_type = st.selectbox(
                    t("student_inst_label", lang),
                    options=[t("inst_govt", lang), t("inst_aided", lang), t("inst_private", lang)],
                    index=0
                )
            course_val = st.text_input(
                t("student_course_label", lang),
                value=add_attrs.get("course", ""),
                placeholder=t("student_course_placeholder", lang)
            )
            add_attrs["student_level"] = cur_lvl
            add_attrs["institution_type"] = inst_type
            add_attrs["course"] = course_val.strip()

        elif "Farmer" in chosen_canonical_occ:
            st.markdown(f"##### {t('farmer_section', lang)}")
            c1, c2 = st.columns(2)
            with c1:
                land_own = st.selectbox(
                    t("farmer_ownership_label", lang),
                    options=[t("farmer_owner", lang), t("farmer_tenant", lang), t("farmer_laborer", lang)],
                    index=0
                )
            with c2:
                land_size = st.selectbox(
                    t("farmer_land_label", lang),
                    options=[t("land_marginal", lang), t("land_small", lang), t("land_medium_large", lang), t("land_none", lang)],
                    index=0
                )
            add_attrs["land_ownership"] = land_own
            add_attrs["landholding_size"] = land_size

        elif "Entrepreneur" in chosen_canonical_occ or "Business" in chosen_canonical_occ:
            st.markdown(f"##### {t('entrepreneur_section', lang)}")
            c1, c2 = st.columns(2)
            with c1:
                biz_type = st.selectbox(
                    t("business_type_label", lang),
                    options=[t("biz_manufacturing", lang), t("biz_services", lang), t("biz_trading", lang), t("biz_agri_allied", lang), t("biz_handicraft", lang)],
                    index=0
                )
            with c2:
                biz_stage = st.selectbox(
                    t("business_stage_label", lang),
                    options=[t("biz_ideation", lang), t("biz_early", lang), t("biz_established", lang)],
                    index=0
                )
            add_attrs["business_type"] = biz_type
            add_attrs["business_stage"] = biz_stage

    c_inc, c_edu = st.columns(2)
    with c_inc:
        cur_inc = float(draft.get("annual_family_income") or 180000.0)
        income_val = st.number_input(
            t("income_label", lang),
            min_value=0.0,
            max_value=10000000.0,
            value=cur_inc,
            step=10000.0,
            help=t("income_help", lang)
        )
    with c_edu:
        edu_options = [
            t("edu_graduate", lang),
            t("edu_12th", lang),
            t("edu_10th", lang),
            t("edu_diploma", lang),
            t("edu_post_graduate", lang),
            t("edu_doctorate", lang),
            t("edu_below_10th", lang),
        ]
        edu_val = st.selectbox(t("education_label", lang), options=edu_options, index=0)

    st.markdown("")
    col_back, col_fwd = st.columns([1, 1])
    with col_back:
        if st.button(t("btn_back", lang), key="btn_step3_back", use_container_width=True):
            st.session_state.onboarding_step = 2
            st.rerun()
    with col_fwd:
        if st.button(t("btn_next", lang), key="btn_step3_next", use_container_width=True, type="primary"):
            draft["occupation"] = chosen_canonical_occ
            draft["annual_family_income"] = float(income_val)
            draft["education_level"] = edu_val
            draft["additional_attributes"] = add_attrs
            st.session_state.profile_draft = draft
            st.session_state.onboarding_step = 4
            st.rerun()


def _render_step_4_social_category(user_id: int, lang: str):
    """Step 4: Social Category, Disability Status, Marital Status & Secure Completion."""
    draft = st.session_state.profile_draft

    st.markdown(f"### 🏛️ {t('step_4', lang)}")
    st.caption("Optional details to unlock reserved schemes, welfare subsidies, and fee waivers.")

    # Sensitive Information Notice Box with lock icon using native Streamlit callout
    st.info(t("sensitive_info_notice", lang), icon="🔒")

    with st.form("form_step_4"):
        col_cat, col_dis = st.columns(2)
        with col_cat:
            cat_options = [
                t("cat_general", lang),
                t("cat_obc", lang),
                t("cat_sc", lang),
                t("cat_st", lang),
                t("cat_ews", lang),
                t("cat_minority", lang),
            ]
            cat_val = st.selectbox(t("social_category_label", lang), options=cat_options, index=0)

        with col_dis:
            dis_options = [
                t("dis_none", lang),
                t("dis_locomotor", lang),
                t("dis_visual", lang),
                t("dis_hearing", lang),
                t("dis_intellectual", lang),
                t("dis_other", lang),
            ]
            dis_val = st.selectbox(t("disability_label", lang), options=dis_options, index=0)

        mar_options = [
            t("mar_single", lang),
            t("mar_married", lang),
            t("mar_widowed", lang),
            t("mar_divorced", lang),
        ]
        mar_val = st.selectbox(t("marital_label", lang), options=mar_options, index=0)

        st.markdown("")
        col_back, col_submit = st.columns([0.4, 0.6])
        with col_back:
            btn_prev = st.form_submit_button(t("btn_back", lang), use_container_width=True)
        with col_submit:
            btn_complete = st.form_submit_button(t("btn_complete", lang), use_container_width=True, type="primary")

        if btn_prev:
            st.session_state.onboarding_step = 3
            st.rerun()

        if btn_complete:
            # Map social category to canonical string
            canonical_cat = "General / Unreserved"
            for code in ["OBC", "SC", "ST", "EWS", "Minority"]:
                if code.lower() in cat_val.lower():
                    canonical_cat = code
                    break

            draft["social_category"] = canonical_cat
            draft["disability_status"] = "None" if "none" in dis_val.lower() or "कोई नहीं" in dis_val else dis_val
            draft["marital_status"] = mar_val
            draft["onboarding_completed"] = 1

            # Save full profile to database
            success = save_user_profile(user_id, draft)
            if success:
                st.session_state.user_profile = draft
                st.session_state.active_view = "recommendations"
                st.session_state.onboarding_completed = True
                st.success(t("profile_saved_success", lang))
                st.rerun()
            else:
                st.error("Failed to save profile. Please try again.")
