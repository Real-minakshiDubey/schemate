import json
import re
from ftfy import fix_text

IN_PATH = "data/processed/schemes_extended.json"
OUT_PATH = "data/processed/schemes_sections.json"

SECTIONS = [
    ("details", r"Details"),
    ("benefits", r"Benefits"),
    ("eligibility", r"Eligibility"),
    ("exclusions", r"Exclusions"),
    ("application", r"Application\s+Process"),
    ("documents", r"Documents\s+Required"),
    ("faq", r"Frequently\s+Asked\s+Questions"),
]
END_MARKERS = [
    r"Sources\s+And\s+References",
    r"Was\s+this\s+helpful\?",
    r"Apply\s*Now\s*Check\s+Eligibility",
]
CORE = ["details", "benefits", "eligibility", "application", "documents"]


def clean(text):
    text = fix_text(text)
    text = re.sub(r"[\u200b-\u200d\ufeff\x80-\x9f]", "", text)
    text = text.replace("â€™", "'").replace("â€“", "-").replace("â€˜", "'")
    return text.replace("â€", '"')


def tidy(s):
    return re.sub(r"\s+", " ", s).strip()


def cut_end(text):
    cuts = [m.start() for p in END_MARKERS if (m := re.search(p, text))]
    return text[:min(cuts)] if cuts else text


def split_sections(text):
    content = cut_end(text)
    found, pos = [], 0
    for key, pat in SECTIONS:
        m = re.compile(pat).search(content, pos)
        if m:
            found.append((key, m.start(), m.end()))
            pos = m.end()
    sections = {}
    for i, (key, start, hend) in enumerate(found):
        end = found[i + 1][1] if i + 1 < len(found) else len(content)
        sections[key] = tidy(content[hend:end])
    preface = tidy(content[:found[0][1]]) if found else tidy(content)
    return preface, sections


with open(IN_PATH, encoding="utf-8") as f:
    records = json.load(f)

out = []
for r in records:
    preface, sections = split_sections(clean(r["text"]))
    r2 = {k: v for k, v in r.items() if k != "text"}
    r2["preface"] = preface
    r2["sections"] = sections
    r2["name"] = clean(r["name"])
    r2["region"] = clean(r["region"])
    out.append(r2)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)

# ---- stats ----
n = len(out)
print("Records:", n)
print("\nSection found:")
for key, _ in SECTIONS:
    c = sum(1 for r in out if key in r["sections"])
    print(f"  {key}: {c}/{n}")

all_core = sum(1 for r in out if all(k in r["sections"] for k in CORE))
print(f"\nAll 5 core sections found: {all_core}/{n}")

moji = sum(
    1 for r in out
    if any(b in json.dumps(r["sections"], ensure_ascii=False) for b in ["â€", "Ã", "à¤"])
)
print("Records with leftover mojibake:", moji)

print("\nRecords missing core sections (first 8):")
bad = [r for r in out if not all(k in r["sections"] for k in CORE)]
for r in bad[:8]:
    print("  ", r["name"], "-> missing", [k for k in CORE if k not in r["sections"]])

print("\n--- Sample (first Madhya Pradesh record) ---")
sample = next(r for r in out if "madhya pradesh" in r["region"].lower())
print(sample["name"])
for k, v in sample["sections"].items():
    print(f"[{k}] ({len(v)} chars) {v[:150]}")