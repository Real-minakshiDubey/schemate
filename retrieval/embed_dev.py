import json
import time
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = "data/processed/chunks.json"
MODEL_NAME = "intfloat/multilingual-e5-base"
COLLECTION = "schemes_dev_e5base"

with open(CHUNKS_PATH, encoding="utf-8") as f:
    chunks = json.load(f)

dev = [c for c in chunks if c["split"] == "dev"]
print("Dev chunks to embed:", len(dev))

model = SentenceTransformer(MODEL_NAME)
start = time.time()
vectors = model.encode(
    ["passage: " + c["text"] for c in dev],   # documents ke aage "passage: "
    batch_size=32,
    normalize_embeddings=True,
    show_progress_bar=True,
)
print(f"Embedding took {time.time() - start:.0f}s")

client = chromadb.PersistentClient(path="data/chroma")
try:
    client.delete_collection(COLLECTION)      # dobara chalane par purana hata do
except Exception:
    pass
col = client.create_collection(name=COLLECTION, metadata={"hnsw:space": "cosine"})

BATCH = 500
for i in range(0, len(dev), BATCH):
    part = dev[i:i + BATCH]
    col.add(
        ids=[c["chunk_id"] for c in part],
        documents=[c["text"] for c in part],
        embeddings=vectors[i:i + BATCH].tolist(),
        metadatas=[{
            "scheme_id": c["scheme_id"],
            "name": c["name"],
            "region": c["region"],
            "level": c["level"],
            "section": c["section"],
            "verified": bool(c["verified"]),
        } for c in part],
    )

print("Stored in Chroma:", col.count())