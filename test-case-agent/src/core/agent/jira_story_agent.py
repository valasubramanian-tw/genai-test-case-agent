"""
Jira Story Agent implementation.
"""
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from ...models.jira_story import JiraStory
from ..llm.chat_ollama_llm import ChatLLM
from ..prompts.prompt_manager import promptManager
from ..tools.jira_mcp_client import client as jira_mcp_client

class JiraStoryAgent:
    def __init__(self, model_name, llm_base_url, llm_api_key, temperature):
        self.llm = ChatLLM(
            model_name=model_name
        )

    async def get_jira_story_details(self, story_id) -> JiraStory | Exception:
        """
        Fetches the details of a Jira story using the provided story ID.
        Args:
            story_id (str): The ID of the Jira story to fetch.
        Returns:
            dict: Details of the Jira story.
        """
        try:
            system_prompt = promptManager.get_system_prompt("get_jira_story")
            user_prompt = promptManager.format_user_prompt("get_jira_story", story_id=story_id)
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            jira_tools = await jira_mcp_client.get_tools()
            model = self.llm.get_chat_model()
            agent = create_react_agent(model, jira_tools, response_format=JiraStory)
            response = await agent.ainvoke({"messages": messages})
            structed_response = response["structured_response"]
            print("get_jira_story_details response:", structed_response)
            return structed_response
            
        except Exception as e:
            print(f"Error processing story details: {str(e)}")
            return Exception(f"Error processing story details: {str(e)}")