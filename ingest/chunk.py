import json
import re
import statistics
from collections import Counter

IN_PATH = "data/processed/schemes_sections.json"
OUT_PATH = "data/processed/chunks.json"

MAX_CHARS = 1200
OVERLAP = 150
ORDER = ["details", "benefits", "eligibility", "exclusions",
         "application", "documents", "faq"]

STATES_UTS = {s.lower() for s in [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
    "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
    "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry",
]}


def get_level(region):
    r = region.lower().strip()
    if r.startswith("the "):
        r = r[4:]
    if not r or len(r) > 100:
        return "unknown"
    if r in STATES_UTS:
        return "state"
    return "central"

def hard_split(s):
    """Jis text mein sentence boundary nahi mili, use seedha MAX_CHARS ke tukdon mein kaato."""
    step = MAX_CHARS - OVERLAP
    return [s[i:i + MAX_CHARS] for i in range(0, len(s), step)]


def split_text(text):
    """Chhota text ek chunk, bada text sentence boundary par overlap ke saath."""
    if len(text) <= MAX_CHARS:
        return [text]

    sentences = re.split(r"(?<=[.!?])\s+|(?<=[a-z][.!?])(?=[A-Z])", text)
    chunks, current = [], ""
    for s in sentences:
        if current and len(current) + len(s) + 1 > MAX_CHARS:
            chunks.append(current.strip())
            current = current[-OVERLAP:] + " " + s    # overlap
        else:
            current = (current + " " + s).strip()
    if current.strip():
        chunks.append(current.strip())

    # jo chunk ab bhi bahut bada hai (boundary nahi mili), use hard split karo
    final = []
    for c in chunks:
        if len(c) > MAX_CHARS * 1.5:
            final.extend(hard_split(c))
        else:
            final.append(c)
    return final


with open(IN_PATH, encoding="utf-8") as f:
    records = json.load(f)

chunks = []
unknown_regions = Counter()

for r in records:
    region = r["region"].strip()
    level = get_level(region)
    if level == "unknown":
        unknown_regions[region or "(empty)"] += 1

    sections = r["sections"] or {"full": r["preface"]}   # fallback
    for key in ORDER + ["full"]:
        body = sections.get(key, "")
        if not body or len(body) < 20:
            continue
        for part_no, part in enumerate(split_text(body)):
            header = f"{r['name']} ({region}) | {key}" if region else f"{r['name']} | {key}"
            chunks.append({
                "chunk_id": f"{r['id']}_{key}_{part_no}",
                "scheme_id": r["id"],
                "name": r["name"],
                "region": region,
                "level": level,
                "section": key,
                "text": f"{header}\n{part}",
                "n_chars": len(part),
                "verified": r["verified"],
                "split": r["split"],
            })

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False)

# ---- stats ----
lengths = [c["n_chars"] for c in chunks]
print("Total chunks:", len(chunks))
print("Dev chunks:", sum(1 for c in chunks if c["split"] == "dev"))
print("Chars per chunk: min", min(lengths), "| median", int(statistics.median(lengths)),
      "| max", max(lengths))
print("Chunks longer than", int(MAX_CHARS * 1.5), "chars:",
      sum(1 for n in lengths if n > MAX_CHARS * 1.5))

print("\nChunks per section:")
for k, v in Counter(c["section"] for c in chunks).most_common():
    print(f"  {k}: {v}")

print("\nLevel split:", Counter(c["level"] for c in chunks))

print("\nTop 'unknown' regions (inhe dekho, state/ministry list mein kyun nahi aaye):")
for reg, n in unknown_regions.most_common(12):
    print(f"  {reg}: {n}")