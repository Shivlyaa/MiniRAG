from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.chunking import create_chunk
from app.rag.embedding import embed_chunks
from app.rag.vector_store import clear_index, upsert_chunks


router = APIRouter(prefix="/ingest", tags=["ingest"])


class IngestRequest(BaseModel):
    text: str


class IngestResponse(BaseModel):
    chunks_ingested: int


@router.post("", response_model=IngestResponse)
def ingest_document(payload: IngestRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # 1. Reset memory (single corpus)
    clear_index()

    # 2. Chunk
    chunks = create_chunk(payload.text)

    # 3. Embed
    chunks = embed_chunks(chunks)

    # 4. Store
    upsert_chunks(chunks)

    return IngestResponse(chunks_ingested=len(chunks))
