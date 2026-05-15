from typing import List, Dict, Any
from src.core.base_llm import BaseLLM
from src.prompts.templates import PromptTemplates

class PromptChain:
    """
    Handles multi-step reasoning (Chain of Thought).
    """

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def run_rag_chain(self, query: str, context_list: List[str]) -> str:
        """
        Standard RAG chain: Combine context -> Format Prompt -> Call LLM.
        """
        combined_context = "\n---\n".join(context_list)
        
        user_prompt = PromptTemplates.format_prompt(
            PromptTemplates.RAG_USER_PROMPT,
            context=combined_context,
            query=query
        )
        
        return self.llm.generate(
            prompt=user_prompt,
            system_prompt=PromptTemplates.RAG_SYSTEM_PROMPT
        )

    def run_plan_and_execute(self, complex_request: str):
        """
        Multi-step: 1. Create Plan -> 2. (Future: Execute each task)
        """
        plan_prompt = PromptTemplates.format_prompt(
            PromptTemplates.PLANNER_PROMPT,
            request=complex_request
        )
        
        # We use generate_json for structured output
        plan = self.llm.generate_json(plan_prompt)
        return plan
