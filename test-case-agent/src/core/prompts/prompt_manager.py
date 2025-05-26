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
    
    generate_jira_test_cases: PromptTemplate = Field(
        default={
            "system": """You are an AI assistant specialized in generating test cases for Jira stories. Return all test cases in list of string format.""",
            "user": """For below Jira story ID: RETAILPRD-1 and title: Product Management - Add Expense, generate test cases:
As a user, I want to add an expense with an amount, category, and expenditure date, so that I can keep track of my spending.
Field Types:
Amount - number filed
Category - dropdown (Values: Food, Rent, EMI, Entertainment, Transport, Clothing, Others)
Acceptance Criteria:
Given the user is on the add expense screen,
When the user inputs amount, category, and expenditure date,
Then the expense is added successfully.
Given the user inputs an invalid amount,
When they try to add the expense,
Then they see an error message indicating amount must be a positive decimal number.
Given the user inputs a future expenditure date,
When they try to add the expense,
Then they see an error message indicating date must not be in the future."""
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