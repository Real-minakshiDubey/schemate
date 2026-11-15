import csv
import json
import re
from collections import Counter, defaultdict


def norm(s):
    s = s.lower().replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


with open("data/processed/schemes_sections.json", encoding="utf-8") as f:
    dev = [r for r in json.load(f) if r["split"] == "dev"]

with open("eval/questions.csv", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

problems = []
groups = defaultdict(set)
for r in rows:
    if r["language"] not in {"en", "hi", "hinglish"}:
        problems.append(f"{r['qid']}: bad language {r['language']!r}")
    if not r["question"].strip():
        problems.append(f"{r['qid']}: empty question")
    groups[r["qid"].rsplit("_", 1)[0]].add(r["language"])

for g, langs in groups.items():
    if langs != {"en", "hi", "hinglish"}:
        problems.append(f"{g}: has {sorted(langs)}, need all 3")

print("Questions:", len(rows), "| per language:", dict(Counter(r["language"] for r in rows)))
print("\nName -> dev scheme (check yourself):")
for key in sorted({r["correct_name"] for r in rows}):
    hits = [d for d in dev if norm(key) in norm(d["name"])]
    status = "OK " if len(hits) == 1 else "FIX"
    detail = f"{hits[0]['id']} | {hits[0]['name'][:55]} | {hits[0]['region'][:22]}" if hits else "no match"
    print(f"  {status} {key!r}: {len(hits)} match(es) -> {detail}")
    if len(hits) != 1:
        problems.append(f"name {key!r} matches {len(hits)} dev schemes")

print("\nPROBLEMS:" if problems else "\nAll checks passed.")
for p in problems:
    print(" -", p)