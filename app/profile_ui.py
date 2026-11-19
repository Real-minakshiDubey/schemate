"""
Profile Management and Editing UI for Schemate AI.
Allows users to update their profile information and recalculate
scheme recommendations anytime.
"""

from typing import Dict, Any
import streamlit as st

from app.translations import t
from app.db import save_user_profile, get_user_profile, set_user_language
from eligibility.scheme_rules import STATES_AND_UTS


def render_profile_view(user: Dict[str, Any]):
    """Renders the comprehensive profile editing interface."""
    user_id = user["id"]
    profile = get_user_profile(user_id) or {}
    lang = profile.get("preferred_language", "en")

    st.markdown(f"## 👤 {t('nav_profile', lang)}")
    st.caption("Keep your details updated so Schemate AI accurately matches you with new government schemes.")
    st.markdown("")

    with st.form("form_edit_profile"):
        # 1. Language Preference
        st.markdown(f"#### 🌐 {t('step_1', lang)}")
        lang_map = {
            t("lang_en_name", lang): "en",
            t("lang_hi_name", lang): "hi",
            t("lang_hinglish_name", lang): "hinglish",
        }
        lang_keys = list(lang_map.keys())
        cur_lang_idx = 0
        for i, (k, v) in enumerate(lang_map.items()):
            if v == lang:
                cur_lang_idx = i
                break

        chosen_lang_display = st.selectbox(
            t("choose_language_title", lang),
            options=lang_keys,
            index=cur_lang_idx,
        )
        new_lang = lang_map[chosen_lang_display]

        st.markdown("---")

        # 2. Basic Information
        st.markdown(f"#### 📍 {t('step_2', lang)}")
        c_age, c_gen = st.columns(2)
        with c_age:
            age_val = st.number_input(
                t("age_label", lang),
                min_value=1,
                max_value=115,
                value=int(profile.get("age") or 22),
                step=1,
            )
        with c_gen:
            gender_options = ["Male", "Female", "Transgender", "Prefer not to say"]
            cur_gender = profile.get("gender", "Male")
            g_idx = gender_options.index(cur_gender) if cur_gender in gender_options else 0
            gender_val = st.selectbox(t("gender_label", lang), options=gender_options, index=g_idx)

        c_state, c_dist = st.columns(2)
        with c_state:
            state_options = sorted(STATES_AND_UTS)
            cur_state = profile.get("state", "Madhya Pradesh")
            s_idx = state_options.index(cur_state) if cur_state in state_options else 0
            state_val = st.selectbox(t("state_label", lang), options=state_options, index=s_idx)
        with c_dist:
            dist_val = st.text_input(
                t("district_label", lang),
                value=profile.get("district", ""),
                placeholder=t("district_placeholder", lang),
            )

        st.markdown("---")

        # 3. Occupation & Economics
        st.markdown(f"#### 💼 {t('step_3', lang)}")
        occ_options = [
            "Student",
            "Farmer / Agriculture",
            "Entrepreneur / MSME / Business Owner",
            "Salaried Employee (Private / Govt)",
            "Self-Employed / Freelancer / Professional",
            "Daily Wage Worker / Laborer / Artisan",
            "Unemployed / Job Seeker",
            "Homemaker",
            "Senior Citizen / Retired",
            "Other",
        ]
        cur_occ = profile.get("occupation", "Student")
        occ_idx = 0
        for i, opt in enumerate(occ_options):
            if opt.lower().startswith(cur_occ.lower()[:5]):
                occ_idx = i
                break

        occ_val = st.selectbox(t("occupation_label", lang), options=occ_options, index=occ_idx)

        # Conditional fields
        add_attrs = profile.get("additional_attributes") or {}

        if "Student" in occ_val:
            st.markdown(f"##### {t('student_section', lang)}")
            c1, c2 = st.columns(2)
            with c1:
                cur_lvl = st.selectbox(
                    t("student_level_label", lang),
                    options=["Undergraduate", "Postgraduate", "School (9-12)", "Doctorate / Ph.D.", "Diploma"],
                    index=0,
                )
            with c2:
                inst_type = st.selectbox(
                    t("student_inst_label", lang),
                    options=[t("inst_govt", lang), t("inst_aided", lang), t("inst_private", lang)],
                    index=0,
                )
            course_val = st.text_input(
                t("student_course_label", lang),
                value=add_attrs.get("course", "B.Tech"),
            )
            add_attrs["student_level"] = cur_lvl
            add_attrs["institution_type"] = inst_type
            add_attrs["course"] = course_val.strip()

        elif "Farmer" in occ_val:
            st.markdown(f"##### {t('farmer_section', lang)}")
            c1, c2 = st.columns(2)
            with c1:
                land_own = st.selectbox(
                    t("farmer_ownership_label", lang),
                    options=[t("farmer_owner", lang), t("farmer_tenant", lang), t("farmer_laborer", lang)],
                    index=0,
                )
            with c2:
                land_size = st.selectbox(
                    t("farmer_land_label", lang),
                    options=[t("land_marginal", lang), t("land_small", lang), t("land_medium_large", lang), t("land_none", lang)],
                    index=0,
                )
            add_attrs["land_ownership"] = land_own
            add_attrs["landholding_size"] = land_size

        elif "Entrepreneur" in occ_val:
            st.markdown(f"##### {t('entrepreneur_section', lang)}")
            c1, c2 = st.columns(2)
            with c1:
                biz_type = st.selectbox(
                    t("business_type_label", lang),
                    options=[t("biz_manufacturing", lang), t("biz_services", lang), t("biz_trading", lang), t("biz_agri_allied", lang), t("biz_handicraft", lang)],
                    index=0,
                )
            with c2:
                biz_stage = st.selectbox(
                    t("business_stage_label", lang),
                    options=[t("biz_ideation", lang), t("biz_early", lang), t("biz_established", lang)],
                    index=0,
                )
            add_attrs["business_type"] = biz_type
            add_attrs["business_stage"] = biz_stage

        c_inc, c_edu = st.columns(2)
        with c_inc:
            cur_inc = float(profile.get("annual_family_income") or 180000.0)
            inc_val = st.number_input(
                t("income_label", lang),
                min_value=0.0,
                max_value=10000000.0,
                value=cur_inc,
                step=10000.0,
            )
        with c_edu:
            edu_options = [
                "Graduate / Bachelor's Degree",
                "12th Standard Pass",
                "10th Standard Pass",
                "Diploma / ITI",
                "Post Graduate / Master's Degree",
                "Doctorate / Ph.D.",
                "Below 10th Standard",
            ]
            cur_edu = profile.get("education_level", edu_options[0])
            e_idx = edu_options.index(cur_edu) if cur_edu in edu_options else 0
            edu_val = st.selectbox(t("education_label", lang), options=edu_options, index=e_idx)

        st.markdown("---")

        # 4. Social & Special Category
        st.markdown(f"#### 🏛️ {t('step_4', lang)}")
        c_cat, c_dis = st.columns(2)
        with c_cat:
            cat_options = ["General / Unreserved", "OBC", "SC", "ST", "EWS", "Minority"]
            cur_cat = profile.get("social_category", "General / Unreserved")
            cat_idx = cat_options.index(cur_cat) if cur_cat in cat_options else 0
            cat_val = st.selectbox(t("social_category_label", lang), options=cat_options, index=cat_idx)

        with c_dis:
            dis_options = ["None", "Locomotor / Physical (≥ 40%)", "Visual Impairment", "Hearing Impairment", "Intellectual", "Other"]
            cur_dis = profile.get("disability_status", "None")
            dis_idx = dis_options.index(cur_dis) if cur_dis in dis_options else 0
            dis_val = st.selectbox(t("disability_label", lang), options=dis_options, index=dis_idx)

        mar_options = ["Single / Unmarried", "Married", "Widowed", "Divorced / Separated"]
        cur_mar = profile.get("marital_status", "Single / Unmarried")
        mar_idx = mar_options.index(cur_mar) if cur_mar in mar_options else 0
        mar_val = st.selectbox(t("marital_label", lang), options=mar_options, index=mar_idx)

        st.markdown("")
        col_cancel, col_save = st.columns([0.4, 0.6])

        with col_cancel:
            btn_cancel = st.form_submit_button(t("btn_cancel", lang), use_container_width=True)

        with col_save:
            btn_save = st.form_submit_button(t("btn_update", lang), use_container_width=True)

        if btn_cancel:
            st.session_state.active_view = "recommendations"
            st.rerun()

        if btn_save:
            updated_data = {
                "preferred_language": new_lang,
                "age": int(age_val),
                "gender": gender_val,
                "state": state_val,
                "district": dist_val.strip(),
                "occupation": occ_val,
                "annual_family_income": float(inc_val),
                "education_level": edu_val,
                "social_category": cat_val,
                "disability_status": dis_val,
                "marital_status": mar_val,
                "additional_attributes": add_attrs,
                "onboarding_completed": 1,
            }
            save_user_profile(user_id, updated_data)
            st.session_state.user_profile = updated_data
            st.session_state.active_view = "recommendations"
            st.success("Profile updated successfully! Recalculating recommendations...")
            st.rerun()
