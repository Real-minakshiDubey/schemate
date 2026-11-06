import json
import re
import shutil
from collections import Counter

PATH = "data/processed/schemes_extended.json"
shutil.copy(PATH, PATH + ".bak")          # backup

STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
    "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
    "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry",
]
STATES.sort(key=len, reverse=True)        # lambe naam pehle ("Madhya Pradesh" > "Pradesh")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def repair(r):
    region = r["region"].strip()
    if region and len(region) <= 80:
        return "ok"                        # theek hai, chhedo mat

    # asli text wapas jodo
    full = (region + "\n" + r["text"]) if region else r["text"]
    full = full.lstrip()
    low = full.lower()

    # 1. region state/UT se shuru hota hai
    for st in STATES:
        if low.startswith(st.lower()):
            r["region"] = st
            r["text"] = full[len(st):].lstrip()
            return "state_prefix"

    # 2. naam ko whitespace normalise karke dhoondo
    fn = norm(full)
    nn = norm(r["name"])[:25]
    pos = fn.find(nn)
    if 0 < pos <= 120:
        r["region"] = fn[:pos].strip()
        r["text"] = fn[pos:]
        return "name_found"

    # 3. nahi mila: text poora rakho, region khali
    r["region"] = ""
    r["text"] = full
    return "unresolved"


with open(PATH, encoding="utf-8") as f:
    records = json.load(f)

results = Counter()
changed = []
for r in records:
    status = repair(r)
    results[status] += 1
    if status != "ok":
        changed.append(r)

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False)

print("Results:", dict(results))
print("\nSample repaired records:")
for r in changed[:8]:
    print("-", r["name"][:60], "| region:", repr(r["region"][:50]))