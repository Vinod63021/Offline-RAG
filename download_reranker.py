from sentence_transformers import CrossEncoder

print("Downloading BGE Reranker...")

model = CrossEncoder(
    "BAAI/bge-reranker-base"
)

model.save(
    "./models/bge-reranker-base"
)

print("Done.")