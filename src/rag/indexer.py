import uuid
from typing import List
from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore

class Indexer:
    """
    Coordinates the process of indexing new documents into the Vector Database.
    """

    def __init__(self, embedder: Embedder, vector_store: VectorStore):
        self.embedder = embedder
        self.vector_store = vector_store

    def index_documents(self, documents: List[str], collection_name: str = "agent_knowledge", metadatas: List[dict] = None):
        """
        Processes a list of text chunks and adds them to ChromaDB.
        """
        if not documents:
            return
            
        # 1. Generate embeddings for all chunks
        embeddings = self.embedder.embed_text(documents).tolist()
        
        # 2. Generate unique IDs
        ids = [str(uuid.uuid4()) for _ in range(len(documents))]
        
        # 3. Add to VectorStore
        self.vector_store.add_documents(
            collection_name=collection_name,
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        print(f"✅ Indexed {len(documents)} chunks into collection '{collection_name}'")
