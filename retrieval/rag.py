import os
import sys
import zipfile
import urllib.request

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

# URL to download prebuilt Chroma vector store if not present on deployment platform
CHROMA_DATA_URL = os.getenv(
    "CHROMA_DATA_URL",
    "https://github.com/Real-minakshiDubey/schemate/releases/download/v1.0.0/chroma_db.zip",
)

# Streamlit compatibility: agar streamlit me import ho to st.cache_resource use karein,
# warna standard python execution me lru_cache fallback
try:
    import streamlit as st
    cache_resource = st.cache_resource
except Exception:
    import functools
    def cache_resource(fn):
        return functools.lru_cache(maxsize=1)(fn)


def ensure_chroma_ready():
    """ChromaDB database file check karta hai.
    Agar deployed environment (jaise Streamlit Cloud) me data/chroma maujood nahi hai,
    to pre-indexed zip download karke extract karega."""
    sqlite_file = os.path.join(CHROMA_PATH, "chroma.sqlite3")
    if not os.path.exists(sqlite_file):
        os.makedirs(CHROMA_PATH, exist_ok=True)
        zip_temp_path = os.path.join(PROJECT_ROOT, "chroma_temp.zip")
        print(f"ChromaDB not found at {sqlite_file}. Downloading from {CHROMA_DATA_URL}...")
        try:
            # Download zip
            urllib.request.urlretrieve(CHROMA_DATA_URL, zip_temp_path)
            # Extract to data/chroma
            with zipfile.ZipFile(zip_temp_path, "r") as zip_ref:
                zip_ref.extractall(CHROMA_PATH)
            print("ChromaDB archive successfully downloaded and extracted.")
        except Exception as e:
            print(f"Warning: Failed to auto-download ChromaDB: {e}")
        finally:
            if os.path.exists(zip_temp_path):
                try:
                    os.remove(zip_temp_path)
                except Exception:
                    pass


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
    # Ensure vector store exists before initializing client
    ensure_chroma_ready()

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
    """Gemini 2.5 Flash ke liye genai.Client banayega (st.secrets ya .env se GEMINI_API_KEY)."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY nahi mila! Kripya Streamlit Settings -> Secrets me GEMINI_API_KEY set karein."
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


def generate_answer(
    query: str,
    chunks: list,
    user_profile: dict = None,
    evaluated_schemes: list = None
) -> str:
    """
    Retrieved chunks aur optional user profile / eligibility results ke context ke aadhar
    par Gemini 2.5 Flash se grounded, personalized answer banata hai.

    Args:
        query: User ka sawal.
        chunks: retrieve() se mile hue chunks.
        user_profile: Optional user demographic & occupation profile dict.
        evaluated_schemes: Optional deterministically evaluated scheme eligibility results.

    Returns:
        Generated answer string.
    """
    if not chunks and not evaluated_schemes:
        return "Mere paas is baare mein jankari nahi hai."

    # Build context from chunks: [Name | Region | Section]\ntext
    context_blocks = []
    for c in chunks:
        header = f"[{c['name']} | {c['region']} | {c['section']}]"
        context_blocks.append(f"{header}\n{c['text']}")
    context_str = "\n\n".join(context_blocks)

    # Build profile context if available
    profile_context_str = ""
    if user_profile:
        p_lines = [
            f"- Age: {user_profile.get('age', 'Not specified')}",
            f"- Gender: {user_profile.get('gender', 'Not specified')}",
            f"- State of Residence: {user_profile.get('state', 'Not specified')}",
            f"- District: {user_profile.get('district', 'Not specified')}",
            f"- Primary Occupation: {user_profile.get('occupation', 'Not specified')}",
            f"- Annual Family Income: ₹{user_profile.get('annual_family_income', 'Not specified')}",
            f"- Education Level: {user_profile.get('education_level', 'Not specified')}",
            f"- Social Category: {user_profile.get('social_category', 'General')}",
            f"- Disability Status: {user_profile.get('disability_status', 'None')}",
        ]
        add_attr = user_profile.get("additional_attributes") or {}
        if add_attr:
            p_lines.append(f"- Additional Occupation Details: {add_attr}")
        profile_context_str = "USER VERIFIED PROFILE:\n" + "\n".join(p_lines)

    # Build evaluated schemes context if available
    elig_context_str = ""
    if evaluated_schemes:
        scheme_blocks = []
        for s in evaluated_schemes[:5]:
            sb = (
                f"• Scheme: {s['name']} ({s.get('region', 'India')})\n"
                f"  - Level: {s.get('level', 'Central').title()} Scheme\n"
                f"  - Deterministic Eligibility Status: {s['status']}\n"
                f"  - Why Matches Profile: {', '.join(s.get('match_reasons', []))}\n"
                f"  - Verification Required / Missing Info: {', '.join(s.get('missing_criteria', []))}\n"
                f"  - Key Benefits: {s.get('benefits', '')[:200]}\n"
                f"  - Official Link: {s.get('official_link', '')}\n"
                f"  - Required Documents: {', '.join(s.get('required_documents', []))}"
            )
            scheme_blocks.append(sb)
        elig_context_str = "DETERMINISTIC SCHEME ELIGIBILITY EVALUATION RESULTS:\n" + "\n\n".join(scheme_blocks)

    pref_lang = user_profile.get("preferred_language", "en") if user_profile else "en"

    # Multilingual instruction based on user preference
    if pref_lang == "hi":
        lang_instruction = (
            "LANGUAGE (MANDATORY): The user has chosen HINDI (हिंदी) as their preferred language.\n"
            "Respond 100% in natural, fluent, and polite Hindi (Devanagari script). "
            "Keep official scheme names and links in recognizable format."
        )
    elif pref_lang == "hinglish":
        lang_instruction = (
            "LANGUAGE (MANDATORY): The user has chosen HINGLISH as their preferred language.\n"
            "Respond in conversational, friendly Hinglish (Hindi written in Roman English alphabet, e.g. "
            "'Aapke profile ke hisab se yeh schemes aapke liye eligible hain...'). "
            "Keep official scheme names, department names, and links intact."
        )
    else:
        lang_instruction = (
            "LANGUAGE (MANDATORY): The user has chosen ENGLISH as their preferred language.\n"
            "Respond strictly in clear, professional English vocabulary and grammar. "
            "NEVER use Hinglish words when the user preferred language is English."
        )

    system_prompt = (
        "You are Schemate AI, an intelligent multilingual assistant for Indian Government Welfare Schemes.\n"
        f"{lang_instruction}\n\n"
        "GUIDELINES FOR ANSWERING:\n"
        "1. GROUNDING & FIDELITY: Base your answer strictly on the provided Context, User Profile, and Evaluated Scheme Results. Do not invent facts or deadlines.\n"
        "2. ELIGIBILITY HONESTY: Clearly distinguish between 'Potentially Eligible' and 'Needs Verification'. Never claim guaranteed eligibility — always state that official approval is subject to departmental verification.\n"
        "3. EXPLAIN MATCHES: Explicitly mention why a scheme matches the user's profile (e.g. matching state, occupation, income ceiling, or category).\n"
        "4. HIGHLIGHT MISSING INFORMATION: Inform the user what certificates or documents (e.g. income certificate, domicile certificate, marksheet) they must provide to verify eligibility.\n"
        "5. OFFICIAL LINKS: Cite the official application portal link and official government sources for each scheme.\n"
        "6. STRUCTURE: Use clean markdown bullet points: Scheme Name, Status, Why It Matches, Benefits, Verification Needed, and How to Apply."
    )

    full_context_parts = []
    if profile_context_str:
        full_context_parts.append(profile_context_str)
    if elig_context_str:
        full_context_parts.append(elig_context_str)
    if context_str:
        full_context_parts.append(f"DOCUMENT REPOSITORY CONTEXT:\n{context_str}")

    combined_context = "\n\n====================\n\n".join(full_context_parts)

    prompt = (
        f"{system_prompt}\n\n"
        f"Context:\n{combined_context}\n\n"
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


def is_eligibility_or_discovery_query(query: str) -> bool:
    """Check if query is asking about eligibility or scheme recommendations."""
    q_low = query.lower()
    keywords = [
        "eligible", "eligibility", "recommend", "scheme for me", "schemes for me",
        "meri yojana", "kiske liye eligible", "yojana batao", "kon si yojana",
        "kaun si yojana", "apply kar sakta", "apply kar sakti", "scholarship",
        "chhatravritti", "kisan", "farmer", "student", "subsidy", "pension",
        "loan", "benefit", "qualify", "which scheme", "what scheme", "my scheme"
    ]
    return any(k in q_low for k in keywords)


def ask(
    query: str,
    n_results: int = N_RESULTS,
    level_filter: str = None,
    user_profile: dict = None
) -> dict:
    """
    End-to-end RAG pipeline:
    1. Evaluates user profile eligibility if profile is provided and query is relevant
    2. retrieve() se top chunks lata hai from ChromaDB
    3. generate_answer() se grounded response banata hai Gemini 2.5 Flash se
    4. Sources aur links combine karke return karta hai

    Args:
        query: User ka sawal.
        n_results: Deduplicate ke baad kitni schemes return karni hain.
        level_filter: Optional filter ('state', 'central').
        user_profile: Optional user profile dict for personalization.

    Returns:
        dict: {
            "answer": str,
            "sources": [{"name": ..., "region": ..., "section": ..., "score": ...}],
            "chunks": list of retrieved chunk dicts,
            "evaluated_schemes": list of evaluated scheme dicts (if any)
        }
    """
    evaluated_schemes = []

    # If profile exists, evaluate deterministic recommendations
    if user_profile:
        try:
            from eligibility.recommendation_service import get_recommendations_for_profile
            # If user query is an eligibility or scheme discovery question, or generic inquiry:
            evaluated_schemes = get_recommendations_for_profile(
                user_profile,
                top_n=5,
                search_query=query
            )
        except Exception as e:
            print(f"Error evaluating schemes for profile in RAG: {e}")

    # Standard ChromaDB retrieval
    chunks = retrieve(query, n_results=n_results, level_filter=level_filter)

    if not chunks and not evaluated_schemes:
        return {
            "answer": "Mere paas is baare mein jankari nahi hai.",
            "sources": [],
            "chunks": [],
            "evaluated_schemes": [],
        }

    answer = generate_answer(
        query,
        chunks,
        user_profile=user_profile,
        evaluated_schemes=evaluated_schemes
    )

    sources = [
        {
            "name": c["name"],
            "region": c["region"],
            "section": c["section"],
            "score": c["score"],
        }
        for c in chunks
    ]

    # Add evaluated schemes to sources if not already present
    existing_names = {s["name"].lower() for s in sources}
    for es in evaluated_schemes:
        if es["name"].lower() not in existing_names:
            sources.append({
                "name": es["name"],
                "region": es.get("region", "Central"),
                "section": f"Eligibility ({es['status']})",
                "score": round(es.get("score", 80.0) / 100.0, 4),
                "official_link": es.get("official_link"),
            })
            existing_names.add(es["name"].lower())

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
        "evaluated_schemes": evaluated_schemes,
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