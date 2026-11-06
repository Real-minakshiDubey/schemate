import csv
import json
import re

def norm(s):
    s = s.lower().replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()

with open("data/processed/schemes_sections.json", encoding="utf-8") as f:
    dev = [r for r in json.load(f) if r["split"] == "dev"]

with open("eval/questions.csv", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

resolved, errors = {}, []
for key in sorted({r["correct_name"] for r in rows}):
    hits = [r for r in dev if norm(key) in norm(r["name"])]
    if len(hits) == 1:
        resolved[key] = hits[0]
    else:
        errors.append((key, hits))

if errors:
    print("FIX THESE (name part must match exactly one dev scheme):")
    for key, hits in errors:
        print(f"  {key!r}: {len(hits)} matches")
        for h in hits[:5]:
            print("     -", h["id"], h["name"][:70], "|", h["region"])
    raise SystemExit(1)

with open("eval/questions.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["qid", "language", "question", "correct_ids"])
    for r in rows:
        w.writerow([r["qid"], r["language"], r["question"], resolved[r["correct_name"]]["id"]])

print("Written", len(rows), "questions -> eval/questions.csv\n")
print("Check each mapping yourself:")
for key, h in resolved.items():
    print(f"  {h['id']} | {h['name'][:60]} | {h['region'][:25]}   <- {key!r}")