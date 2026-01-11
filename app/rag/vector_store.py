from typing import List, Dict

from pinecone import Pinecone
from app.core.config import settings

pc = Pinecone(api_key=settings.pinecone_api_key)

def get_index():
    """
    gets a handle to the Pinecone index
    """
    return pc.Index(settings.pinecone_index_name)

def clear_index():
    """
     deletes all previous vectors on new document ingestion
    """

    index = get_index()
    try:
        index = get_index()
        index.delete(delete_all=True)
    except Exception as e:
        # Happens if namespace doesn't exist yet
        print(f"Warning, could not clear index: {e}")

def upsert_chunks(chunks: List[Dict]):

    """
    stores embedded chunks to Pinecone
    """

    index = get_index()

    vectors =[]
    
    for chunk in chunks:
        vectors.append(
            (
                chunk["id"],
                chunk["embedding"],
                {
                    **chunk["metadata"],
                    "text" : chunk["text"]
                }
            )
        )

    if vectors:

        index.upsert(vectors=vectors)
