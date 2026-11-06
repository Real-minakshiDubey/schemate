import os
import time
import requests
import urllib3
from bs4 import BeautifulSoup
from datetime import date

URL = "https://pmkisan.gov.in"
OUT_NAME = "pm_kisan"
VERIFY_SSL = False   # sirf public page padhne ke liye, key wale code mein kabhi nahi

HEADERS = {"User-Agent": "Mozilla/5.0 (student project, schemate)"}
if not VERIFY_SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=15, verify=VERIFY_SSL)
    except requests.exceptions.RequestException as e:
        print("Request failed:", str(e)[:200])
        return None


def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()          # kachra hatao
    lines = []
    for line in soup.get_text(separator="\n").splitlines():
        line = line.strip()
        if line and line not in lines:   # khali aur duplicate lines hatao
            lines.append(line)
    return lines


resp = fetch(URL)
if resp is None or resp.status_code != 200:
    raise SystemExit("Fetch failed")

lines = extract_text(resp.text)
print("Total lines:", len(lines))
print()
for line in lines[:60]:
    print("-", line)

# raw save (data/raw gitignored hai)
os.makedirs("data/raw", exist_ok=True)
with open(f"data/raw/{OUT_NAME}.txt", "w", encoding="utf-8") as f:
    f.write(f"SOURCE: {URL}\n")
    f.write(f"FETCHED: {date.today().isoformat()}\n\n")
    f.write("\n".join(lines))

print("\nSaved to data/raw/", OUT_NAME, ".txt", sep="")
time.sleep(2)