import json
import random

PATH = "data/processed/schemes_extended.json"
DEV_SIZE = 200
random.seed(42)

with open(PATH, encoding="utf-8") as f:
    records = json.load(f)

mp = [i for i, r in enumerate(records)
      if r["region"].strip().lower() == "madhya pradesh"]
mp_set = set(mp)
others = [i for i in range(len(records)) if i not in mp_set]
random.shuffle(others)

dev = set((mp + others)[:DEV_SIZE])
for i, r in enumerate(records):
    r["split"] = "dev" if i in dev else "full_only"

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False)

print("MP schemes:", len(mp), "| Dev subset:", len(dev))
