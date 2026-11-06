import os
import sys
import time
import requests
import urllib3
from bs4 import BeautifulSoup
from datetime import date

if len(sys.argv) < 3:
    raise SystemExit("Usage: python notebooks\\scrape_page.py <url> <name> [--no-verify]")

URL = sys.argv[1]
OUT_NAME = sys.argv[2]
VERIFY_SSL = "--no-verify" not in sys.argv   # default: safe

KEYWORDS = ["eligib", "benefit", "document", "apply", "पात्र", "लाभ", "दस्तावेज", "आवेदन"]
HEADERS = {"User-Agent": "Mozilla/5.0 (student project, schemate)"}

if not VERIFY_SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=15, verify=VERIFY_SSL)
    except requests.exceptions.RequestException as e:
        print("Request failed:", str(e)[:200])
        return None


def extract_lines(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    lines = []
    for line in soup.get_text(separator="\n").splitlines():
        line = line.strip()
        if line and line not in lines:
            lines.append(line)
    return lines


resp = fetch(URL)
if resp is None or resp.status_code != 200:
    raise SystemExit("Fetch failed")

lines = extract_lines(resp.text)
hits = [l for l in lines if any(k in l.lower() for k in KEYWORDS)]

print("Total lines:", len(lines))
print("Lines with scheme keywords:", len(hits))
for l in hits[:30]:
    print("-", l[:150])

os.makedirs("data/raw", exist_ok=True)
with open(f"data/raw/{OUT_NAME}.txt", "w", encoding="utf-8") as f:
    f.write(f"SOURCE: {URL}\nFETCHED: {date.today().isoformat()}\n\n")
    f.write("\n".join(lines))
print(f"\nSaved to data/raw/{OUT_NAME}.txt")
time.sleep(2)