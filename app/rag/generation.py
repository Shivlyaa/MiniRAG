import requests
from typing import List, Dict

from app.core.config import settings
from app.rag.prompting import build_prompt


def generate_answer(
    query: str,
    reranked_chunks: List[Dict],
    score_threshold: float = 0.3
) -> str:
    """
    Generate a grounded answer using LLaMA via HF Router.
    """

    if not reranked_chunks:
        return "The answer is not found in the provided document."

    top_score = reranked_chunks[0].get("rerank_score", 0)
    if top_score < score_threshold:
        return "The answer is not found in the provided document."

    prompt = build_prompt(query, reranked_chunks)

    response = requests.post(
        f"{settings.hf_base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.hf_api_token}",
            "Content-Type": "application/json"
        },
        json={
            "model": settings.hf_model_id,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
