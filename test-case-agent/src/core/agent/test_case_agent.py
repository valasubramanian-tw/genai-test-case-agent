"""
Main Test Case Agent implementation.
"""
from typing import AsyncGenerator
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from .jira_story_agent import JiraStoryAgent
from ...models.jira_story import JiraStory
from ..llm.chat_ollama_llm import ChatLLM
from ..prompts.prompt_manager import promptManager
from ..tools.jira_mcp_client import client as jira_mcp_client

class TestCaseAgent:
    def __init__(self, model_name, llm_base_url, llm_api_key, temperature):
        self.model_name = model_name
        self.llm_base_url = llm_base_url
        self.llm_api_key = llm_api_key
        self.temperature = temperature
        self.llm = ChatLLM(
            model_name=model_name
        )
        
    async def get_jira_test_cases_by_id(self, story_id: str):
        """
        Generate test cases for a Jira story using the provided story ID.
        Args:
            story_id (str): The ID of the Jira story to generate test cases for.
        Returns:
            list: A list of generated test cases for the Jira story.
        """
        try:
            system_prompt = promptManager.get_system_prompt("generate_jira_test_cases")
            user_prompt = promptManager.format_user_prompt(
                "generate_jira_test_cases",
                story_id=story_id
            )
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            tools = await jira_mcp_client.get_tools()
            model = self.llm.get_chat_model()
            agent = create_react_agent(model, tools, response_format="json")
            response = await agent.ainvoke({"messages": messages})
            
            if not response or 'messages' not in response:
                raise ValueError("No messages found in the response.")
            
            ai_messages = [msg for msg in response['messages'] if isinstance(msg, AIMessage)]
            if not ai_messages:
                raise ValueError("No messages found in the response.")
            last_ai_message = ai_messages[-1]
            llm_response = last_ai_message.content
            
            print(f"LLM Response: {llm_response}")
            return llm_response
            
        except Exception as e:
            print(f"Error generating test cases: {str(e)}")
            return e
    
    async def get_jira_test_cases(self, story: JiraStory):
        """
        Generate test cases for a Jira story using the provided story object.
        Args:
            story (JiraStory): The Jira story object containing details.
        Returns:
            list: A list of generated test cases for the Jira story.
        """
        try:
            system_prompt = promptManager.get_system_prompt("generate_jira_test_cases")
            user_prompt = promptManager.format_user_prompt(
                "generate_jira_test_cases",
                story_id=story.key,
                summary=story.summary,
                description=story.description
            )
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            model = self.llm.get_chat_model()
            agent = create_react_agent(model, tools=[], response_format="json")
            response = await agent.ainvoke({"messages": messages})
            
            if not response or 'messages' not in response:
                raise ValueError("No messages found in the response.")
            
            ai_messages = [msg for msg in response['messages'] if isinstance(msg, AIMessage)]
            if not ai_messages:
                raise ValueError("No messages found in the response.")
            last_ai_message = ai_messages[-1]
            llm_response = last_ai_message.content
            
            print(f"LLM Response: {llm_response}")
            return llm_response
            
        except Exception as e:
            print(f"Error generating test cases: {str(e)}")
            return e
    
    async def stream_jira_test_cases(self, story_id: str) -> AsyncGenerator[str]:
        """
        Generate test cases for a Jira story using the provided story ID.
        Args:
            story_id (str): The ID of the Jira story to generate test cases for.
        Returns:
            AsyncGenerator[str]: A generator yielding test cases as strings.
        """
        try:
            jira_story = await JiraStoryAgent(
                model_name=self.model_name,
                llm_base_url=self.llm_base_url,
                llm_api_key=self.llm_api_key,
                temperature=self.temperature
            ).get_jira_story_details(story_id)
            
            if isinstance(jira_story, Exception):
                yield str(jira_story)
                return
            
            system_prompt = promptManager.get_system_prompt("generate_jira_test_cases")
            user_prompt = promptManager.format_user_prompt("generate_jira_test_cases",
                story_id=jira_story.key,
                summary=jira_story.summary,
                description=jira_story.description
            )
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]

            model = self.llm.get_chat_model()
            agent = create_react_agent(model, tools=[])
            async for token, metadata in agent.astream({"messages": messages}, stream_mode="messages"):
                yield token.content
            
        except Exception as e:
            print(f"Error generating test cases: {str(e)}")
            yield str(e)
        