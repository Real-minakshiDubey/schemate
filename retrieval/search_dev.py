import random
import sys
import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-base"
COLLECTION = "schemes_dev_e5base"
N_FETCH = 30      # kitne chunks mangwane hain (dedup ke baad kam bachenge)
N_SHOW = 5        # kitne schemes dikhane hain

USAGE = ('Usage: python retrieval\\search_dev.py "your question" [state|central|unknown]\n'
         '   or: python retrieval\\search_dev.py --names')
if len(sys.argv) < 2:
    raise SystemExit(USAGE)

col = chromadb.PersistentClient(path="data/chroma").get_collection(COLLECTION)

if sys.argv[1] == "--names":
    metas = col.get(include=["metadatas"])["metadatas"]
    names = sorted({m["name"] for m in metas})
    print("Schemes in dev set:", len(names))
    for n in random.sample(names, min(25, len(names))):
        print("-", n)
    raise SystemExit

query = sys.argv[1]
level = sys.argv[2] if len(sys.argv) > 2 else None

model = SentenceTransformer(MODEL_NAME)
q_vec = model.encode(["query: " + query], normalize_embeddings=True).tolist()

kwargs = dict(query_embeddings=q_vec, n_results=N_FETCH,
              include=["documents", "metadatas", "distances"])
if level:
    kwargs["where"] = {"level": level}
res = col.query(**kwargs)

docs = res["documents"][0]
metas = res["metadatas"][0]
dists = res["distances"][0]

print("QUERY:", query, "| filter:", level)
print("Chunks returned:", len(docs))

seen = set()
shown = 0
for doc, meta, dist in zip(docs, metas, dists):
    if meta["scheme_id"] in seen:
        continue                       # ek scheme ek hi baar (uska best chunk)
    seen.add(meta["scheme_id"])
    shown += 1
    print(f"\n#{shown} score={1 - dist:.3f} | {meta['name'][:70]}")
    print(f"   best section={meta['section']} | region={meta['region'][:30]} | level={meta['level']}")
    print("   ", doc.split("\n", 1)[-1][:160].replace("\n", " "))
    if shown == N_SHOW:
        break

print("\nUnique schemes in all", len(docs), "chunks:", len({m["scheme_id"] for m in metas}))