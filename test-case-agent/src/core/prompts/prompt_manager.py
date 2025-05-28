from pydantic import BaseModel, Field
from typing import TypedDict

class PromptTemplate(TypedDict):
    system: str
    user: str

class PromptManager(BaseModel):
    get_jira_story: PromptTemplate = Field(
        default={
            "system": """You are an AI assistant specialized in processing Jira stories. Return all responses as valid JSON without any additional text or formatting.""",
            "user": """For Jira story {story_id}, return story details including summary, description, acceptance criteria, status.
            Use "Not Available" for any missing fields."""
        }
    )
    
    generate_jira_test_cases: PromptTemplate = Field(
        default={
            "system": """You are an AI assistant specialized in generating test cases for Jira stories.""",
            "user": """For Jira story {story_id}, generate test cases based on the below story details.
            Summary: {summary}
            Description: {description}
            Return the results in tabular format with columns including No., Scenario, Test Case.
            Ensure to include both positive and negative scenarios, including edge cases in Given When Then format."""
        }
    )
    
    def get_prompt(self, prompt_name: str) -> PromptTemplate:
        """Get both system and user prompts for a given prompt name."""
        return getattr(self, prompt_name)
    
    def get_system_prompt(self, prompt_name: str) -> PromptTemplate:
        """Get system prompt for a given prompt name."""
        prompt = self.get_prompt(prompt_name)
        return prompt["system"]
    
    def format_user_prompt(self, prompt_name: str, **kwargs) -> str:
        """Get formatted user prompt for a given prompt name."""
        prompt = self.get_prompt(prompt_name)
        return prompt["user"].format(**kwargs)

    class Config:
        frozen = True

promptManager = PromptManager()