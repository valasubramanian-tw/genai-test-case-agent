"""
FastAPI application for Test case agent.

uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
"""
import json
import logging
from typing import Any
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessageChunk
from ..core.agent.test_case_agent import TestCasAgent
from .models.jira_story import JiraStoryResponse, JiraStoryError
from ..config.settings import settings

apiPrefix = settings.api_prefix
# Initialize FastAPI app
app = FastAPI(title="Test Case Agent Service")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageEncoder(json.JSONEncoder):
    """Custom JSON encoder for AI message chunks."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, AIMessageChunk):
            return {
                "type": "message",
                "content": obj.content,
                "additional_kwargs": obj.additional_kwargs
            }
        return super().default(obj)
    
try:
    agent = TestCasAgent(
        model_name=settings.llm_model,
        llm_base_url=settings.llm_base_url,
        llm_api_key=settings.llm_api_key,
        temperature=settings.llm_temperature
    )
except Exception as e:
    print(f"Error initializing TestCasAgent: {e}")
    raise

@app.get("/jira/story/{story_id}", response_model=JiraStoryResponse)
async def get_jira_story(story_id: str) -> JiraStoryResponse:
    """
    Get a Jira story by its ID.
    """
    try:
        agent_response = await agent.get_jira_story_details(story_id)
        return JiraStoryResponse(response=agent_response)
    except Exception as e:
        print(f"Error fetching Jira story details: {e}")
        return JiraStoryResponse(response=JiraStoryError(error=str(e)))
    
@app.get("/stream/jira/story/{story_id}")
async def stream_jira_story(story_id: str):
    """
    Stream the response of fetching a Jira story by its ID.
    
    Args:
        story_id: The ID of the Jira story to fetch
        
    Returns:
        StreamingResponse: A streaming response containing the story details
    """
    async def generate():
        try:
            async for chunk in agent.stream_jira_story_details(story_id):
                logger.info(f"Streaming chunk: {type(chunk)}")
                # Convert chunk to JSON string and add newline as delimiter
                chunk_json = json.dumps(
                    chunk, 
                    cls=MessageEncoder,
                    ensure_ascii=False
                ) + "\n"
                yield chunk_json
        except Exception as e:
            logger.error(f"Error streaming Jira story details: {e}")
            yield json.dumps({
                "type": "error",
                "content": str(e)
            }) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
        headers={
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "no-cache"
        }
    )