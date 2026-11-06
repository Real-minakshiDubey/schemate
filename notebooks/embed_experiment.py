from sentence_transformers import SentenceTransformer

MODEL = "intfloat/multilingual-e5-base"
model = SentenceTransformer(MODEL)

sentences = [
    "farmer financial aid",
    "किसान को आर्थिक सहायता",
    "kisan ko paisa kaise milega",
    "scholarship for students",
    "mujhe scholarship chahiye",
    "विद्यार्थियों के लिए छात्रवृत्ति",
    "how to cook rice",
    "बारिश का मौसम",
]

# e5 model ko har text ke aage "query: " lagana padta hai
embeddings = model.encode(["query: " + s for s in sentences],
                          normalize_embeddings=True)

print("Embedding shape:", embeddings.shape)
sim = embeddings @ embeddings.T

print("\nSimilarity matrix (1.0 = bilkul same):")
for i, s in enumerate(sentences):
    row = " ".join(f"{sim[i][j]:.2f}" for j in range(len(sentences)))
    print(f"{i}: {row}   <- {s}")