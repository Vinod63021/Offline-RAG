from sentence_transformers import CrossEncoder

RERANKER_PATH = "./models/bge-reranker-base"

print("Loading BGE Reranker...")

reranker = CrossEncoder(
    RERANKER_PATH
)

print("BGE Reranker Loaded")


def rerank_documents(
    query,
    documents,
    top_k=5
):

    pairs = [

        [query, doc.page_content]

        for doc in documents
    ]

    scores = reranker.predict(
        pairs
    )

    ranked = list(
        zip(
            documents,
            scores
        )
    )

    ranked.sort(

        key=lambda x: x[1],

        reverse=True
    )

    return [

        doc

        for doc, score

        in ranked[:top_k]
    ]