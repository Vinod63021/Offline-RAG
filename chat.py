from langchain_community.vectorstores import FAISS
import requests

from model_loader import get_embedding_model

VECTORSTORE_PATH = r"C:\Users\vinod\Downloads\offline-rag\vectorstore"

print("Loading embedding model...")

embeddings = get_embedding_model()

print("Loading vector database...")

db = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

print("Checking Ollama API...")

try:
    response = requests.get(
        "http://localhost:11434/api/tags",
        timeout=5
    )

    if response.status_code != 200:
        raise Exception("Ollama server not reachable")

except Exception as e:
    print("\nERROR: Ollama is not running")
    print(e)
    exit()

print("\nOffline RAG Ready")
print("Type exit to quit\n")


def ask_llm(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:8b",
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]


while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    try:

        docs = db.similarity_search(
            question,
            k=2
        )

        context = "\n\n".join(
            doc.page_content[:1000]
            for doc in docs
        )

        prompt = f"""
You are a helpful assistant.

Use ONLY the information present in the context.

If the answer is not available in the context,
reply exactly:

I don't know based on the provided documents.

Context:
{context}

Question:
{question}

Answer:
"""

        response = ask_llm(prompt)

        print("\nAssistant:")
        print(response)
        print()

    except Exception as e:

        print("\nERROR:")
        print(e)
        print()