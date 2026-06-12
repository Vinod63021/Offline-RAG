import os
from sentence_transformers import SentenceTransformer

# ==========================================
# CONFIG
# ==========================================

MODEL_NAME = "BAAI/bge-base-en-v1.5"

MODELS_DIR = "./models"

LOCAL_PATH = os.path.join(
    MODELS_DIR,
    "bge-base"
)

# ==========================================
# CREATE MODELS DIRECTORY
# ==========================================

os.makedirs(
    MODELS_DIR,
    exist_ok=True
)

# ==========================================
# DOWNLOAD MODEL
# ==========================================

if os.path.exists(LOCAL_PATH):

    print("\nModel already exists.")
    print(f"Location: {LOCAL_PATH}")

else:

    print("\nDownloading BGE Base Model...")
    print(f"Model: {MODEL_NAME}")

    model = SentenceTransformer(
        MODEL_NAME,
        cache_folder=MODELS_DIR
    )

    model.save(LOCAL_PATH)

    print("\nModel downloaded successfully!")

# ==========================================
# VERIFY MODEL
# ==========================================

print("\nVerifying model...")

try:

    model = SentenceTransformer(
        LOCAL_PATH
    )

    embedding = model.encode(
        "This is a test sentence."
    )

    print(
        f"Embedding Dimension: {len(embedding)}"
    )

    print(
        "\nModel verification successful."
    )

except Exception as e:

    print(
        "\nModel verification failed."
    )

    print(e)

print("\nDone.")