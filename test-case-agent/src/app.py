"""
FastAPI application for Test case agent.

uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
ssh -R 80:localhost:8000 serveo.net
"""
import json
import logging
from typing import Any
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .core.agent.test_case_agent import TestCaseAgent
from .core.agent.jira_story_agent import JiraStoryAgent
from .models.jira_story import JiraStoryResponse, JiraStoryError, JiraTestCaseResponse
from .config.settings import settings

apiPrefix = settings.api_prefix
# Initialize FastAPI app
app = FastAPI(title="Test Case Agent Service")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    agent = TestCaseAgent(
        model_name=settings.llm_model,
        llm_base_url=settings.llm_base_url,
        llm_api_key=settings.llm_api_key,
        temperature=settings.llm_temperature
    )
    jiraAgent = JiraStoryAgent(
        model_name=settings.llm_model,
        llm_base_url=settings.llm_base_url,
        llm_api_key=settings.llm_api_key,
        temperature=settings.llm_temperature
    )
except Exception as e:
    print(f"Error initializing TestCasAgent: {e}")
    raise

@app.get("/jira/{story_id}/details", response_model=JiraStoryResponse)
async def get_jira_story(story_id: str) -> JiraStoryResponse:
    """
    Get a Jira story by its ID.
    """
    try:
        agent_response = await jiraAgent.get_jira_story_details(story_id)
        return JiraStoryResponse(response=agent_response)
    except Exception as e:
        print(f"Error fetching Jira story details: {e}")
        return JiraStoryResponse(response=JiraStoryError(error=str(e)))
    
@app.get("/jira/{story_id}/tests", response_model=JiraTestCaseResponse)
async def get_jira_test_cases(story_id: str) -> JiraTestCaseResponse:
    """
    Generate test cases for a Jira story by its ID.
    Args:
        story_id: The ID of the Jira story to generate test cases for.
    Returns:
        JiraTestCaseResponse: A response containing the generated test cases or an error.
    """
    try:
        agent_response = await agent.get_jira_test_cases(story_id)
        return JiraTestCaseResponse(response=agent_response)
    except Exception as e:
        print(f"Error generating tests for Jira issue: {e}")
        return JiraTestCaseResponse(response=JiraStoryError(error=str(e)))
    
@app.get("/stream/jira/{story_id}/tests")
async def stream_jira_test_cases(story_id: str):
    """
    Generate test cases for a Jira story by its ID as streaming response.
    Args:
        story_id: The ID of the Jira story to generate test cases for.
    Returns:
        StreamingResponse: A streaming response containing the generated test cases.
    """
    async def generate():
        try:
            async for chunk in agent.stream_jira_test_cases(story_id):
                event_data = json.dumps({
                    "type": "message",
                    "content": chunk
                }, ensure_ascii=False)
                yield f"data: {event_data}\n\n"
        except Exception as e:
            logger.error(f"Error streaming test cases: {e}")
            error_data = json.dumps({
                "type": "error",
                "content": str(e)
            })
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
            "X-Accel-Buffering": "no"
        }
    )