from typing import List, Dict


def build_prompt(
    query: str,
    chunks: List[Dict]
) -> str:
    """
    Build a grounded prompt using reranked chunks.
    """

    context_blocks = []
    for chunk in chunks:
        position = chunk["metadata"]["position"]
        text = chunk["text"]

        context_blocks.append(
            f"[{position}] {text}"
        )

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are an AI assistant answering questions strictly from the provided document context.

Rules:
- Use ONLY the information in the context below.
- Do NOT include citation numbers, references, or bracketed indices in your answer.
- If the answer is not contained in the context, say exactly:
  "The answer is not found in the provided document."

Provide a clear and concise answer.


Context:
{context}

Question:
{query}

Answer:
""".strip()

    return prompt
