"""
Main Test Case Agent implementation.
"""
import json
from langgraph.prebuilt import create_react_agent
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from ..prompts.prompt_manager import promptManager
from ..mcp.jira_mcp_client import client as jira_mcp_client

class TestCasAgent:
    def __init__(self, model_name, llm_base_url, llm_api_key, temperature):
        self.llm = ChatOpenAI(
            model=model_name,
            base_url="https://api.groq.com/openai/v1",
            api_key=llm_api_key,
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
            "key": story_id,
            "summary": "Not Available",
            "description": "Not Available",
            "status": "Not Available"
        }
        
        try:
            prompts = promptManager.get_prompt("get_jira_story")
            messages = [
                SystemMessage(content=prompts["system"]),
                HumanMessage(content=prompts["user"])
            ]
            tools = await jira_mcp_client.get_tools()
            agent = create_react_agent(self.llm, tools)
            response = await agent.ainvoke({"messages": messages})
            
            if not response or not response.content:
                return default_response
                
            content = response.content.strip()
            if isinstance(content, dict):
                return content
            
            # Try parsing the string response as JSON
            parsed_response = json.loads(content)
            if all(key in parsed_response for key in default_response.keys()):
                return parsed_response
                
            return default_response
            
        except Exception as e:
            print(f"Error processing story details: {str(e)}")
            return default_response
        
    def generate_test_cases(self):
        # Placeholder for actual implementation
        ...