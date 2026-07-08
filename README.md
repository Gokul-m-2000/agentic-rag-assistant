# AI Assistant with RAG, Tool Routing & LLM Evaluation

A progressive AI engineering project built from first principles, following Marina Wyss's **"layered complexity"** philosophy. Every core component was implemented manually before introducing higher-level frameworks such as LangChain.

## Overview

This project demonstrates the implementation of an end-to-end **Retrieval-Augmented Generation (RAG)** pipeline together with a simple AI agent capable of routing user queries to multiple tools.

### Features

- Manual text chunking with configurable overlap
- Embedding generation using the Gemini Embedding API (raw HTTP requests)
- Cosine similarity retrieval implemented from scratch using NumPy
- Context-grounded answer generation using retrieved chunks
- Agentic tool routing (RAG, Calculator, Wikipedia)
- LLM-as-a-Judge evaluation pipeline using a gold-standard test set
- Modular project structure designed for maintainability and future expansion

---

## Project Structure

```text
AI_ASSIST/
│
├── data/
│   └── doc.txt
│
├── evaluation/
│   ├── build_run_results.py
│   ├── evaluator.py
│   └── gold_test.json
│
├── build_index.py
├── chunker.py
├── config.py
├── embedder.py
├── generator.py
├── retriever.py
├── router.py
├── tools.py
├── main.py
│
├── requirements.txt
├── .gitignore
├── README.md
└── .env (not committed)
```

---

## Generated Files

The following files are generated automatically during execution and are **not committed** to the repository:

- `data/embeddings.json`
- `evaluation/run_results.json`
- `evaluation/eval_results.json`
- `evaluation/eval_log.txt`

---

## How to Run

### 1. Clone the repository

```bash
git clone <repository-url>
cd AI_ASSIST
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

```text
GEMINI_API_KEY=your_api_key_here
```

### 4. Build the embedding index (one-time)

```bash
python build_index.py
```

This generates:

```text
data/embeddings.json
```

---

### 5. Run the assistant

```bash
python main.py
```

---

### 6. Generate evaluation answers

```bash
python evaluation/build_run_results.py
```

This generates:

```text
evaluation/run_results.json
```

---

### 7. Run the evaluation pipeline

```bash
python evaluation/evaluator.py
```

This generates:

```text
evaluation/eval_results.json
evaluation/eval_log.txt
```

---

## Engineering Decisions

- **Raw HTTP Requests** — Used the `requests` library directly to understand the complete Gemini API contract before using official SDKs.
- **Manual Text Chunking** — Implemented configurable chunking with overlap to understand how document splitting affects retrieval quality.
- **Manual Embedding Pipeline** — Built the indexing workflow from scratch without vector database libraries.
- **Manual Cosine Similarity** — Implemented similarity search using NumPy to understand the underlying mathematics instead of relying on external libraries.
- **Agentic Tool Routing** — Implemented an LLM-based router capable of selecting and executing multiple tools based on user intent.
- **LLM-as-a-Judge Evaluation** — Built an automated evaluation pipeline using a separate judge prompt for factual correctness and out-of-scope refusal detection.
- **Checkpoint Saving** — Evaluation progress is saved incrementally, allowing interrupted runs to resume without recomputing completed questions.
- **Retry with Backoff** — Implements dynamic retry logic by reading Gemini's `retryDelay` value instead of relying on fixed retry intervals.

---

## Tech Stack

- Python
- Gemini API
- NumPy
- Requests
- Wikipedia API
- python-dotenv

---

## Future Improvements

- Replace JSON embedding storage with a vector database (FAISS or ChromaDB)
- Integrate LangChain for orchestration
- Add conversational memory
- Improve external knowledge retrieval
- Build a FastAPI backend
- Deploy as an API service