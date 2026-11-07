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
DEFAULT_COLLECTION = "schemes_dev_e5base"
FULL_COLLECTION = "schemes_full_e5base"
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
    """ChromaDB collection se persistent connection banayega.
    Agar full collection (2000+ schemes) available hai to use karega,
    warna fallback to dev collection."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        full_col = client.get_collection(FULL_COLLECTION)
        if full_col.count() > 1000:
            return full_col
    except Exception:
        pass
    return client.get_collection(DEFAULT_COLLECTION)


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

def expand_query(user_query: str) -> str:
    """
    Colloquial words, Hinglish, aur regional terms (e.g. 'viklang', 'shaadi', 'chhatravritti')
    ko official English aur formal Hindi keywords me expand karta hai taaki ChromaDB vector retrieval
    har bhasha aur script ke sawalon par highest recall de sake.
    """
    try:
        client = _get_genai_client()
        prompt = (
            "You are a search query optimizer for Indian Government Welfare Schemes (Central & State policies).\n"
            "Your task is to expand the user query into high-relevance search keywords to retrieve official scheme documents.\n"
            "Documents in the database are primarily in official English and formal Hindi.\n\n"
            "Rules:\n"
            "1. Identify the core intent, target audience (e.g. students, persons with disabilities/Divyangjan, farmers, women, unorganized workers), and benefit type (scholarship, pension, loan, grant, subsidy).\n"
            "2. Expand colloquial, slang, or Hinglish words to their formal equivalents in both English and Hindi:\n"
            "   - e.g. 'viklang' -> 'disabled persons with disabilities PwD Divyangjan दिव्यांग निःशक्तजन'\n"
            "   - e.g. 'shaadi' -> 'marriage vivah nikah विवाह'\n"
            "   - e.g. 'padhai / scholarship' -> 'scholarship fellowship chhatravritti छात्रवृत्ति'\n"
            "   - e.g. 'kisaan' -> 'farmer agriculture krishi kisan किसान'\n"
            "3. Return ONLY a concise, space-separated expansion string containing the original query plus the formal English and Hindi synonyms. Do NOT output explanations or markdown formatting.\n\n"
            f"User query: {user_query}\n"
            "Search keywords:"
        )
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        if res and res.text:
            cleaned = res.text.strip().replace("\n", " ")
            if len(cleaned) > 10:
                return cleaned
    except Exception:
        pass
    return user_query


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

    # Step 1: Query expansion (colloquial / Hinglish ko official vocabulary se link karo)
    search_query = expand_query(query)

    # Step 2: E5 query embedding ke liye 'query: ' prefix lagana zaroori hai
    query_text = "query: " + search_query.strip()
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
        "You are an assistant for SchemeSense helping Indian citizens understand government welfare schemes.\n\n"
        "Strictly follow these rules for generating the answer based ONLY on the provided Context:\n"
        "1. LANGUAGE RULES (CRITICAL):\n"
        "   - If the user's question is in English: You MUST answer strictly in standard English vocabulary and grammar (e.g. 'The eligibility criteria are...', 'The benefits include...').\n"
        "     NEVER write Hindi words in English alphabet (Hinglish like 'Aavedan karne ke liye...', 'Is yojana mein...', etc.) when the user asks in English. Answer 100% in pure English.\n"
        "   - If the user's question is in Hindi (Devanagari script) or Roman Hindi (Hinglish): Provide the answer in clear Hindi (Devanagari), followed optionally by an English summary.\n"
        "2. ACCURACY & GROUNDING: Every fact must come strictly from the Context below. Always cite the relevant scheme name for each fact.\n"
        "3. NO HALLUCINATION: If the answer is not in the context, explicitly say: 'I do not have verified information about this in my records.' (or in Hindi: 'मेरे पास इस बारे में सत्यापित जानकारी उपलब्ध नहीं है।').\n"
        "4. STRUCTURE: Be concise and structure your answer with clear bullet points: Eligibility, Benefits, Required Documents, and How to Apply."
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
