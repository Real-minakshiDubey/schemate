import json
import re
from ftfy import fix_text

HEADINGS = ["Details", "Benefits", "Eligibility", "Exclusions",
            "Application Process", "Documents Required",
            "Frequently Asked Questions", "Sources And References"]


def clean(text):
    text = fix_text(text)
    text = re.sub(r"[\u200b-\u200d\ufeff\x80-\x9f]", "", text)
    return text.replace("â€", '"')


with open("data/processed/schemes_extended.json", encoding="utf-8") as f:
    records = json.load(f)

mp = [x for x in records if "madhya pradesh" in x["region"].lower()]
r = mp[0]
text = clean(r["text"])
print("NAME:", r["name"], "| length:", len(text))

for h in HEADINGS:
    matches = list(re.finditer(re.escape(h), text))
    print(f"\n### {h}: {len(matches)} matches")
    for m in matches[:4]:
        s, e = max(0, m.start() - 30), min(len(text), m.end() + 30)
        print(f"  at {m.start()}: {text[s:e]!r}")