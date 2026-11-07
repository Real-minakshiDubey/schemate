import json
import os
import sys
import time
import chromadb
from sentence_transformers import SentenceTransformer

# Paths & Collection config
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "chunks.json")
CHROMA_PATH = os.path.join(PROJECT_ROOT, "data", "chroma")
MODEL_NAME = "intfloat/multilingual-e5-base"
COLLECTION_NAME = "schemes_full_e5base"

# Ensure UTF-8 output on Windows terminal
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

print("=== SchemeSense: Full Dataset Embedding Pipeline ===")
print(f"Loading chunks from: {CHUNKS_PATH}")
with open(CHUNKS_PATH, encoding="utf-8") as f:
    chunks = json.load(f)

total_chunks = len(chunks)
unique_schemes = len({c["scheme_id"] for c in chunks})
print(f"Loaded {total_chunks:,} chunks across {unique_schemes:,} unique government schemes.")

print(f"\nConnecting to ChromaDB at: {CHROMA_PATH}")
client = chromadb.PersistentClient(path=CHROMA_PATH)
col = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

existing_count = col.count()
print(f"Collection '{COLLECTION_NAME}' currently has {existing_count:,} stored chunks.")

# Resume support: Find which chunk IDs are already indexed
if existing_count > 0:
    print("Checking already indexed chunks to support incremental/resumable embedding...")
    existing_ids = set(col.get(include=[])["ids"])
    chunks_to_embed = [c for c in chunks if c["chunk_id"] not in existing_ids]
    print(f"Already indexed: {len(existing_ids):,} | Remaining to embed: {len(chunks_to_embed):,}")
else:
    chunks_to_embed = chunks

if not chunks_to_embed:
    print("\nAll 19,481 chunks are already embedded into ChromaDB! Nothing to do.")
    sys.exit(0)

print(f"\nLoading embedding model: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)

BATCH_SIZE = 256  # Batched embedding & ChromaDB insert
start_time = time.time()
n_remaining = len(chunks_to_embed)

print(f"Starting batched embedding and insertion of {n_remaining:,} chunks...\n")

for i in range(0, n_remaining, BATCH_SIZE):
    batch = chunks_to_embed[i:i + BATCH_SIZE]
    batch_texts = ["passage: " + c["text"] for c in batch]
    
    # 1. Embed batch
    t0 = time.time()
    vectors = model.encode(
        batch_texts,
        batch_size=64,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    
    # 2. Add to ChromaDB
    col.add(
        ids=[c["chunk_id"] for c in batch],
        documents=[c["text"] for c in batch],
        embeddings=vectors.tolist(),
        metadatas=[{
            "scheme_id": str(c["scheme_id"]),
            "name": str(c.get("name", "")),
            "region": str(c.get("region", "")),
            "level": str(c.get("level", "unknown")),
            "section": str(c.get("section", "details")),
            "verified": bool(c.get("verified", False)),
        } for c in batch],
    )
    
    elapsed = time.time() - start_time
    done_so_far = i + len(batch)
    rate = done_so_far / elapsed if elapsed > 0 else 0
    eta_sec = (n_remaining - done_so_far) / rate if rate > 0 else 0
    
    print(
        f"Progress: [{done_so_far:,}/{n_remaining:,}] chunks "
        f"({done_so_far/n_remaining:.1%}) | "
        f"Speed: {rate:.1f} chunks/sec | "
        f"ETA: {int(eta_sec//60)}m {int(eta_sec%60)}s | "
        f"Stored: {col.count():,}"
    )

print("\n" + "="*60)
print(f"SUCCESS! Embedded all {col.count():,} chunks from {unique_schemes:,} schemes.")
print(f"Total time elapsed: {int((time.time() - start_time)//60)}m {int((time.time() - start_time)%60)}s")
print("="*60)
