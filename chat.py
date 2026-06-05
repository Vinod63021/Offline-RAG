from langchain_community.vectorstores import FAISS

from langchain_ollama import OllamaLLM

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

print("Checking Ollama...")

llm = OllamaLLM(
    model="qwen3:8b"
)

print("\nOffline RAG Ready")
print("Type exit to quit\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    docs = db.similarity_search(
        question,
        k=4
    )

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = f"""
You are a helpful assistant.

Answer ONLY using the context.

If the answer is not present in the context,
say you don't know.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    print("\nAssistant:")
    print(response)
    print()