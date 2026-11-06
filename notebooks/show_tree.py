import os

SKIP = {"venv", ".git", "__pycache__", "chroma", "myscheme", "text_cache", ".cache"}

def show(path=".", prefix=""):
    items = sorted(i for i in os.listdir(path) if i not in SKIP)
    for n, item in enumerate(items):
        last = n == len(items) - 1
        print(prefix + ("└── " if last else "├── ") + item)
        full = os.path.join(path, item)
        if os.path.isdir(full):
            show(full, prefix + ("    " if last else "│   "))

show()