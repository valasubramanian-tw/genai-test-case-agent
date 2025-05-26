"""
Main Test Case Agent implementation.
"""
from typing import AsyncGenerator
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from ...models.jira_story import JiraStory
from ..llm.chat_ollama_llm import ChatLLM
from ..prompts.prompt_manager import promptManager
from ..tools.jira_mcp_client import client as jira_mcp_client

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
        try:
            prompts = promptManager.get_prompt("get_jira_story")
            messages = [
                SystemMessage(content=prompts["system"]),
                HumanMessage(content=prompts["user"])
            ]
            jira_tools = await jira_mcp_client.get_tools()
            model = self.llm.get_chat_model()
            # model_with_tools = model.bind_tools(jira_tools)
            agent = create_react_agent(model, jira_tools, response_format=JiraStory)
            response = await agent.ainvoke({"messages": messages})
            structed_response = response["structured_response"]
            return structed_response
            
        except Exception as e:
            print(f"Error processing story details: {str(e)}")
            return e
        
    async def stream_jira_story_details(self, story_id: str) -> AsyncGenerator[str]:
        """
        Stream the details of a Jira story using the provided story ID.
        Get streaming response of fetching a Jira story by its ID.

        Args:
            story_id (str): The ID of the Jira story to fetch.
            
        Yields:
            dict: Chunks of the story details as they become available
        """
        try:
            prompts = promptManager.get_prompt("get_jira_story")
            messages = [
                SystemMessage(content=prompts["system"]),
                HumanMessage(content=prompts["user"])
            ]
            
            tools = await jira_mcp_client.get_tools()
            model = self.llm.get_chat_model()
            model_with_tools = model.bind_tools(tools)            
            async for chunk in model_with_tools.astream(messages):
                yield chunk
                    
        except Exception as e:
            print(f"Error streaming story details: {str(e)}")
            yield {"type": "error", "content": str(e)}
        
    async def generate_jira_test_cases(self, story_id: str):
        """
        Generate test cases for a Jira story using the provided story ID.
        Args:
            story_id (str): The ID of the Jira story to generate test cases for.
        Returns:
            list: A list of generated test cases for the Jira story.
        """
        try:
            prompts = promptManager.get_prompt("generate_jira_test_cases")
            messages = [
                SystemMessage(content=prompts["system"]),
                HumanMessage(content=prompts["user"])
            ]
            tools = [] # await jira_mcp_client.get_tools()
            model = self.llm.get_chat_model()
            model_with_tools = model.bind_tools(tools)
            chain = model | StrOutputParser()
            response = await chain.ainvoke(messages)
            return response
            
        except Exception as e:
            print(f"Error generating test cases: {str(e)}")
            return e
        ...