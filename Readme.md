# VaultRAG

**VaultRAG** is a fully private, offline Retrieval-Augmented Generation (RAG) system that allows you to chat with your PDF documents using local AI models.

Unlike cloud-based AI systems, VaultRAG keeps all data on your machine. Documents are processed locally, stored in a local vector database, and queried through a local Large Language Model (LLM).

No OpenAI API.
No Gemini API.
No Claude API.
No external vector database.

Everything stays on your machine.

---

# Features

* Fully offline AI assistant
* PDF document ingestion
* Local embedding generation
* Semantic search using FAISS
* Local LLM inference using Ollama
* Automatic embedding model management
* Private and secure architecture
* Zero API costs
* Easily expandable to OCR, databases, and enterprise systems

---

# Architecture

```text
                    PDF Documents
                           │
                           ▼
                  Text Extraction
                           │
                           ▼
                       Chunking
                           │
                           ▼
                Embedding Model (BGE)
                           │
                           ▼
                 FAISS Vector Database
                           │
                           ▼
                      Retriever
                           │
                           ▼
                Retrieved Context
                           │
                           ▼
                 Qwen3 via Ollama
                           │
                           ▼
                     Final Answer
```

---

# Tech Stack

| Component       | Technology             |
| --------------- | ---------------------- |
| Language        | Python                 |
| LLM Runtime     | Ollama                 |
| LLM             | Qwen3 8B               |
| Embeddings      | BAAI/bge-small-en-v1.5 |
| Vector Database | FAISS                  |
| Framework       | LangChain              |
| PDF Extraction  | PyPDF                  |
| OS              | Windows/Linux          |

---

# Folder Structure

```text
offline-rag/
│
├── documents/
│   ├── attendance.pdf
│   ├── rules.pdf
│   └── notes.pdf
│
├── models/
│   └── bge-small/
│
├── vectorstore/
│   ├── index.faiss
│   └── index.pkl
│
├── model_loader.py
├── ingest.py
├── chat.py
├── requirements.txt
├── README.md
│
└── venv/
```

---

# Hardware Requirements

Minimum:

```text
RAM: 16 GB
CPU: Modern Quad-Core
GPU: Optional
```

Recommended:

```text
RAM: 16 GB+
GPU: RTX 3050 or higher
Storage: 20 GB+
```

Tested Target:

```text
Windows 11
16 GB RAM
RTX 3050
```

---

# Installation

## Step 1 - Clone Repository

```bash
git clone https://github.com/Vinod63021/Offline-RAG.git

cd Offline-RAG
```

---

## Step 2 - Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux:

```bash
source venv/bin/activate
```

---

## Step 3 - Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

Example requirements.txt

```text
langchain
langchain-community
langchain-ollama

langchain-huggingface

sentence-transformers

faiss-cpu

pypdf

torch
transformers
accelerate

numpy
tqdm
```

---

# Installing Ollama

Download:

https://ollama.com

Verify:

```bash
ollama --version
```

---

# Downloading Qwen3

Download model:

```bash
ollama pull qwen3:8b
```

Test:

```bash
ollama run qwen3:8b
```

Example:

```text
What is AI?
```

If it responds, the local LLM is working.

---

# Embedding Model

VaultRAG uses:

```text
BAAI/bge-small-en-v1.5
```

Purpose:

```text
Convert text into vectors
```

Used in:

```text
ingest.py
chat.py
```

---

# Automatic Model Download

The project contains:

```text
model_loader.py
```

Workflow:

```text
Check Local Model
        │
        ▼
   Exists?
   │     │
 YES     NO
  │       │
  ▼       ▼
 Load   Download
 Model   Model
  │       │
  └──► Load
```

First run:

```text
Downloads model
Stores model locally
```

Later runs:

```text
Loads local model
No download required
```

Storage:

```text
models/
└── bge-small/
```

---

# Adding Documents

Place PDFs inside:

```text
documents/
```

Example:

```text
documents/
├── attendance.pdf
├── rules.pdf
└── notes.pdf
```

---

# Building the Knowledge Base

Run:

```bash
python ingest.py
```

---

# What ingest.py Does

## Step 1

Load PDFs

```text
documents/
```

↓

```text
PyPDFLoader
```

---

## Step 2

Extract text

Example:

```text
Students must maintain
75% attendance.
```

---

## Step 3

Chunk documents

Example:

```text
Chunk 1
Chunk 2
Chunk 3
```

Current settings:

```python
chunk_size = 1000
chunk_overlap = 200
```

---

## Step 4

Generate embeddings

```text
Chunk
 ↓
BGE Model
 ↓
Vector
```

Example:

```text
[0.23, 0.44, 0.91, ...]
```

---

## Step 5

Store vectors

```text
FAISS
```

Output:

```text
vectorstore/
├── index.faiss
└── index.pkl
```

---

# Running the Assistant

Run:

```bash
python chat.py
```

---

# What chat.py Does

User asks:

```text
What is the attendance requirement?
```

---

## Step 1

Question converted into embedding

```text
Question
 ↓
Vector
```

---

## Step 2

Search FAISS

```text
Question Vector
 ↓
Similarity Search
```

---

## Step 3

Retrieve relevant chunks

Example:

```text
Students must maintain
75% attendance.
```

---

## Step 4

Build prompt

```text
Context:
Students must maintain
75% attendance.

Question:
What is attendance requirement?
```

---

## Step 5

Send to Qwen3

```text
Ollama
 ↓
Qwen3
```

---

## Step 6

Generate answer

```text
The minimum attendance
requirement is 75%.
```

---

# Complete Data Flow

## Ingestion Phase

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS
```

---

## Query Phase

```text
Question
 ↓
Embeddings
 ↓
FAISS Search
 ↓
Relevant Chunks
 ↓
Qwen3
 ↓
Answer
```

---

# Understanding Each Component

## PDFs

Knowledge source.

Contains information.

---

## BGE Small

Embedding model.

Converts:

```text
Text
```

into

```text
Vectors
```

---

## FAISS

Vector search engine.

Stores embeddings.

Performs semantic search.

---

## Ollama

Runs AI models locally.

---

## Qwen3

The actual AI model.

Responsible for:

* Understanding context
* Understanding questions
* Generating answers

---

# Security & Privacy

Everything runs locally.

Data never leaves your machine.

No communication with:

* OpenAI
* Gemini
* Claude
* Anthropic

No cloud vector database.

No external APIs.

---

# Current Limitations

* Optimized for digital PDFs
* Scanned PDFs require OCR
* No source citations yet
* No chat memory yet

---

# Future Roadmap

Planned features:

* OCR support
* Source citations
* Conversation memory
* Streamlit UI
* React frontend
* FastAPI backend
* Hybrid Search (FAISS + BM25)
* Re-ranking
* Firebase integration
* Multi-user support
* Agentic RAG workflows

---

# Author

Vinod Kumar

Building secure, private, and offline AI systems.
