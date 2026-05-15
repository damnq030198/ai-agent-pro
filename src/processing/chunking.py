from typing import List
from src.processing.preprocessor import Preprocessor
from src.processing.tokenizer import Tokenizer

class Chunker:
    """
    Splits long text into smaller, overlapping chunks for better RAG performance.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.preprocessor = Preprocessor()
        self.tokenizer = Tokenizer()

    def split_text(self, text: str) -> List[str]:
        """
        Splits text into chunks based on character count (recursive-like simple implementation).
        Ensures each chunk stays within reasonable size and preserves some context overlap.
        """
        # 1. Clean the text first
        clean_text = self.preprocessor.clean_text(text)
        
        if not clean_text:
            return []

        chunks = []
        start = 0
        text_len = len(clean_text)

        while start < text_len:
            # Determine the end of the chunk
            end = min(start + self.chunk_size, text_len)
            
            # If we're not at the end, try to find the last space/newline to avoid cutting a word
            if end < text_len:
                last_space = clean_text.rfind(' ', start, end)
                if last_space != -1 and last_space > start:
                    end = last_space

            chunk = clean_text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start forward, but subtract overlap
            start = end - self.chunk_overlap
            if start < 0: start = 0
            
            # Prevent infinite loop if end doesn't move
            if end <= start + self.chunk_overlap and end < text_len:
                start = end

        return chunks
