"""
eval/run_eval.py
Retrieval quality evaluation across English, Hindi, and Hinglish.

Measures:
  - Hit@1: Kya sahi scheme rank 1 par aayi?
  - Hit@5: Kya sahi scheme top 5 mein aayi?
  - MRR: Mean Reciprocal Rank (1 / rank)

Results terminal mein clean table format mein print hote hain
aur eval/results.json mein save hote hain.
"""

import argparse
import csv
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import chromadb
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------------------------
# Default Constants
# ---------------------------------------------------------------------------
MODEL_NAME = "intfloat/multilingual-e5-base"
CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "schemes_dev_e5base"
SECTIONS_PATH = "data/processed/schemes_sections.json"
QUESTIONS_PATH = "eval/questions.csv"
OUTPUT_PATH = "eval/results.json"
N_FETCH = 30  # kitne chunks mangaane hain (dedup ke baad rank calculate hogi)


def resolve_path(rel_or_abs_path: str) -> Path:
    """
    Path resolve karo - pehle current working dir se check karo,
    agar wahan nahi mile toh project root se relative check karo.
    """
    p = Path(rel_or_abs_path)
    if p.exists():
        return p
    # Project root se relative try karo (eval/ se script run hone par helpful hai)
    root = Path(__file__).resolve().parent.parent
    candidate = root / rel_or_abs_path
    if candidate.exists():
        return candidate
    return p


def norm(s: str) -> str:
    """
    Normalise scheme name / string:
    - Lowercase karo
    - Unicode dashes (en-dash, em-dash) aur hyphen replace karo
    - Whitespace collapse karo (multiple spaces -> single space)
    """
    if not s:
        return ""
    # Unicode dashes aur regular hyphen ko space se replace karo
    s = s.lower().replace("-", " ").replace("–", " ").replace("—", " ")
    return re.sub(r"\s+", " ", s).strip()


def load_dev_schemes(sections_path: Path) -> List[Dict[str, Any]]:
    """
    data/processed/schemes_sections.json load karo aur split == 'dev' wale records filter karo.
    """
    if not sections_path.exists():
        raise FileNotFoundError(f"Schemes sections file nahi mili: {sections_path}")

    print(f"Loading dev schemes from: {sections_path}")
    with open(sections_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    dev_records = [r for r in records if r.get("split") == "dev"]
    print(f"Total records: {len(records)} | Dev records: {len(dev_records)}")
    return dev_records


def load_questions(questions_path: Path) -> List[Dict[str, str]]:
    """
    eval/questions.csv load karo.
    Columns: qid, language, question, correct_name
    """
    if not questions_path.exists():
        raise FileNotFoundError(f"Questions CSV file nahi mili: {questions_path}")

    print(f"Loading questions from: {questions_path}")
    with open(questions_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Total questions loaded: {len(rows)}")
    return rows


def resolve_names_to_schemes(
    unique_names: List[str], dev_records: List[Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    """
    Unique correct_name ko dev scheme records se map karo.
    Rule: norm(correct_name) should be a substring of norm(record['name']).
    Unresolved ya ambiguous names ke liye warning print karo.
    """
    resolved: Dict[str, Dict[str, Any]] = {}
    unresolved: List[str] = []

    for name in sorted(unique_names):
        norm_target = norm(name)
        hits = [r for r in dev_records if norm_target in norm(r.get("name", ""))]

        if len(hits) == 1:
            resolved[name] = hits[0]
        elif len(hits) > 1:
            # Agar multiple dev schemes match ho jayein (jaise 'Jeevan Jyoti')
            print(f"Warning: Multiple ({len(hits)}) schemes matched for '{name}':")
            for h in hits:
                print(f"   - ID: {h['id']} | Name: {h['name']} | Region: {h.get('region', 'N/A')}")

            # Jeevan Jyoti case: Central life insurance scheme (PMJJBY) intended hai
            bima_candidates = [
                h for h in hits
                if "bima" in norm(h.get("name", "")) or "pradhan mantri" in norm(h.get("name", ""))
            ]
            if bima_candidates:
                resolved[name] = bima_candidates[0]
                print(f"   -> Disambiguated '{name}' to ID {bima_candidates[0]['id']}: {bima_candidates[0]['name']}")
            else:
                resolved[name] = hits[0]
                print(f"   -> Defaulted to first match ID {hits[0]['id']}: {hits[0]['name']}")
        else:
            print(f"Warning: Unresolved scheme name: '{name}' (koi dev scheme match nahi hui)")
            unresolved.append(name)

    print(f"Resolved {len(resolved)} / {len(unique_names)} unique scheme names successfully.")
    if unresolved:
        print(f"Unresolved schemes ({len(unresolved)}): {unresolved}")

    return resolved


def evaluate_retrieval(
    questions: List[Dict[str, str]],
    resolved_schemes: Dict[str, Dict[str, Any]],
    model_name: str = MODEL_NAME,
    chroma_path: str = CHROMA_PATH,
    collection_name: str = COLLECTION_NAME,
    n_fetch: int = N_FETCH,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Har question par retrieval run karo aur metrics calculate karo.
    """
    chroma_dir = resolve_path(chroma_path)
    if not chroma_dir.exists():
        raise FileNotFoundError(f"ChromaDB path nahi mila: {chroma_dir}")

    print(f"\nConnecting to ChromaDB at: {chroma_dir}")
    client = chromadb.PersistentClient(path=str(chroma_dir))
    try:
        col = client.get_collection(collection_name)
    except Exception as e:
        raise RuntimeError(
            f"Collection '{collection_name}' ChromaDB mein nahi mili: {e}. "
            "Pehle 'python retrieval/embed_dev.py' chalayein."
        )

    print(f"Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)

    per_question_results: List[Dict[str, Any]] = []

    print(f"\nRunning retrieval evaluation on {len(questions)} queries...")
    for idx, row in enumerate(questions, 1):
        qid = row.get("qid", f"q{idx:02d}")
        lang = row.get("language", "unknown").strip().lower()
        question = row.get("question", "").strip()
        correct_name = row.get("correct_name", "").strip()

        # Scheme resolution check karo
        scheme_info = resolved_schemes.get(correct_name)
        target_scheme_id = str(scheme_info["id"]).strip() if scheme_info else None
        target_scheme_name = scheme_info["name"] if scheme_info else correct_name

        if not question:
            print(f"Warning: Empty question for {qid}")
            per_question_results.append({
                "qid": qid,
                "language": lang,
                "question": question,
                "correct_name": correct_name,
                "scheme_id": target_scheme_id,
                "scheme_name": target_scheme_name,
                "rank": None,
                "hit_at_1": False,
                "hit_at_5": False,
                "mrr": 0.0,
            })
            continue

        # E5 model ke liye query prefix: "query: "
        query_text = "query: " + question
        q_vec = model.encode([query_text], normalize_embeddings=True).tolist()

        # ChromaDB se top 30 chunks query karo
        res = col.query(
            query_embeddings=q_vec,
            n_results=n_fetch,
            include=["metadatas"]
        )

        metadatas = res.get("metadatas", [[]])[0]

        # Scheme-level deduplication: ek scheme ek hi baar (uska highest ranking chunk)
        # Order maintain rakhna hai (best first)
        deduped_scheme_ids: List[str] = []
        for meta in metadatas:
            sid = str(meta.get("scheme_id", "")).strip()
            if sid and sid not in deduped_scheme_ids:
                deduped_scheme_ids.append(sid)

        # Target scheme ki rank dhundho (1-based index)
        rank: Optional[int] = None
        if target_scheme_id and target_scheme_id in deduped_scheme_ids:
            rank = deduped_scheme_ids.index(target_scheme_id) + 1

        # Metrics per question
        hit_1 = bool(rank == 1) if rank is not None else False
        hit_5 = bool(rank is not None and rank <= 5)
        mrr = (1.0 / rank) if rank is not None else 0.0

        per_question_results.append({
            "qid": qid,
            "language": lang,
            "question": question,
            "correct_name": correct_name,
            "scheme_id": target_scheme_id,
            "scheme_name": target_scheme_name,
            "rank": rank,
            "hit_at_1": hit_1,
            "hit_at_5": hit_5,
            "mrr": mrr,
        })

    # Summary metrics aggregate karo
    summary: Dict[str, Any] = {}
    languages = ["en", "hi", "hinglish"]

    # Agar koi aur language ho CSV mein toh usko bhi shamil karo
    detected_langs = sorted({q["language"] for q in per_question_results})
    for l in detected_langs:
        if l not in languages:
            languages.append(l)

    for l in languages:
        sub = [q for q in per_question_results if q["language"] == l]
        n = len(sub)
        if n > 0:
            hit1_rate = sum(1 for q in sub if q["hit_at_1"]) / n
            hit5_rate = sum(1 for q in sub if q["hit_at_5"]) / n
            mean_mrr = sum(q["mrr"] for q in sub) / n
            summary[l] = {
                "n": n,
                "hit_at_1": round(hit1_rate, 4),
                "hit_at_5": round(hit5_rate, 4),
                "mrr": round(mean_mrr, 4),
            }
        else:
            summary[l] = {"n": 0, "hit_at_1": 0.0, "hit_at_5": 0.0, "mrr": 0.0}

    total_n = len(per_question_results)
    if total_n > 0:
        summary["ALL"] = {
            "n": total_n,
            "hit_at_1": round(sum(1 for q in per_question_results if q["hit_at_1"]) / total_n, 4),
            "hit_at_5": round(sum(1 for q in per_question_results if q["hit_at_5"]) / total_n, 4),
            "mrr": round(sum(q["mrr"] for q in per_question_results) / total_n, 4),
        }
    else:
        summary["ALL"] = {"n": 0, "hit_at_1": 0.0, "hit_at_5": 0.0, "mrr": 0.0}

    return per_question_results, summary


def print_results(per_question: List[Dict[str, Any]], summary: Dict[str, Any]) -> None:
    """
    Per-question details aur summary table clean f-string format mein print karo.
    """
    # 1. Per-question details table
    print("\n" + "=" * 92)
    print(" " * 32 + "PER-QUESTION DETAILS")
    print("=" * 92)
    print(f"{'QID':<12} | {'Lang':<10} | {'Rank':<10} | {'Scheme'}")
    print("-" * 92)
    for q in per_question:
        rank_str = str(q["rank"]) if q["rank"] is not None else ">30"
        scheme_display = q["scheme_name"] or q["correct_name"]
        # Trim scheme display if too long
        if len(scheme_display) > 60:
            scheme_display = scheme_display[:57] + "..."
        print(f"{q['qid']:<12} | {q['language']:<10} | {rank_str:<10} | {scheme_display}")
    print("=" * 92)

    # 2. Summary table
    print("\n" + "=" * 54)
    print(" " * 13 + "RETRIEVAL EVALUATION SUMMARY")
    print("=" * 54)
    print(f"{'Language':<12} | {'N':>4} | {'Hit@1':>8} | {'Hit@5':>8} | {'MRR':>8}")
    print("-" * 54)
    for lang, metrics in summary.items():
        if lang == "ALL":
            print("-" * 54)
        n = metrics["n"]
        h1 = metrics["hit_at_1"]
        h5 = metrics["hit_at_5"]
        mrr = metrics["mrr"]
        print(f"{lang:<12} | {n:>4} | {h1:>8.3f} | {h5:>8.3f} | {mrr:>8.3f}")
    print("=" * 54 + "\n")


def save_results(
    output_path: Path, per_question: List[Dict[str, Any]], summary: Dict[str, Any]
) -> None:
    """
    Full results ko eval/results.json mein save karo.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_data = {
        "summary": summary,
        "per_question": per_question,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=2, ensure_ascii=False)
    print(f"Results successfully saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate retrieval quality across English, Hindi, and Hinglish queries."
    )
    parser.add_argument(
        "--questions",
        default=QUESTIONS_PATH,
        help=f"Path to questions CSV file (default: {QUESTIONS_PATH})",
    )
    parser.add_argument(
        "--sections",
        default=SECTIONS_PATH,
        help=f"Path to schemes sections JSON file (default: {SECTIONS_PATH})",
    )
    parser.add_argument(
        "--chroma",
        default=CHROMA_PATH,
        help=f"Path to ChromaDB persistent directory (default: {CHROMA_PATH})",
    )
    parser.add_argument(
        "--collection",
        default=COLLECTION_NAME,
        help=f"ChromaDB collection name (default: {COLLECTION_NAME})",
    )
    parser.add_argument(
        "--model",
        default=MODEL_NAME,
        help=f"SentenceTransformer model name (default: {MODEL_NAME})",
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=N_FETCH,
        help=f"Number of chunks to fetch per query (default: {N_FETCH})",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_PATH,
        help=f"Path to save results JSON (default: {OUTPUT_PATH})",
    )
    args = parser.parse_args()

    # Step 1: Load data
    sections_file = resolve_path(args.sections)
    questions_file = resolve_path(args.questions)
    dev_records = load_dev_schemes(sections_file)
    questions = load_questions(questions_file)

    # Step 2: Resolve scheme names to IDs
    unique_names = list({row["correct_name"].strip() for row in questions if row.get("correct_name")})
    resolved_schemes = resolve_names_to_schemes(unique_names, dev_records)

    # Step 3 & 4: Run retrieval & compute metrics
    per_question, summary = evaluate_retrieval(
        questions=questions,
        resolved_schemes=resolved_schemes,
        model_name=args.model,
        chroma_path=args.chroma,
        collection_name=args.collection,
        n_fetch=args.top_k,
    )

    # Step 5: Output (terminal print & JSON save)
    print_results(per_question, summary)
    output_file = Path(args.output)
    save_results(output_file, per_question, summary)


if __name__ == "__main__":
    main()
