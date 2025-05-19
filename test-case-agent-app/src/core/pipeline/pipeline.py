"""
Main Test Case agent pipeline implementation.
"""

from ..llm.chat_openai_llm import ChatLLM
from ..llm.chat_groq_llm import ChatLLM as ChatGroqLLM
from ..prompts.prompt_manager import promptManager

class TestCasePipeline:
    def __init__(self, model_name, llm_base_url, llm_api_key, temperature):
        self.llm = ChatGroqLLM(
            model_name=model_name,
            llm_api_key=llm_api_key,
            temperature=temperature
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
        prompts = promptManager.get_prompt("get_jira_story")
        print(prompts["system"], prompts["user"])
        response = await self.llm.get_response(
            system_message=prompts["system"],
            user_message=prompts["user"]
        )
        return {
            "key": story_id,
            "summary": "Not Available",
            "description": "Not Available",
            "status": "Not Available"
        } if not response else response
        
    def generate_test_cases(self):
        # Placeholder for actual implementation
        ...