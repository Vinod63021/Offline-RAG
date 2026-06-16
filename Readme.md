
# OfflineRAG - Enterprise Offline RAG System

## Overview

VaultRAG is a fully offline Retrieval-Augmented Generation (RAG) system designed to build a private AI knowledge assistant capable of understanding and answering questions from personal and organizational data.

Unlike cloud-based AI systems, VaultRAG runs entirely on local hardware and does not require internet access after the initial model download.

The system supports multiple data formats, OCR, hierarchical chunking, semantic retrieval, reranking, and local LLM inference.

---

# Key Features

## Fully Offline

* No OpenAI API
* No cloud dependency
* Local embeddings
* Local vector database
* Local LLM inference

---

## Multi-Format Document Support

Supported file types:

* PDF
* Scanned PDF
* DOCX
* TXT
* CSV
* XLSX
* JSON
* SQLite Database (.db)
* Images (.jpg, .jpeg, .png, .bmp)
* HTML files

---

## OCR Support

Scanned documents and images are automatically processed using EasyOCR.

Supported:

* Scanned PDFs
* Screenshots
* Photos
* Documents captured from mobile devices

---

## Hierarchical Chunking

Instead of splitting documents into random character blocks, VaultRAG preserves document structure.

Example:

Resume
├── Education
├── Projects
├── Skills
└── Certifications

Each section is stored as a meaningful chunk.

---

## Semantic Embeddings

Embedding Model:

BAAI/bge-base-en-v1.5

Specifications:

* 768 Dimensions
* High semantic accuracy
* Optimized for retrieval systems
* Fully offline

---

## Vector Database

Database:

FAISS

Benefits:

* Fast retrieval
* Lightweight
* Local storage
* No server required

---

## Advanced Retrieval

Pipeline:

Question
↓
BGE Base Embedding
↓
FAISS Search
↓
Top 20 Chunks
↓
BGE Reranker
↓
Best 5 Chunks
↓
Qwen3
↓
Answer

---

## Local LLM

Current Model:

Qwen3 8B

Features:

* Excellent reasoning
* Good retrieval grounding
* Fast local inference
* Fully offline

---

# Project Architecture

Documents
│
├── PDF
├── DOCX
├── XLSX
├── CSV
├── TXT
├── JSON
├── SQLite
├── HTML
├── Images
└── Scanned PDFs
│
▼
Document Loader
│
▼
Text Extraction
│
▼
OCR (EasyOCR)
│
▼
Hierarchical Chunking
│
▼
BGE Base Embeddings
│
▼
FAISS Vector Database
│
▼
Top 20 Retrieval
│
▼
BGE Reranker
│
▼
Best 5 Chunks
│
▼
Qwen3 8B
│
▼
Answer Generation

---

# Workflow

## Step 1

Place documents inside:

data/

---

## Step 2

Run ingestion:

python ingest.py

This process:

* Loads documents
* Extracts text
* Runs OCR
* Performs hierarchical chunking
* Generates embeddings
* Stores vectors in FAISS

---

## Step 3

Launch chat:

python chat.py

---

## Step 4

Ask questions

Examples:

What projects has Vinod worked on?

What is the CGPA mentioned in the resume?

List all students from the database.

Summarize the project report.

---

# How Retrieval Works

Traditional Search:

Question
↓
Keyword Match
↓
Answer

Problems:

* Misses meaning
* Sensitive to wording

---

VaultRAG Search:

Question
↓
Embedding
↓
Vector Search
↓
Semantic Similarity
↓
Relevant Chunks

Benefits:

* Understands meaning
* Works with different wording
* Better recall

---

# What is an Embedding?

Embeddings convert text into numbers.

Example:

"Artificial Intelligence"

↓

[0.23, -0.18, 0.45, ...]

The embedding model places similar concepts near each other in vector space.

Example:

AI
Machine Learning
Deep Learning

are closer together than:

AI
Pizza
Football

---

# Why BGE Base?

Previous Version:

BGE Small

* 384 Dimensions
* Smaller
* Faster
* Lower retrieval accuracy

Current Version:

BGE Base

* 768 Dimensions
* Better semantic understanding
* Higher retrieval quality

Result:

More accurate document retrieval.

---

# What is Hierarchical Chunking?

Old Version:

Document
↓
1000 Characters
↓
1000 Characters

Problems:

* Breaks context
* Splits sentences
* Splits sections

Example:

Education section could be divided across multiple chunks.

---

New Version:

Document
↓
Sections
↓
Paragraph Groups
↓
Chunks

Benefits:

* Preserves meaning
* Better retrieval
* Better answers

---

# What is a Reranker?

Most people misunderstand this concept.

FAISS finds chunks that look similar.

Example:

Question:

What is Vinod's educational qualification?

FAISS might return:

* Education
* Projects
* Skills
* Address

because all are related to the person.

---

BGE Reranker reads:

Question + Chunk

and scores relevance.

Example:

Education Chunk
Score: 0.99

Projects Chunk
Score: 0.20

Address Chunk
Score: 0.03

Then only the highest scoring chunks are sent to Qwen.

Result:

More accurate answers.

Less hallucination.

---

# Old Architecture vs New Architecture

## Old Version

PDF
↓
Character Chunking
↓
BGE Small
↓
FAISS
↓
Top 4 Chunks
↓
Qwen

Limitations:

* Poor chunk quality
* Lower retrieval accuracy
* No reranking
* Limited file support

---

## Current Version

Multi-Format Data
↓
OCR
↓
Hierarchical Chunking
↓
BGE Base
↓
FAISS
↓
Top 20 Chunks
↓
BGE Reranker
↓
Best 5 Chunks
↓
Qwen3

Advantages:

* Better retrieval
* Better chunk quality
* Better semantic understanding
* Higher answer accuracy

---

# Project Structure

offline-rag/

├── data/

├── models/

│ ├── bge-base/

│ └── bge-reranker-base/

├── vectorstore/

├── document_loader.py

├── hierarchical_chunker.py

├── model_loader.py

├── reranker.py

├── ingest.py

├── chat.py

├── requirements.txt

└── README.md

---

# Installation

## Create Virtual Environment

python -m venv venv

Windows:

venv\Scripts\activate

Linux:

source venv/bin/activate

---

## Install Dependencies

pip install -r requirements.txt

---

## Download Embedding Model

python download_embedding.py

---

## Download Reranker Model

python download_reranker.py

---

## Install Ollama

Download and install Ollama.

Pull model:

ollama pull qwen3:8b

Verify:

ollama run qwen3:8b

---

# Running VaultRAG

## Build Vector Database

python ingest.py

---

## Start Ollama

ollama serve

---

## Launch Assistant

python chat.py

---

# Current Status

Completed:

* Multi-format ingestion
* OCR
* Hierarchical chunking
* BGE Base embeddings
* FAISS vector search
* BGE reranking
* Qwen3 integration
* Offline operation

---

# Planned Upgrades

* Hybrid Search (BM25 + FAISS)
* Metadata Filtering
* Conversation Memory
* Incremental Indexing
* Source Grounding
* Qdrant Support
* Multi-user Knowledge Vaults

---

# License

MIT License

---

# Author

Vinod Kumar

VaultRAG is a personal project focused on building an enterprise-grade fully offline AI knowledge assistant.
