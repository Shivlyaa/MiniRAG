from typing import List, Dict

def create_chunk(
      text: str,
      chunk_size: int = 4000, # 800-1k tokens = 4000 chars
      overlap: int = 500,  #12.5% overlap (between 10%-15%)
      source:str = "user_paste"
) -> List[Dict]:
    """
     Splitting the text into overlapping chunks and attaching metadata for retrieval, embeddings
     and citations
    """

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk sie")
    
    # for each chunk:

    chunks = []
    start = 0 
    position = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk_text = text[start:end]

        chunk = {
            "id" : f"chunk_{position}",
            "text" : chunk_text,
            "metadata": {
                "source": source,
                "position": position
            }
        }

        chunks.append(chunk)

        position += 1
        start += chunk_size - overlap


    return chunks

