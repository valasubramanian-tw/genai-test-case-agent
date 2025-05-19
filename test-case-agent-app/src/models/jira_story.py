from pydantic import BaseModel

class JiraStory(BaseModel):
    id: str
    title: str
    description: str
    status: str