import os
import sys

# Windows console encoding fix for Devanagari / multilingual printing
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from dotenv import load_dotenv
import chromadb
from google import genai
from sentence_transformers import SentenceTransformer

# Project root resolve karo (chahe retrieval/ se chale ya app/ se import ho)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
load_dotenv()

# Constants
MODEL_NAME = "intfloat/multilingual-e5-base"
COLLECTION = "schemes_dev_e5base"
CHROMA_PATH = os.path.join(PROJECT_ROOT, "data", "chroma")
N_FETCH = 30   # ChromaDB se kitne chunks laane hain (dedup ke baad kam bachenge)
N_RESULTS = 5  # deduplicate ke baad kitne schemes dikhane hain

# Streamlit compatibility: agar streamlit me import ho to st.cache_resource use karein,
# warna standard python execution me lru_cache fallback
try:
    import streamlit as st
    cache_resource = st.cache_resource
except Exception:
    import functools
    def cache_resource(fn):
        return functools.lru_cache(maxsize=1)(fn)


# ---------------------------------------------------------------------------
# Lazy-loaded singletons
# ---------------------------------------------------------------------------

@cache_resource
def _get_model():
    """SentenceTransformer embedding model ko ek hi baar load karega."""
    return SentenceTransformer(MODEL_NAME)


@cache_resource
def _get_collection():
    """ChromaDB collection se persistent connection banayega."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_collection(COLLECTION)


@cache_resource
def _get_genai_client():
    """Gemini 2.5 Flash ke liye genai.Client banayega (.env se GEMINI_API_KEY)."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY nahi mila! Kripya .env file me GEMINI_API_KEY set karein."
        )
    return genai.Client(api_key=api_key)


# ---------------------------------------------------------------------------
# Retrieval & Generation Functions
# ---------------------------------------------------------------------------

def retrieve(query: str, n_results: int = N_RESULTS, level_filter: str = None) -> list:
    """
    User query ke aadhar par ChromaDB se relevant chunks fetch karta hai,
    phir per-scheme deduplicate karke top n_results chunks return karta hai.

    Args:
        query: User ka sawal ya search term.
        n_results: Kitni unique schemes return karni hain (default N_RESULTS=5).
        level_filter: Optional level filter ('state', 'central', etc.).

    Returns:
        List of dicts: [{scheme_id, name, region, level, section, score, text}]
    """
    model = _get_model()
    # E5 query embedding ke liye 'query: ' prefix lagana zaroori hai
    query_text = "query: " + query.strip()
    q_vec = model.encode([query_text], normalize_embeddings=True).tolist()

    col = _get_collection()
    kwargs = {
        "query_embeddings": q_vec,
        "n_results": N_FETCH,
        "include": ["documents", "metadatas", "distances"],
    }

    if level_filter:
        lvl = level_filter.strip().lower()
        if lvl not in ("all", "none", ""):
            kwargs["where"] = {"level": lvl}

    res = col.query(**kwargs)

    if not res or not res.get("documents") or not res["documents"][0]:
        return []

    docs = res["documents"][0]
    metas = res["metadatas"][0]
    dists = res["distances"][0]

    seen_schemes = set()
    chunks = []

    for doc, meta, dist in zip(docs, metas, dists):
        scheme_id = meta.get("scheme_id")
        if scheme_id in seen_schemes:
            continue  # Ek scheme ek hi baar (uska best scoring chunk)
        seen_schemes.add(scheme_id)

        chunks.append({
            "scheme_id": scheme_id,
            "name": meta.get("name", ""),
            "region": meta.get("region", ""),
            "level": meta.get("level", ""),
            "section": meta.get("section", ""),
            "score": round(1.0 - dist, 4),  # Cosine distance to similarity score (1 - dist)
            "text": doc,
        })

        if len(chunks) >= n_results:
            break

    return chunks


def generate_answer(query: str, chunks: list) -> str:
    """
    Retrieved chunks ke context ke aadhar par Gemini 2.5 Flash se grounded answer banata hai.

    Args:
        query: User ka sawal.
        chunks: retrieve() se mile hue chunks.

    Returns:
        Generated answer string.
    """
    if not chunks:
        return "Mere paas is baare mein jankari nahi hai."

    # Build context from chunks: [Name | Region | Section]\ntext
    context_blocks = []
    for c in chunks:
        header = f"[{c['name']} | {c['region']} | {c['section']}]"
        context_blocks.append(f"{header}\n{c['text']}")
    context_str = "\n\n".join(context_blocks)

    system_prompt = (
        "Aap SchemeSense ke sahayak hain jo bhartiya sarkari yojanaon (government welfare schemes) ke bare mein jankari dete hain.\n\n"
        "Neeche diye gaye Context (yojanaon ki jankari) ke aadhar par hi sawal ka jawab dein:\n"
        "1. Answer in the SAME language as the user's question (agar sawal Hindi me ho to Hindi me, English me ho to English me, Hinglish me ho to Hinglish me jawab dein).\n"
        "2. Har factual jankari ke sath sambandhit scheme ka naam cite karein.\n"
        "3. Agar jawab context mein na ho, to saaf kahein: 'Mere paas is baare mein jankari nahi hai.' Bina context ke koi bhi jankari man se na banayein.\n"
        "4. Be concise and focus on eligibility, benefits, documents, and application process."
    )

    prompt = (
        f"{system_prompt}\n\n"
        f"Context:\n{context_str}\n\n"
        f"User Question: {query}\n\n"
        f"Answer:"
    )

    try:
        client = _get_genai_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        if response and response.text:
            return response.text.strip()
        return "Mere paas is baare mein jankari nahi hai."
    except Exception as e:
        return f"Jawab generate karne mein error aaya: {e}"


def ask(query: str, n_results: int = N_RESULTS, level_filter: str = None) -> dict:
    """
    End-to-end RAG pipeline:
    1. retrieve() se top chunks lata hai
    2. generate_answer() se grounded response banata hai
    3. Agar koi chunks na milein to 'no info' answer return karta hai

    Args:
        query: User ka sawal.
        n_results: Deduplicate ke baad kitni schemes return karni hain.
        level_filter: Optional filter ('state', 'central').

    Returns:
        dict: {
            "answer": str,
            "sources": [{"name": ..., "region": ..., "section": ..., "score": ...}],
            "chunks": list of retrieved chunk dicts
        }
    """
    chunks = retrieve(query, n_results=n_results, level_filter=level_filter)

    if not chunks:
        return {
            "answer": "Mere paas is baare mein jankari nahi hai.",
            "sources": [],
            "chunks": [],
        }

    answer = generate_answer(query, chunks)
    sources = [
        {
            "name": c["name"],
            "region": c["region"],
            "section": c["section"],
            "score": c["score"],
        }
        for c in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
    }


# ---------------------------------------------------------------------------
# CLI mode
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python retrieval/rag.py "your question" [state|central]')
        sys.exit(1)

    user_query = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Question: {user_query}")
    if level:
        print(f"Filter level: {level}")
    print("\nRetrieving chunks and generating answer with Gemini 2.5 Flash...\n")

    res = ask(user_query, level_filter=level)

    print("=== Answer ===")
    print(res["answer"])
    print("\n=== Sources ===")
    if res["sources"]:
        for idx, src in enumerate(res["sources"], 1):
            print(
                f"#{idx} score={src['score']:.4f} | {src['name']} | "
                f"region={src['region']} | section={src['section']}"
            )
    else:
        print("No sources found.")
