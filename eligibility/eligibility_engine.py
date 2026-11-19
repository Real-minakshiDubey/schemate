"""
Deterministic Scheme Eligibility Evaluation Engine for Schemate AI.
Evaluates structured rules against user profile attributes with zero LLM hallucination.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from eligibility.scheme_rules import SchemeRule


@dataclass
class EvaluationResult:
    scheme_id: str
    name: str
    region: str
    level: str
    status: str                         # 'Potentially Eligible', 'Needs Verification', 'Not Eligible'
    score: float                        # 0.0 to 100.0 relevance and match score
    match_reasons: List[str]            # Why the user matches
    missing_criteria: List[str]         # Missing info or verification needed
    disqualification_reasons: List[str] # Reasons if disqualified
    required_documents: List[str]
    official_link: str
    official_sources: List[str]
    benefits_summary: str
    description: str


def normalize_occupation(raw_occ: Optional[str]) -> str:
    """Normalize raw occupation string to canonical category key."""
    if not raw_occ:
        return "other"
    low = raw_occ.lower()
    if "student" in low:
        return "student"
    if "farmer" in low or "agri" in low:
        return "farmer"
    if "entrepreneur" in low or "msme" in low or "business" in low:
        return "entrepreneur"
    if "daily wage" in low or "labor" in low or "artisan" in low:
        return "daily_wage"
    if "unemployed" in low or "seeker" in low:
        return "unemployed"
    if "salaried" in low:
        return "salaried"
    if "self-employed" in low or "freelance" in low:
        return "self_employed"
    if "homemaker" in low:
        return "homemaker"
    if "retired" in low or "senior" in low:
        return "retired"
    return "other"


def evaluate_scheme(rule: SchemeRule, profile: Dict[str, Any]) -> EvaluationResult:
    """
    Deterministically evaluates a scheme rule against a user profile.
    
    Rules:
    - Never confidently claims eligibility if key conditions cannot be verified.
    - If explicit contradictions exist -> 'Not Eligible'.
    - If core conditions match and prerequisites require verification -> 'Needs Verification'.
    - If all specific conditions match and profile provides solid evidence -> 'Potentially Eligible'.
    """
    match_reasons: List[str] = []
    missing_criteria: List[str] = []
    disqualification_reasons: List[str] = []
    score: float = 10.0  # Base score for any relevant government welfare scheme

    p_age = profile.get("age")
    p_gender = profile.get("gender")
    p_state = profile.get("state")
    p_occ_raw = profile.get("occupation")
    p_occ = normalize_occupation(p_occ_raw)
    p_income = profile.get("annual_family_income")
    p_cat = profile.get("social_category")
    p_dis = profile.get("disability_status")
    p_mar = profile.get("marital_status")
    p_attr = profile.get("additional_attributes") or {}

    # -------------------------------------------------------------
    # 1. State / Jurisdiction Check
    # -------------------------------------------------------------
    if rule.level == "state":
        if rule.target_state:
            if p_state:
                p_state_clean = p_state.strip().lower()
                target_clean = rule.target_state.strip().lower()
                if p_state_clean == target_clean:
                    match_reasons.append(f"Resident of target state: {rule.target_state}")
                    score += 25.0
                else:
                    disqualification_reasons.append(
                        f"State-specific scheme for {rule.target_state} (Your profile: {p_state})"
                    )
            else:
                missing_criteria.append(f"Verification of domicile / residency in {rule.target_state}")
    else:
        # Central schemes apply nationwide
        match_reasons.append("Central Government Scheme (Applicable nationwide across all States & UTs)")
        score += 15.0

    # -------------------------------------------------------------
    # 2. Gender Check
    # -------------------------------------------------------------
    if rule.gender == "female":
        if p_gender == "Male":
            disqualification_reasons.append("Exclusively designated for women / female beneficiaries")
        elif p_gender == "Female":
            match_reasons.append("Meets female beneficiary criteria")
            score += 20.0
        else:
            missing_criteria.append("Verification of female applicant eligibility")
    elif rule.gender == "female_preferred":
        if p_gender == "Female":
            match_reasons.append("Provides special priority / benefits for female applicants")
            score += 10.0
    elif rule.gender == "male":
        if p_gender == "Female":
            disqualification_reasons.append("Exclusively designated for male beneficiaries")

    # -------------------------------------------------------------
    # 3. Age Constraints Check
    # -------------------------------------------------------------
    if p_age is not None:
        try:
            age_int = int(p_age)
            if rule.min_age and age_int < rule.min_age:
                disqualification_reasons.append(
                    f"Minimum age requirement is {rule.min_age} years (Current age: {age_int})"
                )
            elif rule.max_age and age_int > rule.max_age:
                disqualification_reasons.append(
                    f"Maximum age limit is {rule.max_age} years (Current age: {age_int})"
                )
            elif rule.min_age or rule.max_age:
                bounds_str = f"{rule.min_age or 0} - {rule.max_age or 'No upper limit'}"
                match_reasons.append(f"Age ({age_int} yrs) falls within eligible bracket ({bounds_str} yrs)")
                score += 15.0
        except ValueError:
            pass
    else:
        if rule.min_age or rule.max_age:
            missing_criteria.append(f"Proof of age ({rule.min_age or 0} to {rule.max_age or 'open'} years)")

    # -------------------------------------------------------------
    # 4. Income Limit Check
    # -------------------------------------------------------------
    if p_income is not None and rule.max_income is not None:
        try:
            inc_val = float(p_income)
            if inc_val > rule.max_income:
                disqualification_reasons.append(
                    f"Annual income ₹{int(inc_val):,} exceeds eligibility limit of ₹{int(rule.max_income):,}"
                )
            else:
                match_reasons.append(
                    f"Family income ₹{int(inc_val):,} is within permissible limit of ₹{int(rule.max_income):,}"
                )
                score += 20.0
        except ValueError:
            pass
    elif rule.max_income is not None:
        missing_criteria.append(
            f"Income certificate certifying annual family income under ₹{int(rule.max_income):,}"
        )

    # -------------------------------------------------------------
    # 5. Occupation & Beneficiary Group Check
    # -------------------------------------------------------------
    if rule.target_occupations:
        if p_occ in rule.target_occupations:
            match_reasons.append(f"Matches target occupation & group: {p_occ_raw}")
            score += 30.0

            # Occupation-specific bonus matches:
            if p_occ == "student":
                if p_attr.get("course"):
                    match_reasons.append(f"Active student enrolled in: {p_attr['course']}")
                    score += 5.0
                if p_attr.get("institution_type"):
                    match_reasons.append(f"Institution type: {p_attr['institution_type']}")
                    score += 5.0
            elif p_occ == "farmer":
                if p_attr.get("land_ownership"):
                    match_reasons.append(f"Landholding status: {p_attr['land_ownership']}")
                    score += 5.0
                if p_attr.get("landholding_size"):
                    match_reasons.append(f"Land size: {p_attr['landholding_size']}")
                    score += 5.0
            elif p_occ == "entrepreneur":
                if p_attr.get("business_type"):
                    match_reasons.append(f"Business sector: {p_attr['business_type']}")
                    score += 5.0
                if p_attr.get("business_stage"):
                    match_reasons.append(f"Enterprise stage: {p_attr['business_stage']}")
                    score += 5.0
        else:
            # Check for strict occupational exclusion
            if p_occ in ("student", "salaried", "homemaker") and rule.target_occupations == ["farmer"]:
                disqualification_reasons.append(f"Designated solely for farmers and cultivators (User: {p_occ_raw})")
            elif p_occ in ("farmer", "salaried", "retired") and rule.target_occupations == ["student"]:
                disqualification_reasons.append(f"Designated solely for enrolled students (User: {p_occ_raw})")
            else:
                missing_criteria.append(
                    f"Verification of status under target sector: {', '.join(rule.target_occupations).title()}"
                )

    # -------------------------------------------------------------
    # 6. Social Category Check
    # -------------------------------------------------------------
    if rule.target_categories:
        if p_cat:
            cat_matched = False
            for tc in rule.target_categories:
                if tc.lower() in p_cat.lower():
                    cat_matched = True
                    break
            if cat_matched:
                match_reasons.append(f"Qualifies under social category quota: {p_cat}")
                score += 20.0
            else:
                # If scheme strictly requires SC/ST and user is General
                if all(c in ["SC", "ST"] for c in rule.target_categories) and "general" in p_cat.lower():
                    disqualification_reasons.append(
                        f"Restricted exclusively to {', '.join(rule.target_categories)} beneficiaries (User: {p_cat})"
                    )
                else:
                    missing_criteria.append(
                        f"Category verification for {', '.join(rule.target_categories)} quota"
                    )
        else:
            missing_criteria.append(
                f"Valid Caste / Category Certificate for {', '.join(rule.target_categories)} quota"
            )

    # -------------------------------------------------------------
    # 7. Disability Status Check
    # -------------------------------------------------------------
    if rule.requires_disability:
        if p_dis and p_dis != "None":
            match_reasons.append(f"Meets disability eligibility: {p_dis}")
            score += 25.0
        elif p_dis == "None":
            disqualification_reasons.append(
                "Exclusively reserved for Persons with Disabilities (PwD / Divyangjan)"
            )
        else:
            missing_criteria.append("Valid Disability / Divyangjan Certificate (≥ 40% benchmark disability)")

    # -------------------------------------------------------------
    # 8. Marital Status Check
    # -------------------------------------------------------------
    if rule.target_marital:
        if p_mar:
            mar_clean = p_mar.lower()
            if any(tm in mar_clean for tm in rule.target_marital):
                match_reasons.append(f"Meets targeted marital status: {p_mar}")
                score += 20.0
            elif "widow" in rule.target_marital and "married" in mar_clean:
                disqualification_reasons.append("Exclusively designated for widowed beneficiaries")
            else:
                missing_criteria.append(f"Proof of status: {', '.join(rule.target_marital).title()}")
        else:
            missing_criteria.append(f"Verification of status: {', '.join(rule.target_marital).title()}")

    # -------------------------------------------------------------
    # 9. Final Eligibility Status & Ranking Logic
    # -------------------------------------------------------------
    if disqualification_reasons:
        status = "Not Eligible"
        score = round(max(0.0, min(30.0, score * 0.2)), 1)
    else:
        # If user has strong matches and minimal missing criteria
        if score >= 45.0 and len(missing_criteria) <= 1:
            status = "Potentially Eligible"
            if not missing_criteria:
                missing_criteria.append("Verification of original certificates during departmental document check")
        else:
            status = "Needs Verification"
            if not missing_criteria:
                missing_criteria.append("Confirmation of program-specific guidelines on official department portal")

        score = round(min(100.0, score), 1)

    return EvaluationResult(
        scheme_id=rule.scheme_id,
        name=rule.name,
        region=rule.region,
        level=rule.level,
        status=status,
        score=score,
        match_reasons=match_reasons,
        missing_criteria=missing_criteria,
        disqualification_reasons=disqualification_reasons,
        required_documents=rule.required_documents,
        official_link=rule.official_link,
        official_sources=rule.official_sources,
        benefits_summary=rule.benefits_summary,
        description=rule.description
    )
