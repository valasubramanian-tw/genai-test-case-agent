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
