"""
Schemate AI Eligibility and Recommendation Engine Package.
Provides profile management, deterministic rule-based scheme evaluation,
and personalized ranking of Indian Government welfare schemes.
"""

from eligibility.profile_service import (
    get_profile,
    save_profile,
    set_language,
    is_onboarded,
    get_profile_summary,
)
from eligibility.scheme_rules import load_all_scheme_rules, SchemeRule
from eligibility.eligibility_engine import evaluate_scheme, EvaluationResult
from eligibility.recommendation_service import (
    get_recommendations_for_user,
    get_recommendations_for_profile,
)

__all__ = [
    "get_profile",
    "save_profile",
    "set_language",
    "is_onboarded",
    "get_profile_summary",
    "load_all_scheme_rules",
    "SchemeRule",
    "evaluate_scheme",
    "EvaluationResult",
    "get_recommendations_for_user",
    "get_recommendations_for_profile",
]
