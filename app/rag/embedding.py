from typing import List, Dict
from app.core.config import settings

import cohere 

co = cohere.Client(settings.cohere_api_key)

def embed_chunks(chunks: List[Dict]) -> List[Dict]:
                 """
                 generate embeddings for each chunk using Cohere Embeddings and then attach the vectors to the corresponding chunks 
                 """

                 if not chunks:
                        return chunks 
                 
                 texts = [chunk["text"] for chunk in chunks]

                 response = co.embed(
                    texts= texts,
                    model='embed-english-v3.0',
                    input_type='search_document'
                    )
                 
                 embeddings = response.embeddings

                 for chunk , vector in zip(chunks, embeddings):
                         chunk["embedding"] = vector

                 return chunks
                         
