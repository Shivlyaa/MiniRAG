from typing import List, Dict
import cohere
from app.core.config import settings
from app.rag.vector_store import get_index

co = cohere.Client(settings.cohere_api_key)

def retrieve_chunks(
        query: str,
        top_k: int = 8
)-> List[Dict]:
    """
    function  for #1 embedding the query and #2 retrieving the top k chunks from Pinecone index
    """

    #embed the query

    query_embedding = co.embed(
        texts = [query],
        model = "embed-english-v3.0" , 
        input_type = "search_query"
    ).embeddings[0]

    #query pineconde
    index = get_index()
    response = index.query(
        vector= query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    #3 normalizing the pinecode response such that we only take what we want

    results =[]

    for match in response.matches:
         results.append({
            "id": match.id,
            "score": match.score,
            "text": match.metadata["text"],
            "metadata": {
                k: v for k, v in match.metadata.items() if k != "text"
            }
        })
         
    return results