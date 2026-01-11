from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.health import router as health_router
from app.api.ingest import router as ingest_router
from app.api.query import router as query_router


app = FastAPI(
    title="MiniRAG",
    version="1.0.0",
    description="Document-grounded Mini RAG system"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all for dev
    allow_methods=["*"],        # GET, POST, OPTIONS, etc.
    allow_headers=["*"],        # Content-Type, Authorization, etc.
)


app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(query_router)
