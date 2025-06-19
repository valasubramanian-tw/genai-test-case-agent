from pydantic import BaseModel, Field
from typing import List

class JiraStory(BaseModel):
    key: str = Field(description="The key of the Jira story")
    summary: str = Field(description="The title of the Jira story")
    description: str = Field(description="The description of the Jira story.")
    status: str = Field(description="The status of the Jira story")
    
class JiraStoryError(BaseModel):
    error: str
    
class JiraStoryResponse(BaseModel):
    response: JiraStory | JiraStoryError
    
class JiraTestCaseResponse(BaseModel):
    response: str | JiraStoryError
    
class JiraTestCaseRequest(BaseModel):
    story: JiraStory
    format: str = Field(default="markdown", description="The format of the test cases to be generated. Default is markdown.")
    limit: int = Field(default=10, description="The maximum number of test cases to generate. Default is 10.")
