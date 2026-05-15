import tiktoken

class Tokenizer:
    """
    Counts tokens for different models to ensure context window compliance.
    """

    def __init__(self, model_name: str = "gpt-4"):
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # Fallback to cl100k_base (used by GPT-4 and Claude 3)
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """Returns the number of tokens in a text string."""
        return len(self.encoding.encode(text))

    def truncate_text(self, text: str, max_tokens: int) -> str:
        """Truncates text to a maximum number of tokens."""
        tokens = self.encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text
        return self.encoding.decode(tokens[:max_tokens])
