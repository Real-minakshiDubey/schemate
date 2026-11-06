import glob
import os
import pdfplumber

paths = sorted(glob.glob("data/raw/myscheme/**/*.pdf", recursive=True))
print("Total PDFs:", len(paths))
print("Folder example:", os.path.dirname(paths[0]))
print()

for path in paths[:5]:
    size_kb = os.path.getsize(path) // 1024
    with pdfplumber.open(path) as pdf:
        n_pages = len(pdf.pages)
        text = (pdf.pages[0].extract_text() or "").strip()
    print("=" * 60)
    print(os.path.basename(path), "|", size_kb, "KB |", n_pages, "pages")
    print(text[:600] if text else "[NO TEXT]")
    print()