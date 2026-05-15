from typing import List, Dict, Any
from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore

class Retriever:
    """
    Handles retrieving the most relevant document chunks for a given query.
    """

    def __init__(self, embedder: Embedder, vector_store: VectorStore):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str, collection_name: str = "agent_knowledge", n_results: int = 3) -> List[str]:
        """
        1. Embed the query
        2. Search in VectorStore
        3. Return list of relevant text chunks
        """
        # Convert query to vector
        query_vector = self.embedder.embed_text(query).tolist()
        
        # Search
        results = self.vector_store.query(
            collection_name=collection_name,
            query_embeddings=[query_vector],
            n_results=n_results
        )
        
        # Extract and return documents
        if results and 'documents' in results:
            return results['documents'][0]
        return []
