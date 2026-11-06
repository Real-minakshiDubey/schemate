import json

with open("data/processed/schemes_sections.json", encoding="utf-8") as f:
    records = json.load(f)

empty = [r for r in records if not r["region"].strip()]
print("Empty region records:", len(empty))
for r in empty[:6]:
    print("-", r["name"])
    print("  file:", r["file"])
    print("  preface:", r["preface"][:200])