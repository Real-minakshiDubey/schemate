import json

with open("data/schemes.json", encoding="utf-8") as f:
    schemes = json.load(f)

print("Total schemes:", len(schemes))

for s in schemes:
    print(s["id"], "|", s["category"], "|", s["level"])

required = ["id", "name", "category", "level", "benefits_text",
            "eligibility_text", "documents_text", "apply_text",
            "source_url", "last_verified", "language"]
allowed_levels = {"central", "MP"}

for s in schemes:
    for field in required:
        if field not in s or not s[field]:
            print(f"{s.get('id')}: field missing/empty -> {field}")
    if s.get("level") not in allowed_levels:
        print(f"{s.get('id')}: invalid level -> {s.get('level')}")