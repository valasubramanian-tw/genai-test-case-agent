from pydantic import BaseModel

class JiraStory(BaseModel):
    id: str
    title: str
    description: str
    status: str
    
class ErrorResponse(BaseModel):
    error: str
    
class JiraStoryResponse(BaseModel):
    response: str | JiraStory | ErrorResponse
