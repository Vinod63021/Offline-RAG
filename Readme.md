# Offline RAG Assistant (Private Local AI)

## Overview

This project is a fully local and private RAG (Retrieval-Augmented Generation) system.

The goal is to build an AI assistant that can answer questions from your PDF documents without sending any data to OpenAI, Gemini, Claude, or any cloud service.

Everything runs on your own computer.

---

# Architecture

```text
PDF Documents
      ↓
Text Extraction
      ↓
Chunking
      ↓
Embedding Model (BGE Small)
      ↓
FAISS Vector Database
      ↓
Retriever
      ↓
Qwen3 (Ollama)
      ↓
Answer
```

---

# How RAG Works

RAG stands for:

* Retrieval
* Augmented
* Generation

Instead of asking the LLM to remember everything, we first search our documents and then provide the relevant information to the model.

Example:

User Question:

```text
What is the attendance requirement?
```

Process:

```text
Question
   ↓
Retriever searches PDFs
   ↓
Finds:
"Students must maintain 75% attendance"
   ↓
Qwen3 receives context
   ↓
Generates answer
```

Answer:

```text
The minimum attendance requirement is 75%.
```

---

# Why Use RAG?

Without RAG:

```text
Question
   ↓
LLM
   ↓
Guess
```

With RAG:

```text
Question
   ↓
Search Documents
   ↓
Get Relevant Information
   ↓
LLM
   ↓
Accurate Answer
```

Benefits:

* Better accuracy
* Uses private documents
* No retraining required
* Works offline
* No API costs

---

# Technologies Used

## Ollama

Runs local AI models.

Used for:

```text
Qwen3 8B
```

Role:

```text
Answer Generation
```

---

## Qwen3

Large Language Model (LLM).

Role:

```text
Understand context
Generate final answer
```

---

## BGE Small

Embedding model.

Role:

```text
Convert text into vectors
```

Used during:

* PDF ingestion
* User query search

---

## FAISS

Facebook AI Similarity Search

Role:

```text
Store vectors
Search vectors
```

FAISS is not an AI model.

It is a vector search engine.

---

## LangChain

Used to connect:

* PDFs
* Embeddings
* FAISS
* Ollama

into one pipeline.

---

# Project Structure

```text
offline-rag/
│
├── documents/
│   ├── file1.pdf
│   ├── file2.pdf
│
├── models/
│   └── bge-small/
│
├── vectorstore/
│
├── model_loader.py
├── ingest.py
├── chat.py
│
├── requirements.txt
│
└── README.md
```

---

# Hardware Requirements

Recommended:

```text
Windows 10/11

16 GB RAM

RTX 3050 or higher

20 GB free disk space
```

Current machine:

```text
RAM: 16 GB
GPU: RTX 3050
OS: Windows
```

Suitable for:

```text
Qwen3 8B
```

---

# Installation

## Step 1

Create virtual environment:

```powershell
python -m venv venv
```

Activate:

```powershell
venv\Scripts\activate
```

---

## Step 2

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## Step 3

Install Ollama

Download:

[https://ollama.com](https://ollama.com)

Verify:

```powershell
ollama --version
```

---

## Step 4

Download Qwen3

```powershell
ollama pull qwen3:8b
```

Verify:

```powershell
ollama run qwen3:8b
```

---

# Embedding Model

This project uses:

```text
BAAI/bge-small-en-v1.5
```

Purpose:

```text
Convert text into embeddings
```

First run:

```text
Download model
Save locally
```

Later runs:

```text
Load local copy
```

No internet required after download.

---

# PDF Processing Flow

When running:

```powershell
python ingest.py
```

Process:

```text
PDF
 ↓
Read Text
 ↓
Chunk Text
 ↓
Generate Embeddings
 ↓
Store in FAISS
```

Example:

```text
Attendance Rules

Students must maintain
75% attendance.
```

becomes:

```text
Chunk
 ↓
Embedding
 ↓
FAISS Storage
```

---

# Text Extraction

Current Method:

```text
PyPDFLoader
```

Internally uses:

```text
pypdf
```

Suitable for:

✅ Digital PDFs

Examples:

```text
Word to PDF
Google Docs PDF
Normal PDFs
```

Not suitable for:

❌ Scanned PDFs

Example:

```text
Photo of a document
Scanned notebook page
```

Future upgrade:

```text
OCR
(Tesseract / EasyOCR)
```

---

# Chunking

Documents are split into smaller pieces.

Example:

```text
Original Document
```

↓

```text
Chunk 1
Chunk 2
Chunk 3
```

Current settings:

```python
chunk_size=1000
chunk_overlap=200
```

Reason:

```text
Improves retrieval quality
```

---

# Embeddings

BGE converts text:

```text
Attendance must be above 75%
```

into:

```text
[0.23, 0.67, 0.81, ...]
```

Computers compare vectors instead of words.

This enables semantic search.

---

# FAISS Database

Stores:

```text
Chunk
Vector
Metadata
```

Example:

```text
Chunk 1
 ↓
Vector 1

Chunk 2
 ↓
Vector 2
```

Saved in:

```text
vectorstore/
```

Files:

```text
index.faiss
index.pkl
```

---

# Chat Flow

When running:

```powershell
python chat.py
```

User asks:

```text
What is attendance requirement?
```

Process:

```text
Question
 ↓
Embedding Model
 ↓
FAISS Search
 ↓
Top Chunks
 ↓
Build Prompt
 ↓
Qwen3
 ↓
Answer
```

---

# What Happens Internally

Example:

User:

```text
What is attendance requirement?
```

Question Embedding:

```text
[0.11, 0.34, 0.92 ...]
```

FAISS finds:

```text
Students must maintain
75% attendance.
```

Prompt becomes:

```text
Context:

Students must maintain
75% attendance.

Question:

What is attendance requirement?
```

Qwen3 responds:

```text
The minimum attendance requirement is 75%.
```

---

# Security

Current Design:

```text
Local PDFs
Local Embeddings
Local FAISS
Local Qwen3
```

No cloud APIs.

No OpenAI.

No Gemini.

No Claude.

No external vector database.

Benefits:

```text
Private
Secure
Offline
No API costs
```

---

# Future Improvements

Planned upgrades:

* Source citations
* Conversation memory
* Streamlit UI
* React frontend
* FastAPI backend
* OCR support
* Hybrid Search (FAISS + BM25)
* Re-ranking
* Agentic RAG
* Firebase integration
* Multi-user support

---

# Current Workflow

Build vector database:

```powershell
python ingest.py
```

Start chatbot:

```powershell
python chat.py
```

Exit chatbot:

```text
exit
```

---

# Summary

This project creates a fully private AI assistant using:

```text
Qwen3
+
BGE Small
+
FAISS
+
LangChain
+
PDF Documents
```

The assistant retrieves information from PDFs and generates answers locally on the user's machine without relying on external AI services.
