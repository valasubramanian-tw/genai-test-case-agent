"""
FastAPI application for Test case agent.

uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI
from typing import List
from ..core.pipeline.pipeline import TestCasePipeline
from ..core.agent.test_case_agent import TestCasAgent
from .models.jira import JiraStoryResponse
from ..config.settings import settings

apiPrefix = settings.api_prefix
# Initialize FastAPI app

app = FastAPI(title="Test Case Agent Service")

try:
    agent = TestCasAgent(
        model_name=settings.llm_model,
        llm_base_url=settings.llm_base_url,
        llm_api_key=settings.llm_api_key,
        temperature=settings.llm_temperature
    )
except Exception as e:
    print(f"Error initializing TestCasePipeline: {e}")
    raise

@app.get("/jira/story/{story_id}", response_model=JiraStoryResponse)
async def get_jira_story(story_id: str) -> JiraStoryResponse:
    """
    Get a Jira story by its ID.
    """
    try:
        story_details = await agent.get_jira_story_details(story_id)
        return JiraStoryResponse(response=story_details)
    except Exception as e:
        print(f"Error fetching Jira story details: {e}")
        return {"error": "Failed to fetch Jira story details."}