import asyncio
from browser_use import Agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class BrowserTool:
    """
    Automates web browsing using browser-use library.
    Allows the agent to search the web, click elements, and extract information.
    """

    def __init__(self, provider="anthropic"):
        # We use ChatOpenAI or ChatAnthropic for browser-use logic
        if provider == "anthropic":
            self.llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", api_key=os.getenv("ANTHROPIC_API_KEY"))
        else:
            self.llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    async def browse(self, task: str) -> str:
        """
        Executes a browsing task and returns the result.
        Example task: 'Find the current stock price of NVIDIA and tell me its market cap'
        """
        print(f"🌐 BrowserTool is starting task: {task}")
        
        agent = Agent(
            task=task,
            llm=self.llm,
        )
        
        result = await agent.run()
        
        # Extract the final answer from the result history
        if result and len(result.history) > 0:
            final_answer = result.history[-1].result
            print(f"✅ BrowserTask Completed: {final_answer}")
            return str(final_answer)
        
        return "No information found."

# Helper to run async from sync code if needed
def run_browser_task(task_description: str, provider="anthropic"):
    return asyncio.run(BrowserTool(provider).browse(task_description))

if __name__ == "__main__":
    # Test simple search
    test_task = "What is the latest version of Python released today?"
    print(run_browser_task(test_task))
