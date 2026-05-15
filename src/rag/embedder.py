import os
from typing import List, Union
from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    """
    Handles converting text into vector embeddings.
    Defaults to local model (all-MiniLM-L6-v2) for speed and 0 cost.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # This model runs locally on your CPU/GPU
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: Union[str, List[str]]) -> np.ndarray:
        """Generates embedding for a single string or a list of strings."""
        return self.model.encode(text)

    def get_embedding_dimension(self) -> int:
        """Returns the size of the vector."""
        return self.model.get_sentence_embedding_dimension()
