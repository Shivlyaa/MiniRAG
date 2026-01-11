from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from app.rag.retrieval import retrieve_chunks
from app.rag.reranking import rerank_chunks
from app.rag.generation import generate_answer


router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    question: str


class Citation(BaseModel):
    position: int
    text: str


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]


@router.post("", response_model=QueryResponse)
def query_document(payload: QueryRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # 1. Retrieve
    retrieved = retrieve_chunks(payload.question)

    # 2.Rerank
    reranked = rerank_chunks(payload.question, retrieved)

    # 3. Generate answer
    answer = generate_answer(payload.question, reranked)

    # 4. Build citations (top reranked chunks)
    citations = []
    for chunk in reranked:
        citations.append(
            Citation(
                position=chunk["metadata"]["position"],
                text=chunk["text"]
            )
        )

    return QueryResponse(
        answer=answer,
        citations=citations
    )
