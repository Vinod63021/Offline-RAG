import os

from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from model_loader import get_embedding_model


DOCUMENTS_PATH = r"C:\Users\vinod\Downloads\offline-rag\documents"
VECTORSTORE_PATH = r"C:\Users\vinod\Downloads\offline-rag\vectorstore"

print("Loading PDFs...")

documents = []

for file in os.listdir(DOCUMENTS_PATH):

    if file.endswith(".pdf"):

        pdf_path = os.path.join(DOCUMENTS_PATH, file)

        loader = PyPDFLoader(pdf_path)

        documents.extend(loader.load())

print(f"Loaded {len(documents)} pages")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

embeddings = get_embedding_model()

print("Creating FAISS database...")

db = FAISS.from_documents(
    chunks,
    embeddings
)

os.makedirs(VECTORSTORE_PATH, exist_ok=True)

db.save_local(VECTORSTORE_PATH)

print("\nVector database created.\n")