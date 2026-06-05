import os

from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings

MODEL_NAME = "BAAI/bge-small-en-v1.5"
LOCAL_MODEL_PATH = "./models/bge-small"


def get_embedding_model():

    os.makedirs("./models", exist_ok=True)

    if not os.path.exists(LOCAL_MODEL_PATH):

        print("\nEmbedding model not found.")
        print("Downloading BGE Small...\n")

        model = SentenceTransformer(MODEL_NAME)

        model.save(LOCAL_MODEL_PATH)

        print("\nModel downloaded successfully.\n")

    else:

        print("\nUsing local embedding model.\n")

    return HuggingFaceEmbeddings(
        model_name=LOCAL_MODEL_PATH
    )