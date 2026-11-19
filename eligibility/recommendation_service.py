"""
Recommendation Service for Schemate AI.
Orchestrates scheme retrieval, rule-based eligibility evaluation,
scoring, ranking, and explanation generation.
"""

from typing import List, Dict, Any, Optional
from eligibility.profile_service import get_profile
from eligibility.scheme_rules import load_all_scheme_rules, SchemeRule
from eligibility.eligibility_engine import evaluate_scheme, EvaluationResult


def get_recommendations_for_user(
    user_id: int,
    top_n: int = 60,
    filter_status: Optional[str] = None,
    search_query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Fetch personalized scheme recommendations for a registered user."""
    profile = get_profile(user_id)
    if not profile:
        profile = {}
    return get_recommendations_for_profile(
        profile,
        top_n=top_n,
        filter_status=filter_status,
        search_query=search_query
    )


def get_recommendations_for_profile(
    profile: Dict[str, Any],
    top_n: int = 60,
    filter_status: Optional[str] = None,
    search_query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Evaluates all schemes against the given profile, ranks by eligibility
    confidence and relevance score, and returns structured recommendation cards.
    """
    all_rules = load_all_scheme_rules()
    user_state = profile.get("state", "").strip().lower()

    # Normalize search tokens if search query provided
    search_tokens = set(search_query.lower().split()) if search_query else set()

    evaluated_results: List[EvaluationResult] = []

    for rule in all_rules:
        # Pre-filtering optimization:
        # If it's a state scheme for another state and no search query override,
        # we can still evaluate it to show as 'Not Eligible' if user filters for all,
        # or evaluate directly.
        res = evaluate_scheme(rule, profile)

        # Apply search token boost if query provided
        if search_tokens:
            target_str = (res.name + " " + res.description + " " + res.benefits_summary).lower()
            overlap = sum(1 for tok in search_tokens if tok in target_str)
            if overlap > 0:
                res.score = min(100.0, res.score + (overlap * 10.0))

        # Filter by status if requested
        if filter_status and filter_status != "All":
            if res.status.lower() != filter_status.lower():
                continue

        evaluated_results.append(res)

    # Status priority mapping for display order
    status_priority = {
        "Potentially Eligible": 3,
        "Needs Verification": 2,
        "Not Eligible": 1
    }

    # Sort primarily by status priority (Potentially Eligible first),
    # secondarily by deterministic score descending
    evaluated_results.sort(
        key=lambda x: (status_priority.get(x.status, 0), x.score),
        reverse=True
    )

    # Convert to structured dictionary list for UI & Chatbot
    output: List[Dict[str, Any]] = []
    for r in evaluated_results[:top_n]:
        output.append({
            "scheme_id": r.scheme_id,
            "name": r.name,
            "region": r.region,
            "level": r.level,
            "status": r.status,
            "score": r.score,
            "match_reasons": r.match_reasons,
            "missing_criteria": r.missing_criteria,
            "disqualification_reasons": r.disqualification_reasons,
            "required_documents": r.required_documents,
            "official_link": r.official_link,
            "official_sources": r.official_sources,
            "benefits": r.benefits_summary,
            "description": r.description
        })

    return output
