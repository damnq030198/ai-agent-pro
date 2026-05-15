from typing import List, Optional, Dict, Any
from src.core.factory import ModelFactory
from src.rag.retriever import Retriever
from src.prompts.chain import PromptChain
from src.inference.response_parser import ResponseParser

class InferenceEngine:
    """
    The Orchestrator: Coordinates RAG, Prompts, and LLMs to provide final answers.
    """

    def __init__(self, retriever: Retriever, model_id: Optional[str] = None):
        self.retriever = retriever
        # Initialize the chosen LLM
        self.llm = ModelFactory.get_model(model_id)
        self.prompt_chain = PromptChain(self.llm)
        self.parser = ResponseParser()

    def query_with_rag(self, user_query: str, collection_name: str = "agent_knowledge") -> str:
        """
        Full RAG Pipeline: Retrieve -> Chain -> LLM -> Parse
        """
        # 1. Retrieve context from Vector DB
        context_chunks = self.retriever.retrieve(user_query, collection_name=collection_name)
        
        # 2. Run the RAG chain (Formats prompt + calls LLM)
        raw_response = self.prompt_chain.run_rag_chain(user_query, context_chunks)
        
        # 3. Parse/Clean response
        return self.parser.clean_markdown(raw_response)

    def generate_task_plan(self, complex_request: str) -> List[Dict]:
        """
        Task Planning Pipeline
        """
        raw_plan = self.prompt_chain.run_plan_and_execute(complex_request)
        # Ensure it's a list of dictionaries
        if isinstance(raw_plan, str):
            return self.parser.to_json(raw_plan)
        return raw_plan
