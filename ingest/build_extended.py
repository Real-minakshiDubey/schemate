import glob
import json
import os
import random
import re
import time
import pdfplumber

DEV_SIZE = 200
random.seed(42)

SIGN_OUT = "Are you sure you want to sign out?"
MARKER = "Check Eligibility"

paths = sorted(glob.glob("data/raw/myscheme/**/*.pdf", recursive=True))
paths = [p for p in paths if " copy" not in os.path.basename(p).lower()]
print("PDFs after removing 'copy' files:", len(paths))

records, seen = [], set()
skipped = dupes = 0
start = time.time()

for i, path in enumerate(paths, 1):
    try:
        with pdfplumber.open(path) as pdf:
            raw = "\n".join((p.extract_text() or "") for p in pdf.pages).strip()
    except Exception as e:
        print("Failed:", os.path.basename(path), str(e)[:80])
        skipped += 1
        continue

    if len(raw) < 200:
        skipped += 1
        continue

    # name: text ke shuru se, filename se nahi
    if SIGN_OUT in raw:
        name = raw.split(SIGN_OUT)[0].replace("\n", " ").strip()
    else:
        name = os.path.splitext(os.path.basename(path))[0]

    # duplicate scheme names hatao
    key = re.sub(r"\W+", "", name.lower())
    if key in seen:
        dupes += 1
        continue
    seen.add(key)

    # UI kachra hatao: "Check Eligibility" ke baad ka hissa rakho
    body = raw.split(MARKER, 1)[1].strip() if MARKER in raw else raw

    # region (state ya ministry): body mein naam se pehle ka hissa
    pos = body.find(name[:25])
    region = body[:pos].strip() if pos >= 0 else ""
    if pos >= 0:
        body = body[pos:]

    records.append({
        "id": f"{len(records):04d}",
        "name": name,
        "region": region,
        "text": body,
        "file": os.path.basename(path),
        "language": "en",
        "verified": False,
        "split": "full_only",
        "source": "myscheme.gov.in via Hugging Face dataset shrijayan/gov_myscheme",
    })

    if i % 200 == 0:
        print(f"{i}/{len(paths)} done, {time.time() - start:.0f}s elapsed")

# dev subset: pehle saari Madhya Pradesh schemes, phir random se 200 tak bharo
mp_idx = [k for k, r in enumerate(records) if "madhya pradesh" in r["region"].lower()]
others = [k for k in range(len(records)) if k not in set(mp_idx)]
random.shuffle(others)
dev_idx = (mp_idx + others)[:DEV_SIZE]
for k in dev_idx:
    records[k]["split"] = "dev"

os.makedirs("data/processed", exist_ok=True)
with open("data/processed/schemes_extended.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False)

print()
print("Saved:", len(records), "| Skipped:", skipped, "| Duplicates:", dupes)
print("Madhya Pradesh schemes:", len(mp_idx), "| Dev subset:", len(dev_idx))
print(f"Total time: {time.time() - start:.0f}s")

print("\n--- 3 sample records ---")
for r in records[:3]:
    print("NAME:", r["name"])
    print("REGION:", r["region"])
    print("TEXT:", r["text"][:300].replace("\n", " "))
    print()