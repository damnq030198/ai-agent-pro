import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional

class VectorStore:
    """
    Interface with ChromaDB (running in Docker).
    Manages collections and semantic search.
    """

    def __init__(self, host: str = "localhost", port: int = 8000):
        self.client = chromadb.HttpClient(host=host, port=port)

    def get_or_create_collection(self, name: str):
        return self.client.get_or_create_collection(name=name)

    def add_documents(self, collection_name: str, ids: List[str], documents: List[str], embeddings: List[List[float]], metadatas: Optional[List[Dict]] = None):
        collection = self.get_or_create_collection(collection_name)
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def query(self, collection_name: str, query_embeddings: List[List[float]], n_results: int = 5) -> Dict[str, Any]:
        collection = self.get_or_create_collection(collection_name)
        return collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )

    def delete_collection(self, name: str):
        self.client.delete_collection(name=name)
