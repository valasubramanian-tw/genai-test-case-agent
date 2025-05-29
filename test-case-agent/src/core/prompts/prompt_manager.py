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
            Return 5 test cases and ensure to include both positive and negative scenarios, including edge cases in below example format.
            Example format:
            Here are some test cases for RETAILPRD-1 based on the provided story details:

**Test Case 1: Successful Add Expense**

* **Title:** Add expense with valid amount, category, and date
* **Given**: The user is on the add expense screen
* **When**: The user inputs a positive decimal number for amount (e.g. $100.50), selects a valid category from the dropdown (e.g. Food), and enters a past or present date (e.g. 2023-02-15)
* **Then**: The expense is added successfully, and the user sees a confirmation message
            """
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