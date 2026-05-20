# AI Document RAG System

A local Retrieval-Augmented Generation (RAG) application built using FastAPI, ChromaDB, Sentence Transformers, and Ollama.

This project allows users to upload PDF or TXT documents, generate embeddings from extracted text, store vectors in ChromaDB, and ask questions about uploaded documents using a local LLM.

---

# Features

* Upload PDF and TXT files
* Extract text from documents
* Chunk document text
* Generate embeddings using Sentence Transformers
* Store embeddings in ChromaDB
* Semantic similarity search
* Ask questions about uploaded documents
* Local LLM inference using Ollama
* FastAPI backend
* Persistent vector database storage

---

# Tech Stack

## Backend

* FastAPI
* Uvicorn

## AI / RAG

* Sentence Transformers
* ChromaDB
* Ollama
* Vector Embeddings
* Semantic Search

## Document Processing

* PyMuPDF (fitz)

---

# Project Workflow

```text
Document Upload
    ↓
Text Extraction
    ↓
Text Cleaning
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Store in ChromaDB
    ↓
User Question
    ↓
Question Embedding
    ↓
Semantic Retrieval
    ↓
Context Injection
    ↓
LLM Response Generation
```

---

# Supported File Types

* PDF
* TXT

---

# Installation

## Clone Repository

```bash
git clone <your-repository-url>
cd <project-folder>
```

---

## Create Environment

```bash
conda create -n pdfai python=3.11
conda activate pdfai
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

```text
fastapi
uvicorn
pymupdf
chromadb
sentence-transformers
ollama
python-multipart
```

---

# Ollama Setup

Install Ollama:

https://ollama.com/download

Pull model:

```bash
ollama pull llama3.1
```

Run model:

```bash
ollama run llama3.1
```

---

# Run FastAPI Server

```bash
python -m uvicorn main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Upload Document

```http
POST /upload
```

Uploads and processes PDF/TXT documents.

---

## Ask Question

```http
POST /ask
```

Queries uploaded documents using semantic retrieval and local LLM inference.

---

# Example Response

```json
{
  "answer": "According to the document..."
}
```

---

# Learning Outcomes

This project helped in understanding:

* RAG architecture
* Embeddings
* Vector databases
* Semantic retrieval
* FastAPI backend development
* Local LLM integration
* Chunking strategies
* Document processing pipelines

---

# Future Improvements

* DOCX support
* JWT authentication
* Frontend UI
* Docker support
* Source citations
* Retrieval filtering by document
* Streaming responses
* Async background processing
* Better chunking strategies

---

# Disclaimer

This project is built for learning and experimentation purposes and is not production-ready.
