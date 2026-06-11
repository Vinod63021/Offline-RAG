import os
import shutil
import time
import json

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from model_loader import get_embedding_model
from document_loader import load_all_documents


# ==========================================
# CONFIG
# ==========================================

DATA_PATH = r"C:\Users\vinod\Downloads\offline-rag\data"

VECTORSTORE_PATH = r"C:\Users\vinod\Downloads\offline-rag\vectorstore"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# ==========================================
# TIMER
# ==========================================

start_time = time.time()


# ==========================================
# LOAD DOCUMENTS
# ==========================================

print("\n===================================")
print("Loading Documents...")
print("===================================\n")

documents = load_all_documents(DATA_PATH)

print(f"\nTotal documents loaded: {len(documents)}")

if not documents:

    print("\nNo documents found.")
    print(f"Checked folder: {DATA_PATH}")

    exit()


# ==========================================
# DOCUMENT STATISTICS
# ==========================================

print("\n===================================")
print("Document Statistics")
print("===================================\n")

stats = {}

for doc in documents:

    doc_type = doc.metadata.get(
        "type",
        "unknown"
    )

    stats[doc_type] = (
        stats.get(doc_type, 0) + 1
    )

for key, value in stats.items():

    print(
        f"{key:<15} : {value}"
    )


# ==========================================
# CHUNKING
# ==========================================

print("\n===================================")
print("Chunking Documents...")
print("===================================\n")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)

chunks = splitter.split_documents(
    documents
)

# Remove empty chunks
chunks = [
    chunk
    for chunk in chunks
    if chunk.page_content.strip()
]

# Remove duplicate chunks
seen = set()
unique_chunks = []

for chunk in chunks:

    content = chunk.page_content.strip()

    if content not in seen:

        seen.add(content)

        unique_chunks.append(chunk)

chunks = unique_chunks

print(f"Created {len(chunks)} chunks")

if len(chunks) == 0:

    print("\nNo valid chunks created.")

    exit()


# ==========================================
# EMBEDDINGS
# ==========================================

print("\n===================================")
print("Loading Embedding Model...")
print("===================================\n")

try:

    embeddings = get_embedding_model()

except Exception as e:

    print(
        "Embedding model failed."
    )

    print(e)

    exit()


# ==========================================
# RESET VECTORSTORE
# ==========================================

if os.path.exists(
    VECTORSTORE_PATH
):

    print(
        "\nRemoving old vector database..."
    )

    shutil.rmtree(
        VECTORSTORE_PATH
    )


# ==========================================
# CREATE FAISS
# ==========================================

print("\n===================================")
print("Creating FAISS Database...")
print("===================================\n")

try:

    db = FAISS.from_documents(
        chunks,
        embeddings
    )

except Exception as e:

    print(
        "FAISS creation failed."
    )

    print(e)

    exit()


# ==========================================
# SAVE VECTORSTORE
# ==========================================

os.makedirs(
    VECTORSTORE_PATH,
    exist_ok=True
)

db.save_local(
    VECTORSTORE_PATH
)

print(
    "\nVector database saved."
)


# ==========================================
# SAVE INGESTION INFO
# ==========================================

metadata = {

    "documents_loaded": len(
        documents
    ),

    "chunks_created": len(
        chunks
    ),

    "document_types": stats,

    "created_at": time.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
}

with open(

    os.path.join(
        VECTORSTORE_PATH,
        "metadata.json"
    ),

    "w",

    encoding="utf-8"

) as f:

    json.dump(
        metadata,
        f,
        indent=4
    )


# ==========================================
# VERIFY VECTORSTORE
# ==========================================

try:

    test_db = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print(
        "\nVector database verification successful."
    )

except Exception as e:

    print(
        "\nVector database verification failed."
    )

    print(e)


# ==========================================
# COMPLETE
# ==========================================

elapsed = round(
    time.time() - start_time,
    2
)

print("\n===================================")
print("INGESTION COMPLETE")
print("===================================")

print(
    f"\nDocuments Loaded : {len(documents)}"
)

print(
    f"Chunks Created   : {len(chunks)}"
)

print(
    f"Vector DB Saved  : {VECTORSTORE_PATH}"
)

print(
    f"Ingestion Time   : {elapsed} sec"
)

print("\nReady for chat.py\n")