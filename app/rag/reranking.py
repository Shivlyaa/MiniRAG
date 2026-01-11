from typing import List, Dict
import cohere

from app.core.config import settings


co = cohere.Client(settings.cohere_api_key)


def rerank_chunks(
    query: str,
    chunks: List[Dict],
    top_n: int = 5
) -> List[Dict]:
    """
    Rerank retrieved chunks using Cohere Rerank.
    """

    if not chunks:
        return []

    documents = [chunk["text"] for chunk in chunks]

    response = co.rerank(
        query=query,
        documents=documents,
        model="rerank-english-v3.0",
        top_n=top_n
    )

    reranked = []
    for result in response.results:
        chunk = chunks[result.index]
        chunk["rerank_score"] = result.relevance_score
        reranked.append(chunk)

    return reranked
