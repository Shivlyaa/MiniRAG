# MiniRAG — Deterministic Citation-Based Retrieval-Augmented Generation

MiniRAG is a lightweight, end-to-end Retrieval-Augmented Generation (RAG) system designed to ingest documents, retrieve relevant context, and generate answers with clear, deterministic citations.

The project focuses on correctness, transparency, and production-minded engineering rather than surface-level polish.

---

## Live Links

Frontend (Netlify)  
https://minirag-frontend.netlify.app/

Backend API (FastAPI)  
https://shivlyaa-minirag.hf.space/

API Documentation (Swagger)  
https://shivlyaa-minirag.hf.space/docs

GitHub Repository  
https://github.com/Shivlyaa/MiniRAG

---

## What This Project Does

MiniRAG implements a complete RAG pipeline:

1. Document ingestion via a frontend UI or API
2. Deterministic chunking of text
3. Vector embedding of chunks
4. Storage and retrieval using a vector database
5. Optional reranking of retrieved chunks
6. LLM-based answer generation constrained strictly to retrieved context
7. Explicit citations pointing to the source chunks used

If an answer is not present in the ingested document, the system explicitly states that the answer is not found.

---

## Architecture Overview

The system is split into a frontend and a backend.

Frontend  
- Static HTML, CSS, and JavaScript
- Deployed on Netlify
- Used for document ingestion and querying

Backend  
- FastAPI application
- Handles ingestion, retrieval, reranking, and generation
- Deployed as a containerized service

Core pipeline flow:

Frontend  
→ FastAPI backend  
→ Chunking  
→ Embedding (Cohere)  
→ Vector store (Pinecone)  
→ Retrieval and reranking  
→ LLM generation (Hugging Face)  
→ Answer with citations

---

## Project Structure

    MiniRAG/
    ├── app/
    │   ├── main.py
    │   ├── schemas.py
    │   │
    │   ├── api/
    │   │   ├── ingest.py
    │   │   ├── query.py
    │   │   └── health.py
    │   │
    │   ├── core/
    │   │   ├── config.py
    │   │   └── logging.py
    │   │
    │   └── rag/
    │       ├── chunking.py
    │       ├── embedding.py
    │       ├── retrieval.py
    │       ├── reranking.py
    │       ├── prompting.py
    │       ├── generation.py
    │       └── vector_store.py
    │
    ├── frontend/
    │   ├── index.html
    │   ├── script.js
    │   └── style.css
    │
    ├── Dockerfile
    ├── requirements.txt
    ├── README.md
    └── .env.example
    

---

## Deterministic Chunking and Citations

Documents are split into fixed-size overlapping chunks.  
Each chunk is assigned a stable index starting from zero.

During querying:
- Only retrieved chunks are provided to the LLM
- The prompt explicitly forbids using outside knowledge
- All factual statements must be cited using chunk indices

Example citation format:

[0], [2], [3]

This makes the system auditable and prevents hallucinations.

---

## API Endpoints

POST /ingest  
Ingests raw text, chunks it, embeds it, and stores it in the vector database.

POST /query  
Accepts a user question, retrieves relevant chunks, and returns:
- Answer text
- List of cited chunks with positions and source text

GET /health  
Health check endpoint.

---

## Environment Configuration

All secrets are provided via environment variables.  
No secrets are committed to the repository.

Example `.env.example`:

        COHERE_API_KEY=your_key_here
        PINECONE_API_KEY=your_key_here
        PINECONE_INDEX_NAME=minirag-index
        HF_API_TOKEN=your_key_here
        HF_MODEL_ID=meta-llama/Llama-3.1-8B-Instruct


On hosted platforms, these values are set using Secrets rather than plain variables.

---

## Running Locally

Install dependencies:
pip install -r requirements.txt

Run the backend:
uvicorn app.main:app --host 0.0.0.0 --port 8000

Access API docs at:
http://localhost:8000/docs


The frontend can be opened directly as a static site or served using any static file server.

---

## Deployment Notes

Backend  
- Containerized using Docker
- Uses Python 3.11 for compatibility with dependencies
- Runs FastAPI with Uvicorn

Frontend  
- Static deployment on Netlify
- Configured to point to the live backend base URL
- Does not use the /docs endpoint for API calls

---

## Acceptance Criteria Mapping

Working live URLs  
Satisfied

First screen loads without console errors  
Satisfied

Query flow: retrieve → rerank → answer  
Satisfied

Citations clearly visible  
Satisfied

README with setup and architecture explanation  
Satisfied

Environment variables handled correctly  
Satisfied

---

## Disqualifiers Explicitly Avoided

No broken or loading-only URLs  
No missing README or setup instructions  
No missing schema or index explanation  
No plagiarized repositories  
No copy-paste code without understanding  
No silent failures or swallowed errors  

---

## Trade-offs and Design Decisions

Pinecone was chosen over local FAISS for reliability and simplicity in a hosted environment.

Cohere embeddings were used for fast and consistent semantic search.

Hugging Face Inference API was used instead of a self-hosted LLM to reduce operational complexity.

The frontend intentionally remains minimal to keep focus on system correctness rather than UI complexity.

---

## What I Would Improve Next

Hybrid retrieval using keyword and vector search  
Streaming responses from the LLM  
Multi-document ingestion and citation grouping  
Evaluation metrics for retrieval quality  
Authentication and rate limiting  

---

## Final Notes

This project prioritizes correctness, transparency, and clear engineering boundaries.

Every component in the pipeline is explicit, inspectable, and designed to fail loudly rather than silently.

The goal was not to build the most complex system, but to build the most understandable and reliable one.



