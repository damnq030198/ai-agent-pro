class PromptTemplates:
    """
    Centralized store for all prompt templates.
    Use {variable} syntax for dynamic content.
    """

    # RAG: Standard prompt for answering based on retrieved context
    RAG_SYSTEM_PROMPT = """You are a helpful and professional AI Assistant. 
Your task is to answer the user's question using ONLY the provided context.
If the answer is not in the context, say that you don't know based on the provided documents.
Keep your answer concise and structured."""

    RAG_USER_PROMPT = """CONTEXT:
{context}

QUESTION:
{query}

ANSWER:"""

    # PLANNING: For breaking down complex tasks
    PLANNER_PROMPT = """As an expert project manager, break down the following request into a series of small, actionable tasks.
REQUEST: {request}

Format your response as a JSON list of tasks:
[{"id": 1, "task": "description", "dependency": null}]"""

    # REFINER: For self-correction
    REFINER_PROMPT = """Review the following AI response for accuracy and clarity. 
If there are errors or it can be improved, provide a better version.
ORIGINAL RESPONSE: {response}
IMPROVED RESPONSE:"""

    @staticmethod
    def format_prompt(template: str, **kwargs) -> str:
        """Utility to safely format templates with provided variables."""
        return template.format(**kwargs)
