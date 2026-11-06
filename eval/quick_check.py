import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-base"
COLLECTION = "schemes_dev_e5base"
N_FETCH = 30

# (language, sawal, scheme ke naam ka koi hissa jo sahi scheme mein ho)
TESTS = [
    ("en",       "scholarship for disabled students",                        "Disabled Students To Study Abroad"),
    ("hinglish", "viklang students ke liye scholarship kaise milegi",        "Disabled Students To Study Abroad"),
    ("hi",       "दिव्यांग विद्यार्थियों के लिए छात्रवृत्ति",                  "Disabled Students To Study Abroad"),
         ("hinglish", "viklang students ke liye scholarship",                  "Disabled Students To Study Abroad"),
    ("hinglish", "divyang students ke liye scholarship kaise milegi",     "Disabled Students To Study Abroad"),
    ("hinglish", "disabled students ke liye scholarship kaise milegi",    "Disabled Students To Study Abroad"),
    ("hinglish", "disabled students scholarship kaise milegi",            "Disabled Students To Study Abroad")
    # yahan apni baaki 6 rows jodo (2 aur schemes x 3 languages)
]

col = chromadb.PersistentClient(path="data/chroma").get_collection(COLLECTION)
model = SentenceTransformer(MODEL_NAME)


def scheme_rank(query, target):
    q_vec = model.encode(["query: " + query], normalize_embeddings=True).tolist()
    res = col.query(query_embeddings=q_vec, n_results=N_FETCH, include=["metadatas"])
    seen = []
    for meta in res["metadatas"][0]:
        if meta["scheme_id"] not in seen:
            seen.append(meta["scheme_id"])
            if target.lower() in meta["name"].lower():
                return len(seen)          # scheme-level rank
    return None


print(f"{'lang':<9} {'rank':<12} query")
for lang, query, target in TESTS:
    rank = scheme_rank(query, target)
    shown = str(rank) if rank else f"not in top {N_FETCH} chunks"
    print(f"{lang:<9} {shown:<12} {query[:60]}")