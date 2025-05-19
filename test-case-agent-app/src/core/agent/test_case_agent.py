"""
Main Test Case Agent implementation.
"""
from langgraph.prebuilt import create_react_agent
from langchain.schema import HumanMessage, SystemMessage
from ..llm.chat_ollama_llm import ChatLLM
from ..prompts.prompt_manager import promptManager
from ..mcp.jira_mcp_client import client as jira_mcp_client

class TestCasAgent:
    def __init__(self, model_name, llm_base_url, llm_api_key, temperature):
        self.llm = ChatLLM(
            model_name=model_name
        )
        self.jira_story = None
        self.test_cases = []

    async def get_jira_story_details(self, story_id):
        """
        Fetches the details of a Jira story using the provided story ID.
        Args:
            story_id (str): The ID of the Jira story to fetch.
        Returns:
            dict: Details of the Jira story.
        """
        default_response = {
            "id": story_id,
            "title": "Not Available",
            "description": "Not Available",
            "status": "Not Available"
        }
        
        try:
            prompts = promptManager.get_prompt("get_jira_story")
            messages = [
                SystemMessage(content=prompts["system"]),
                HumanMessage(content=prompts["user"])
            ]
            tools = [] # await jira_mcp_client.get_tools()
            agent = create_react_agent(self.llm.get_chat_model(), tools)
            response = await agent.ainvoke({"messages": messages})
            
            if response:
                # Extracting the response content
                return response.content
                
            return default_response
            
        except Exception as e:
            print(f"Error processing story details: {str(e)}")
            return default_response
        
    def generate_test_cases(self):
        # Placeholder for actual implementation
        ...