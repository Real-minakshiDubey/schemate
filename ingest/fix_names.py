import glob
import json
import os
import re
import shutil
import pdfplumber

PATH = "data/processed/schemes_extended.json"
shutil.copy(PATH, PATH + ".bak2")

STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
    "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
    "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry",
]
STATES.sort(key=len, reverse=True)

SIGN_OUT = re.compile(r"Are\s+you\s+sure\s+you\s+want\s+to\s+sign\s+out\?")
MARKER = re.compile(r"Check\s+Eligibility")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


path_of = {os.path.basename(p): p
           for p in glob.glob("data/raw/myscheme/**/*.pdf", recursive=True)}

with open(PATH, encoding="utf-8") as f:
    records = json.load(f)

todo = [r for r in records if r["name"] == os.path.splitext(r["file"])[0]]
print("Records with filename as name:", len(todo))

fixed = failed = 0
for r in todo:
    path = path_of.get(r["file"])
    if not path:
        failed += 1
        continue
    with pdfplumber.open(path) as pdf:
        raw = "\n".join((p.extract_text() or "") for p in pdf.pages[:5])

    m_out, m_mark = SIGN_OUT.search(raw), MARKER.search(raw)
    if not (m_out and m_mark):
        failed += 1
        continue

    name = norm(raw[:m_out.start()])
    body = norm(raw[m_mark.end():])

    region, text = "", body
    for st in STATES:
        if body.lower().startswith(st.lower()):
            region, text = st, body[len(st):].lstrip()
            break
    else:
        pos = body.find(name[:25])
        if 0 < pos <= 120:
            region, text = body[:pos].strip(), body[pos:]

    r["name"], r["region"], r["text"] = name, region, text
    fixed += 1

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False)

print("Fixed:", fixed, "| Could not fix:", failed)
print("\nSamples:")
for r in todo[:8]:
    print("-", r["name"][:70], "| region:", repr(r["region"][:40]))
    