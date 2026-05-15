import re
import unicodedata

class Preprocessor:
    """
    Cleans and normalizes raw text before indexing or processing.
    """

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""

        # 1. Normalize Unicode (handle special characters)
        text = unicodedata.normalize("NFC", text)

        # 2. Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # 3. Replace multiple newlines with a double newline
        text = re.sub(r'\n\s*\n', '\n\n', text)

        # 4. Replace multiple spaces with a single space
        text = re.sub(r' +', ' ', text)

        # 5. Strip leading/trailing whitespace
        return text.strip()

    @staticmethod
    def remove_urls(text: str) -> str:
        """Optional: Remove URLs if they are not useful for the context."""
        return re.sub(r'http\S+', '', text)
