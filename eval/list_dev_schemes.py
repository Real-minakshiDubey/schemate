import json

with open("data/processed/schemes_sections.json", encoding="utf-8") as f:
    records = json.load(f)

dev = [r for r in records if r["split"] == "dev"]
dev.sort(key=lambda r: (r["region"].lower() != "madhya pradesh", r["name"].lower()))

with open("eval/dev_schemes.txt", "w", encoding="utf-8") as out:
    for r in dev:
        out.write(f"ID: {r['id']} | {r['name']} | {r['region']}\n")
        out.write("   " + r["sections"].get("details", "")[:250] + "\n")
        out.write("   ELIG: " + r["sections"].get("eligibility", "")[:200] + "\n\n")

print("Written:", len(dev), "schemes -> eval/dev_schemes.txt")