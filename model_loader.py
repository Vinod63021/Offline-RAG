import os

from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================
# CONFIG
# ==========================================

MODEL_NAME = "BAAI/bge-base-en-v1.5"

LOCAL_MODEL_PATH = "./models/bge-base"


# ==========================================
# EMBEDDING MODEL
# ==========================================

def get_embedding_model():

    os.makedirs(
        "./models",
        exist_ok=True
    )

    if not os.path.exists(
        LOCAL_MODEL_PATH
    ):

        print(
            "\nEmbedding model not found."
        )

        print(
            "Downloading BGE Base...\n"
        )

        model = SentenceTransformer(
            MODEL_NAME
        )

        model.save(
            LOCAL_MODEL_PATH
        )

        print(
            "\nModel downloaded successfully.\n"
        )

    else:

        print(
            "\nUsing local BGE Base embedding model.\n"
        )

    return HuggingFaceEmbeddings(

        model_name=LOCAL_MODEL_PATH,

        model_kwargs={
            "device": "cpu"
        },

        encode_kwargs={
            "normalize_embeddings": True
        }
    )