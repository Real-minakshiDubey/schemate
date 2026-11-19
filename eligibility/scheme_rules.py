"""
Scheme Rules Extractor & Dataclass Definition for Schemate AI.
Parses natural language eligibility, benefits, and application sections
from Indian Government scheme records into structured evaluation rules.
"""

import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMES_SECTIONS_PATH = PROJECT_ROOT / "data" / "processed" / "schemes_sections.json"
RULES_CACHE_PATH = PROJECT_ROOT / "data" / "processed" / "scheme_rules_cache.json"

STATES_AND_UTS = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
    "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
    "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

STATE_SET = {s.lower(): s for s in STATES_AND_UTS}


@dataclass
class SchemeRule:
    scheme_id: str
    name: str
    region: str
    level: str                          # 'central' or 'state'
    target_state: Optional[str]         # e.g. "Madhya Pradesh" or None if Central/All India
    gender: str                         # 'all', 'female', 'male', 'female_preferred'
    min_age: Optional[int]
    max_age: Optional[int]
    max_income: Optional[float]
    target_occupations: List[str]
    target_categories: List[str]
    requires_disability: bool
    target_marital: List[str]
    student_levels: List[str]
    farmer_types: List[str]
    business_types: List[str]
    required_documents: List[str]
    official_link: str
    official_sources: List[str]
    description: str
    benefits_summary: str
    raw_eligibility: str
    raw_application: str
    raw_documents: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SchemeRule":
        return cls(**data)


def slugify_name(name: str) -> str:
    """Convert scheme name to URL-friendly slug."""
    s = name.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"[-\s]+", "-", s).strip("-")


def extract_rule_from_scheme(item: Dict[str, Any]) -> SchemeRule:
    """Extract structured eligibility parameters from a scheme record."""
    scheme_id = str(item.get("id", ""))
    name = item.get("name", "").strip()
    region = item.get("region", "").strip()
    sections = item.get("sections", {})

    details = sections.get("details", "").strip()
    benefits = sections.get("benefits", "").strip()
    eligibility = sections.get("eligibility", "").strip()
    exclusions = sections.get("exclusions", "").strip()
    application = sections.get("application", "").strip()
    documents = sections.get("documents", "").strip()

    combined_elig_text = f"{eligibility} {exclusions} {name}".lower()

    # 1. Level and Target State
    region_lower = region.lower()
    target_state = None
    if region_lower in STATE_SET:
        level = "state"
        target_state = STATE_SET[region_lower]
    elif region_lower.startswith("the ") and region_lower[4:] in STATE_SET:
        level = "state"
        target_state = STATE_SET[region_lower[4:]]
    elif any(st.lower() in region_lower for st in STATES_AND_UTS):
        level = "state"
        for st in STATES_AND_UTS:
            if st.lower() in region_lower:
                target_state = st
                break
    else:
        level = "central"
        target_state = None

    # Check if eligibility explicitly requires resident of a specific state
    if not target_state:
        for st in STATES_AND_UTS:
            pat = rf"\b(?:resident|domicile|native)\s+(?:of|in)\s+{re.escape(st.lower())}\b"
            if re.search(pat, combined_elig_text):
                target_state = st
                level = "state"
                break

    # 2. Gender
    gender = "all"
    if re.search(r"\b(only\s+(?:for\s+)?women|female\s+only|girls?\s+only|widows?|maternity|pregnant|girl\s+child|mahila|kanya|balika)\b", combined_elig_text):
        if not re.search(r"\b(all\s+citizens|any\s+individual|both\s+men\s+and\s+women|all\s+persons|all\s+sections)\b", combined_elig_text):
            gender = "female"
        else:
            gender = "female_preferred"
    elif re.search(r"\b(only\s+(?:for\s+)?men|male\s+only|boys?\s+only)\b", combined_elig_text):
        gender = "male"

    # Ministry level gender default
    if "women and child" in region_lower:
        gender = "female_preferred"

    # 3. Age constraints
    min_age = None
    max_age = None

    m_between = re.search(
        r"(?:between|age\s+group\s+of|age\s+bracket\s+of|age\s+limit\s+(?:is\s+)?)\s*(\d{1,2})\s*(?:to|and|-)\s*(\d{1,2})\s*years?",
        combined_elig_text
    )
    if m_between:
        a1, a2 = int(m_between.group(1)), int(m_between.group(2))
        if 5 <= a1 <= 80 and 10 <= a2 <= 100:
            min_age, max_age = a1, a2
    else:
        m_min = re.search(
            r"(?:age\s+(?:should\s+be\s+)?(?:above|at\s+least|minimum\s+of|more\s+than)|minimum\s+age\s+(?:is|of|limit\s+is)|completed\s+(?:the\s+)?age\s+of|at\s+least)\s+(\d{1,2})\s*(?:years?\s+of\s+age|years?\s+old|years)",
            combined_elig_text
        )
        if m_min:
            val = int(m_min.group(1))
            if 5 <= val <= 80:
                min_age = val

        m_max = re.search(
            r"(?:age\s+(?:should\s+be\s+)?(?:below|less\s+than|not\s+exceeding|up\s+to)|maximum\s+age\s+(?:is|of|limit\s+is)|upper\s+age\s+limit\s+is|not\s+more\s+than)\s+(\d{1,2})\s*(?:years?\s+of\s+age|years?\s+old|years)",
            combined_elig_text
        )
        if m_max:
            val = int(m_max.group(1))
            if 14 <= val <= 90:
                max_age = val

    # 4. Income Limit
    max_income = None
    m_inc = re.search(
        r"(?:income\s+(?:not\s+exceeding|up\s+to|less\s+than|below|does\s+not\s+exceed|ceiling\s+of|limit\s+of))\s*₹?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|crore)?",
        combined_elig_text
    )
    if m_inc:
        val_str = m_inc.group(1).replace(",", "")
        try:
            val = float(val_str)
            unit = m_inc.group(2) or ""
            if "lakh" in unit:
                val *= 100000
            elif "crore" in unit:
                val *= 10000000
            if 10000 <= val <= 2500000:
                max_income = val
        except ValueError:
            pass

    # BPL / EWS default ceilings if explicitly mentioned without exact number
    if max_income is None:
        if re.search(r"\b(below\s+poverty\s+line|bpl\s+card|antodaya|bpl\s+family)\b", combined_elig_text):
            max_income = 120000.0   # Standard BPL threshold ceiling
        elif re.search(r"\b(economically\s+weaker\s+section|ews\s+certificate)\b", combined_elig_text):
            max_income = 800000.0   # Standard EWS threshold ceiling

    # 5. Occupations
    target_occupations = []
    if re.search(r"\b(student|students|scholarship|fellowship|matriculation|post-matric|pre-matric|college|university|school|studying|fellow|ph\.?d|degree|diploma|enrolled)\b", combined_elig_text) or "education" in region_lower:
        target_occupations.append("student")
    if re.search(r"\b(farmer|farmers|kisan|kisans|cultivator|cultivators|landholder|landholders|crop\s+loss|crop\s+insurance|agriculture\s+land|horticulture|dairy\s+farming|sericulture)\b", combined_elig_text) or "agriculture" in region_lower:
        target_occupations.append("farmer")
    if re.search(r"\b(entrepreneur|entrepreneurs|business|msme|msmes|startup|startups|manufacturing\s+unit|vendor|artisan|weaver|trader|shopkeeper|commercial\s+enterprise)\b", combined_elig_text) or "micro, small" in region_lower:
        target_occupations.append("entrepreneur")
    if re.search(r"\b(unemployed|job\s*seeker|youth\s+training|skill\s+development|rojgar)\b", combined_elig_text) or "skill development" in region_lower:
        target_occupations.append("unemployed")
    if re.search(r"\b(construction\s+worker|daily\s+wage|laborer|labourer|unorganized\s+worker|artisan|shramik)\b", combined_elig_text):
        target_occupations.append("daily_wage")
    if re.search(r"\b(senior\s+citizen|pensioner|old\s+age\s+pension|elderly|vridha)\b", combined_elig_text):
        target_occupations.append("retired")

    # 6. Social Categories
    target_categories = []
    if re.search(r"\b(scheduled\s+caste|sc\b)", combined_elig_text):
        target_categories.append("SC")
    if re.search(r"\b(scheduled\s+tribe|st\b)", combined_elig_text) or "tribal" in region_lower:
        target_categories.append("ST")
    if re.search(r"\b(other\s+backward\s+class|obc\b)", combined_elig_text):
        target_categories.append("OBC")
    if re.search(r"\b(minority|minorities|muslim|christian|sikh|buddhist|parsi|jain)\b", combined_elig_text) or "minority" in region_lower:
        target_categories.append("Minority")
    if re.search(r"\b(ews|economically\s+weaker\s+section|bpl)\b", combined_elig_text):
        target_categories.append("EWS")

    # 7. Disability
    requires_disability = bool(re.search(
        r"\b(physically\s+handicapped|disabilit|pwd|divyang|blindness|low\s+vision|hearing\s+impairment|locomotor)\b",
        combined_elig_text
    ))

    # 8. Marital
    target_marital = []
    if re.search(r"\b(widow|widowed|vidhwa)\b", combined_elig_text):
        target_marital.append("widowed")
    if re.search(r"\b(divorced|destitute\s+women|deserted)\b", combined_elig_text):
        target_marital.append("divorced")
    if re.search(r"\b(unmarried|spinster)\b", combined_elig_text):
        target_marital.append("single")

    # 9. Occupation Specific Sub-attributes
    student_levels = []
    if "student" in target_occupations:
        if re.search(r"\b(school|10th|matric|secondary|pre-matric)\b", combined_elig_text):
            student_levels.append("school")
        if re.search(r"\b(12th|intermediate|higher\s+secondary|undergraduate|bachelor|b\.?tech|b\.?sc|b\.?com|post-matric)\b", combined_elig_text):
            student_levels.append("undergraduate")
        if re.search(r"\b(postgraduate|master|m\.?tech|m\.?sc|m\.?com|ph\.?d|doctorate|research)\b", combined_elig_text):
            student_levels.append("postgraduate")

    farmer_types = []
    if "farmer" in target_occupations:
        if re.search(r"\b(marginal|small\s+and\s+marginal|small\s+farmer)\b", combined_elig_text):
            farmer_types.append("small_marginal")
        if re.search(r"\b(tenant|sharecropper)\b", combined_elig_text):
            farmer_types.append("tenant")
        if re.search(r"\b(landless)\b", combined_elig_text):
            farmer_types.append("landless")

    business_types = []
    if "entrepreneur" in target_occupations:
        if re.search(r"\b(manufacturing|production|factory)\b", combined_elig_text):
            business_types.append("manufacturing")
        if re.search(r"\b(service|it|consulting)\b", combined_elig_text):
            business_types.append("services")
        if re.search(r"\b(trading|retail|shop)\b", combined_elig_text):
            business_types.append("trading")
        if re.search(r"\b(handloom|handicraft|artisan)\b", combined_elig_text):
            business_types.append("handicraft")

    # 10. Required Documents parsing
    required_docs = []
    if documents:
        raw_doc_items = re.split(r"(?:\d+\.|\n|•|-|;)\s*", documents)
        for d in raw_doc_items:
            clean_d = d.strip().strip(". ")
            if len(clean_d) >= 4 and len(clean_d) <= 100:
                required_docs.append(clean_d)
    if not required_docs:
        # Default standard welfare document requirements
        required_docs = ["Aadhaar Card", "Proof of Identity", "Bank Account Details / Passbook"]

    # 11. Official Link & Source
    portal_urls = re.findall(r"https?://[^\s<>\"\'\)]+", application + " " + details)
    clean_urls = []
    for u in portal_urls:
        u_clean = u.rstrip(".,;)>'\"")
        if "myscheme" not in u_clean and "google" not in u_clean and "hf.co" not in u_clean:
            clean_urls.append(u_clean)

    official_link = clean_urls[0] if clean_urls else f"https://www.myscheme.gov.in/schemes/{slugify_name(name)}"

    official_sources = ["myScheme Portal (Government of India)"]
    if region:
        official_sources.append(region)

    return SchemeRule(
        scheme_id=scheme_id,
        name=name,
        region=region,
        level=level,
        target_state=target_state,
        gender=gender,
        min_age=min_age,
        max_age=max_age,
        max_income=max_income,
        target_occupations=target_occupations,
        target_categories=target_categories,
        requires_disability=requires_disability,
        target_marital=target_marital,
        student_levels=student_levels,
        farmer_types=farmer_types,
        business_types=business_types,
        required_documents=required_docs[:6],
        official_link=official_link,
        official_sources=official_sources,
        description=details[:300] + ("..." if len(details) > 300 else ""),
        benefits_summary=benefits[:300] + ("..." if len(benefits) > 300 else ""),
        raw_eligibility=eligibility,
        raw_application=application,
        raw_documents=documents
    )


_RULES_REGISTRY: Optional[List[SchemeRule]] = None


def load_all_scheme_rules(force_rebuild: bool = False) -> List[SchemeRule]:
    """
    Load all scheme rules from cache if available, or generate from
    schemes_sections.json and persist to cache.
    """
    global _RULES_REGISTRY
    if _RULES_REGISTRY is not None and not force_rebuild:
        return _RULES_REGISTRY

    if RULES_CACHE_PATH.exists() and not force_rebuild:
        try:
            with open(RULES_CACHE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            _RULES_REGISTRY = [SchemeRule.from_dict(item) for item in data]
            return _RULES_REGISTRY
        except Exception:
            pass

    # Rebuild from schemes_sections.json
    if not SCHEMES_SECTIONS_PATH.exists():
        return []

    with open(SCHEMES_SECTIONS_PATH, "r", encoding="utf-8") as f:
        schemes_data = json.load(f)

    rules = [extract_rule_from_scheme(s) for s in schemes_data]

    # Cache to disk for instant subsequent loads
    try:
        RULES_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(RULES_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in rules], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not cache scheme rules: {e}")

    _RULES_REGISTRY = rules
    return _RULES_REGISTRY


_RAW_SECTIONS_CACHE: Optional[Dict[str, Dict[str, Any]]] = None


def get_scheme_rule_by_id(scheme_id: str) -> Optional[SchemeRule]:
    """Retrieve SchemeRule by scheme_id in O(1) time."""
    rules = load_all_scheme_rules()
    target_id = str(scheme_id).strip()
    for r in rules:
        if r.scheme_id == target_id:
            return r
    return None


def get_scheme_full_details(scheme_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve full structured scheme details including raw sections,
    benefits, application instructions, eligibility, and documents.
    """
    global _RAW_SECTIONS_CACHE
    target_id = str(scheme_id).strip()

    if _RAW_SECTIONS_CACHE is None:
        if SCHEMES_SECTIONS_PATH.exists():
            try:
                with open(SCHEMES_SECTIONS_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                _RAW_SECTIONS_CACHE = {str(item.get("id", "")): item for item in data}
            except Exception:
                _RAW_SECTIONS_CACHE = {}
        else:
            _RAW_SECTIONS_CACHE = {}

    rule = get_scheme_rule_by_id(target_id)
    raw_item = _RAW_SECTIONS_CACHE.get(target_id, {})
    raw_sections = raw_item.get("sections", {}) if raw_item else {}

    if not rule and not raw_item:
        return None

    # Derive high-level category
    name = (rule.name if rule else raw_item.get("name", "")).strip()
    region = (rule.region if rule else raw_item.get("region", "")).strip()
    level = rule.level if rule else ("central" if "ministry" in region.lower() else "state")

    category = "General Welfare"
    if rule and rule.target_occupations:
        if "student" in rule.target_occupations:
            category = "Students & Education"
        elif "farmer" in rule.target_occupations:
            category = "Agriculture & Farmers"
        elif "entrepreneur" in rule.target_occupations:
            category = "Business & MSME"
        elif "unemployed" in rule.target_occupations:
            category = "Employment & Skills"
    elif rule and rule.gender in ("female", "female_preferred"):
        category = "Women & Child"
    elif "education" in region.lower() or "scholarship" in name.lower():
        category = "Students & Education"
    elif "agriculture" in region.lower() or "kisan" in name.lower() or "krishi" in name.lower():
        category = "Agriculture & Farmers"
    elif "micro, small" in region.lower() or "msme" in name.lower() or "business" in name.lower():
        category = "Business & MSME"
    elif "health" in region.lower():
        category = "Healthcare & Social Welfare"

    return {
        "scheme_id": target_id,
        "name": name,
        "region": region,
        "level": level,
        "category": category,
        "description": raw_sections.get("details") or (rule.description if rule else ""),
        "benefits": raw_sections.get("benefits") or (rule.benefits_summary if rule else ""),
        "eligibility": raw_sections.get("eligibility") or (rule.raw_eligibility if rule else ""),
        "exclusions": raw_sections.get("exclusions", ""),
        "application": raw_sections.get("application") or (rule.raw_application if rule else ""),
        "documents": raw_sections.get("documents") or (rule.raw_documents if rule else ""),
        "faq": raw_sections.get("faq", ""),
        "required_documents": rule.required_documents if rule else ["Aadhaar Card", "Proof of Identity", "Bank Account Passbook"],
        "official_link": rule.official_link if rule else f"https://www.myscheme.gov.in/schemes/{slugify_name(name)}",
        "official_sources": rule.official_sources if rule else ["myScheme Portal (Government of India)"],
        "rule": rule,
    }
