import csv
import json
from collections import Counter, defaultdict

with open("data/processed/schemes_sections.json", encoding="utf-8") as f:
    records = json.load(f)
dev_ids = {r["id"] for r in records if r["split"] == "dev"}
name_of = {r["id"]: r["name"] for r in records}

with open("eval/questions.csv", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

problems = []
per_group = defaultdict(set)

for r in rows:
    qid = r["qid"]
    if r["language"] not in {"en", "hi", "hinglish"}:
        problems.append(f"{qid}: language must be en / hi / hinglish, got {r['language']!r}")
    if not r["question"].strip():
        problems.append(f"{qid}: question is empty")
    for cid in r["correct_ids"].split(";"):
        cid = cid.strip()
        if cid not in dev_ids:
            problems.append(f"{qid}: id {cid!r} not found in dev set (leading zero gayab?)")
    per_group[qid.rsplit("_", 1)[0]].add(r["language"])

for base, langs in per_group.items():
    if langs != {"en", "hi", "hinglish"}:
        problems.append(f"{base}: has {sorted(langs)}, need all 3 languages")

print("Questions:", len(rows))
print("Per language:", dict(Counter(r["language"] for r in rows)))
print("Distinct question groups:", len(per_group))

print("\nCorrect scheme per group (khud dekh ke confirm karo):")
shown = set()
for r in rows:
    base = r["qid"].rsplit("_", 1)[0]
    if base in shown:
        continue
    shown.add(base)
    cid = r["correct_ids"].split(";")[0].strip()
    print(f"  {base}: {name_of.get(cid, '???')[:70]}")

print("\nPROBLEMS:" if problems else "\nAll checks passed.")
for p in problems:
    print(" -", p)

    