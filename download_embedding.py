import os
from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"
LOCAL_PATH = "./models/bge-small"

os.makedirs("./models", exist_ok=True)

if os.path.exists(LOCAL_PATH):
    print("Model already exists.")
else:
    print("Downloading model...")
    
    model = SentenceTransformer(
        MODEL_NAME,
        cache_folder="./models"
    )

    model.save(LOCAL_PATH)

    print("Model downloaded successfully!")

print("Done.")