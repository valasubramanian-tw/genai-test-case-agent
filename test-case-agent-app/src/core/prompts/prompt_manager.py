from pydantic import BaseModel, Field
from typing import TypedDict

class PromptTemplate(TypedDict):
    system: str
    user: str

class PromptManager(BaseModel):
    get_jira_story: PromptTemplate = Field(
        default={
            "system": """You are an AI assistant specialized in processing Jira stories. Return all responses as valid JSON without any additional text or formatting.""",
            "user": """For Jira story ID: AIFSDET-1, return story details in this exact JSON structure:
{"id": "story identifier", "title": "story title", "description": "detailed story description", "status": "current story status"}

Use "Not Available" for any missing fields. Return only the JSON object."""
        }
    )
    
    def get_prompt(self, prompt_name: str) -> PromptTemplate:
        """Get both system and user prompts for a given prompt name."""
        return getattr(self, prompt_name)
    
    def format_user_prompt(self, prompt_name: str, **kwargs) -> str:
        """Get formatted user prompt for a given prompt name."""
        prompt = self.get_prompt(prompt_name)
        return prompt["user"].format(**kwargs)

    class Config:
        frozen = True

promptManager = PromptManager()