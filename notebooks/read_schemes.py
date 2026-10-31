import json
from datetime import datetime

DATA_PATH = "data/schemes.json"

REQUIRED_FIELDS = [
    "id", "name", "category", "level", "target_group",
    "benefits_text", "eligibility_text", "documents_text", "apply_text",
    "source_url", "last_verified", "language",
]
ALLOWED_LEVELS = {"central", "MP"}
ALLOWED_LANGUAGES = {"hi", "en"}

# 1. Load
with open(DATA_PATH, encoding="utf-8") as f:
    schemes = json.load(f)

print("Total schemes:", len(schemes))
print()

# 2. Summary
for s in schemes:
    print(f"{s.get('id')} | {s.get('category')} | {s.get('level')} | {s.get('language')}")
print()

# 3. Validation
problems = []

for s in schemes:
    sid = s.get("id", "<no id>")

    # required fields present and non-empty
    for field in REQUIRED_FIELDS:
        if field not in s or not s[field]:
            problems.append(f"{sid}: field missing/empty -> {field}")

    # allowed values
    if s.get("level") not in ALLOWED_LEVELS:
        problems.append(f"{sid}: invalid level -> {s.get('level')}")
    if s.get("language") not in ALLOWED_LANGUAGES:
        problems.append(f"{sid}: invalid language -> {s.get('language')}")

    # source url
    if not str(s.get("source_url", "")).startswith("https://"):
        problems.append(f"{sid}: source_url looks wrong")

    # date format
    try:
        datetime.strptime(s.get("last_verified", ""), "%Y-%m-%d")
    except ValueError:
        problems.append(f"{sid}: last_verified must be YYYY-MM-DD")

    # target_group should be a list
    if not isinstance(s.get("target_group"), list):
        problems.append(f"{sid}: target_group must be a list")

# duplicate ids
ids = [s.get("id") for s in schemes]
if len(ids) != len(set(ids)):
    problems.append("Duplicate ids found")

# 4. Result
if problems:
    print("PROBLEMS FOUND:")
    for p in problems:
        print(" -", p)
else:
    print("All checks passed.")