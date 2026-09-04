# AI Engineering Learning Journey

This repository documents my progression in AI engineering by building increasingly capable AI applications while learning the underlying concepts before introducing higher-level frameworks.

Instead of starting directly with libraries such as LangChain or FastAPI, I first implemented the core ideas manually and then gradually migrated to modern tooling. Each phase is preserved to show the evolution from simple API usage to a modular backend application.

> **Note**
>
> This repository intentionally preserves every implementation phase instead of replacing previous versions. The goal is to document the learning progression and compare manual implementations with framework-based solutions.

---

# Repository Structure

```text
.

├── phase_1/
├── phase_2/
├── phase_3/
├── phase_4/
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env (not committed)
```

---

# Learning Progression

## Phase 1 — Gemini API Fundamentals

A small introductory project created while learning how to interact with Google's Gemini API.

### Topics Covered

- Gemini API integration
- Prompt construction
- Sentiment analysis example
- Raw HTTP requests using Python

---

## Phase 2 — Manual Retrieval-Augmented Generation (RAG)

Implemented the core components of a Retrieval-Augmented Generation (RAG) system without using orchestration frameworks.

### Features

- Manual text chunking with configurable overlap
- Embedding generation using the Gemini Embedding API (raw HTTP requests)
- Embedding storage using JSON
- Manual cosine similarity retrieval using NumPy
- Context-grounded answer generation
- Manual tool routing
    - RAG
    - Calculator
    - Wikipedia
- LLM-as-a-Judge evaluation pipeline
- Incremental evaluation logging
- Retry with Gemini retryDelay

This phase focuses on understanding how retrieval systems work internally before introducing higher-level abstractions.

---

## Phase 3 — LangChain Migration

Migrated the manual RAG implementation to LangChain while preserving the same retrieval workflow.

### Features

- GoogleGenerativeAIEmbeddings
- FAISS Vector Store
- ChatPromptTemplate
- Stuff Documents Chain
- Retrieval Chain
- Persistent vector database
- Modular project structure

The objective of this phase was to understand what LangChain abstracts compared to a manual implementation.

---

## Phase 4 — FastAPI Backend

Wrapped the LangChain-based RAG system inside a REST API.

### Features

- FastAPI REST API
- Request validation using Pydantic
- Response models
- Application lifespan management
- Startup initialization of the RAG pipeline
- Health endpoint
- Rebuild-index endpoint
- API-key authentication
- Request ID generation and request-level logging
- Centralized exception handling
- Rate limiting using SlowAPI
- Separation of API, RAG, configuration, and infrastructure concerns
- Automatic Swagger/OpenAPI documentation


This phase focuses on exposing the RAG pipeline as a backend service.

---

# Technologies Used

- Python
- Google Gemini API
- NumPy
- Requests
- LangChain
- FAISS
- FastAPI
- Pydantic
- Wikipedia API
- python-dotenv

---

# Running the Repository

## 1. Clone the Repository

```bash
git clone https://github.com/Gokul-m-2000/agentic-rag-assistant.git

cd agentic-rag-assistant
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Create a `.env` File

```text
GEMINI_API_KEY=your_api_key_here
```

---

# Running Phase 1

Navigate to the Phase 1 directory.

```bash
cd phase_1
python main.py
```

---

# Running Phase 2

Navigate to the Phase 2 directory.

```bash
cd phase_2
```

Build the embedding index (one-time).

```bash
python build_index.py
```

This generates

```text
data/embeddings.json
```

Run the assistant.

```bash
python main.py
```

### Evaluation

Generate answers

```bash
python evaluation/build_run_results.py
```

Run the evaluator

```bash
python evaluation/evaluator.py
```

Generated files

```text
evaluation/run_results.json
evaluation/eval_results.json
evaluation/eval_log.txt
```

---

# Running Phase 3

Navigate to the Phase 3 directory.

```bash
cd phase_3
```

Build the vector store.

```bash
python build_index.py
```

Run the assistant.

```bash
python main.py
```

---

# Running Phase 4

Navigate to the Phase 4 directory.

```bash
cd phase_4
```

Build the vector store.

```bash
python build_index.py
```

Start the FastAPI server.

```bash
uvicorn main:app --reload
```

FastAPI automatically generates interactive API documentation.

Open

```text
http://127.0.0.1:8000/docs
```

---

# Generated Files

The following files are generated during execution and are intentionally excluded from version control.

### Phase 2

- data/embeddings.json
- evaluation/run_results.json
- evaluation/eval_results.json
- evaluation/eval_log.txt

### Phase 3

- vector_store/

### Phase 4

- vector_store/
- phase_4/logs/
---

# Engineering Decisions

Some implementation choices were made intentionally for learning purposes.

- Used raw HTTP requests before official SDKs to understand the Gemini API contract.
- Implemented manual document chunking before using LangChain abstractions.
- Implemented cosine similarity manually before introducing FAISS.
- Built a complete manual RAG pipeline before migrating to LangChain.
- Preserved every learning phase instead of replacing earlier implementations.
- Introduced FastAPI only after understanding the retrieval pipeline.

---

# Current Status

Completed

- Gemini API integration
- Manual RAG implementation
- Tool routing
- Evaluation pipeline
- LangChain migration
- FastAPI backend
- Application lifespan management
- Logging and request tracing
- Centralized exception handling
- API-key authentication
- Rate limiting

Currently Building

- Production-grade PostgreSQL + pgvector RAG architecture
- Incremental document ingestion
- Persistent document and conversation storage

---

Future Improvements

- Hybrid retrieval
- Reranking
- RAG evaluation
- Persistent conversations
- LangGraph agent
- SQL and web tools
- Redis-backed infrastructure
- Docker deployment

---

# Acknowledgements

The learning approach followed throughout this repository emphasizes understanding the underlying concepts before relying on higher-level frameworks.