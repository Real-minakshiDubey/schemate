import json
import re
from ftfy import fix_text

HEADINGS = ["Details", "Benefits", "Eligibility", "Exclusions",
            "Application Process", "Documents Required",
            "Frequently Asked Questions", "Sources And References"]

with open("data/processed/schemes_extended.json", encoding="utf-8") as f:
    records = json.load(f)

# 1. Ek record: raw vs fixed
r = records[0]
print("=== RAW (pehle 700 chars) ===")
print(r["text"][:700])
print("\n=== FIXED with ftfy ===")
print(fix_text(r["text"])[:700])

# 2. Headings kitne records mein milti hain (sirf dev subset)
dev = [x for x in records if x["split"] == "dev"]
print(f"\n=== Heading coverage in {len(dev)} dev records ===")
for h in HEADINGS:
    count = sum(1 for x in dev if h in x["text"])
    print(f"{h}: {count}/{len(dev)}")

# 3. Text length stats
lengths = sorted(len(x["text"]) for x in dev)
print("\nText length (chars): min", lengths[0],
      "| median", lengths[len(lengths) // 2], "| max", lengths[-1])

def clean(text):
    text = fix_text(text)
    text = re.sub(r"[\u200b-\u200d\ufeff\x80-\x9f]", "", text)   # chhupe hue kharab characters
    text = text.replace("â€", '"')                                # bacha hua tuta quote
    return text