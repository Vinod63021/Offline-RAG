import os
import requests

from langchain_community.vectorstores import FAISS

from model_loader import get_embedding_model
from reranker import rerank_documents


# ==========================================
# CONFIG
# ==========================================

VECTORSTORE_PATH = r"C:\Users\vinod\Downloads\offline-rag\vectorstore"

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "qwen3:8b"

TOP_K_RETRIEVAL = 20

TOP_K_RERANK = 5

MAX_CONTEXT_LENGTH = 12000


# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

print("Loading embedding model...\n")

embeddings = get_embedding_model()


# ==========================================
# LOAD VECTOR DATABASE
# ==========================================

print("Loading vector database...\n")

db = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)


# ==========================================
# CHECK OLLAMA
# ==========================================

print("Checking Ollama API...\n")

try:

    response = requests.get(
        "http://localhost:11434/api/tags",
        timeout=5
    )

    response.raise_for_status()

except Exception as e:

    print("\nERROR: Ollama is not running.\n")

    print(e)

    exit()


# ==========================================
# LLM CALL
# ==========================================

def ask_llm(prompt):

    response = requests.post(

        OLLAMA_URL,

        json={

            "model": MODEL_NAME,

            "prompt": prompt,

            "stream": False
        },

        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]


# ==========================================
# RETRIEVAL + RERANKING
# ==========================================

def retrieve_context(question):

    print(
        "\nSearching Vector Database..."
    )

    retrieved_docs = db.similarity_search(

        question,

        k=TOP_K_RETRIEVAL
    )

    print(
        f"Retrieved {len(retrieved_docs)} chunks"
    )

    print(
        "Running BGE Reranker..."
    )

    reranked_docs = rerank_documents(

        question,

        retrieved_docs,

        top_k=TOP_K_RERANK
    )

    print(
        f"Selected Top {len(reranked_docs)} Chunks"
    )

    context_parts = []

    sources = set()

    current_length = 0

    for doc in reranked_docs:

        text = doc.page_content.strip()

        if not text:

            continue

        if (

            current_length
            + len(text)

            > MAX_CONTEXT_LENGTH

        ):

            break

        context_parts.append(
            text
        )

        current_length += len(
            text
        )

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        sources.add(
            os.path.basename(source)
        )

    context = "\n\n".join(
        context_parts
    )

    return (
        context,
        sources
    )


# ==========================================
# PROMPT BUILDER
# ==========================================

def build_prompt(
    context,
    question
):

    return f"""
You are an enterprise knowledge assistant.

STRICT RULES:

1. Use ONLY the supplied context.
2. Never invent information.
3. Never guess.
4. If the answer is not present in the context reply exactly:

I don't know based on the provided documents.

5. Give concise and accurate answers.
6. Summarize when appropriate.
7. Use bullet points when useful.

CONTEXT:

{context}

QUESTION:

{question}

ANSWER:
"""


# ==========================================
# MAIN
# ==========================================

print("\n===================================")
print("Enterprise Offline RAG Ready")
print("FAISS + BGE Base + BGE Reranker")
print("===================================\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":

        break

    try:

        context, sources = retrieve_context(
            question
        )

        if not context:

            print(
                "\nAssistant:"
            )

            print(
                "I don't know based on the provided documents.\n"
            )

            continue

        prompt = build_prompt(

            context,

            question
        )

        response = ask_llm(
            prompt
        )

        print("\n===================================")
        print("Assistant")
        print("===================================\n")

        print(response)

        print("\n-----------------------------------")
        print("Sources")
        print("-----------------------------------")

        for source in sorted(
            sources
        ):

            print(
                f"- {source}"
            )

        print()

    except Exception as e:

        print("\nERROR:\n")

        print(e)

        print()