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
            Generate {number} test cases and ensure to include both positive and negative scenarios, including edge cases.
            Output format: {format}
            Example output:
            {example_output}
            At the end, ask the user for any questions or any further specific test cases to generate."""
        }
    )
    
    generate_jira_test_cases_instruct: PromptTemplate = Field(
        default={
            "system": """You are a member of a QA team responsible for testing an application. Using the JIRA story information provided, generate comprehensive test scenarios that combine exploratory testing with story-driven approaches.""",
            "user": """## CONTEXT DESCRIPTION:
            ~JIRA Story Summary:~
            {summary}
            ~JIRA Story Description:~ 
            {description}
            
            ## OBJECTIVE
            Based on the context provided, please generate in-depth, specific exploratory test scenarios that target critical functionalities, unexpected behaviors, and key edge cases.
            You analysis and identify various scenarios including happy paths, sad paths, exceptional edge case scenarios, and associate each scenario with a priority level for implementation.
            Choose priorities of high, medium or low to determine the order in which scenario should be implemented, and list those with high priority first.

            ## Instructions
            You will create at least one scenario for each path.
            You will respond with a specific format: Markdown or Table or JSON format.
            You will check if I have provided any specific format for you to respond, otherwise you will use Markdown format.
            Markdown format with brief description, given/when/then sentence, priority, putting each part of the scenario in a new line.
            Table format with the columns: Number, brief description, GIVEN-WHEN-THEN-scenario sentence, suggestion of a priority level.
            Json format with properties title, test case, Given-When-Then sentence, priority.
            {user_instructions}
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