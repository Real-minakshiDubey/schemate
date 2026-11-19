"""
Profile service: Handles user profile retrieval, persistence,
and profile serialization for Schemate AI.
"""

from typing import Optional, Dict, Any
from app.db import (
    get_user_profile,
    save_user_profile,
    set_user_language,
    is_onboarding_completed,
)


def get_profile(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve full profile dictionary for a given user ID."""
    return get_user_profile(user_id)


def save_profile(user_id: int, profile_data: Dict[str, Any]) -> bool:
    """Save or update user profile with validation."""
    return save_user_profile(user_id, profile_data)


def set_language(user_id: int, language: str) -> bool:
    """Update preferred language ('en', 'hi', 'hinglish')."""
    valid_langs = {"en", "hi", "hinglish"}
    if language not in valid_langs:
        language = "en"
    return set_user_language(user_id, language)


def is_onboarded(user_id: int) -> bool:
    """Returns True if the user has completed the onboarding flow."""
    return is_onboarding_completed(user_id)


def get_profile_summary(profile: Optional[Dict[str, Any]], lang: str = "en") -> str:
    """
    Generate a clear, compact summary of the user's profile for LLM prompting,
    chat context, and header displays.
    """
    if not profile:
        return "Anonymous Citizen (Profile not completed)"

    parts = []
    if profile.get("age"):
        parts.append(f"Age: {profile['age']}")
    if profile.get("gender") and profile["gender"] != "Prefer not to say":
        parts.append(f"Gender: {profile['gender']}")
    if profile.get("state"):
        loc = profile["state"]
        if profile.get("district"):
            loc += f" ({profile['district']})"
        parts.append(f"Location: {loc}")
    if profile.get("occupation"):
        parts.append(f"Occupation: {profile['occupation']}")
    if profile.get("annual_family_income"):
        try:
            inc = float(profile["annual_family_income"])
            parts.append(f"Annual Income: ₹{int(inc):,}")
        except Exception:
            parts.append(f"Annual Income: ₹{profile['annual_family_income']}")
    if profile.get("education_level"):
        parts.append(f"Education: {profile['education_level']}")
    if profile.get("social_category") and profile["social_category"] != "General / Unreserved":
        parts.append(f"Category: {profile['social_category']}")
    if profile.get("disability_status") and profile["disability_status"] != "None":
        parts.append(f"Disability: {profile['disability_status']}")
    if profile.get("marital_status"):
        parts.append(f"Marital: {profile['marital_status']}")

    add_attr = profile.get("additional_attributes") or {}
    if profile.get("occupation") == "Student":
        if add_attr.get("course"):
            parts.append(f"Course: {add_attr['course']}")
        if add_attr.get("institution_type"):
            parts.append(f"Institute: {add_attr['institution_type']}")
    elif profile.get("occupation") in ("Farmer / Agriculture", "Farmer"):
        if add_attr.get("land_ownership"):
            parts.append(f"Land: {add_attr['land_ownership']}")
        if add_attr.get("landholding_size"):
            parts.append(f"Land Size: {add_attr['landholding_size']}")
    elif profile.get("occupation") in ("Entrepreneur / MSME / Business Owner", "Entrepreneur"):
        if add_attr.get("business_type"):
            parts.append(f"Sector: {add_attr['business_type']}")
        if add_attr.get("business_stage"):
            parts.append(f"Stage: {add_attr['business_stage']}")

    return " | ".join(parts) if parts else "Citizen (Profile Incomplete)"
