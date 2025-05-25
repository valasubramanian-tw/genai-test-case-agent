"""
FastAPI application for Test case agent.

uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
ssh -R 80:localhost:55372 serveo.net
"""
import json
import logging
import uvicorn
from typing import Any
from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI(title="Test Case Agent Service")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/jira/comments")
async def get_jira_comments():
    return [
        {
            "id": "1",
            "author": "user1",
            "body": "This is a comment on the Jira story.",
            "created_at": "2023-10-01T12:00:00Z"
        },
        {
            "id": "2",
            "author": "user2",
            "body": "This is another comment on the Jira story.",
            "created_at": "2023-10-02T12:00:00Z"
        }
    ]
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=0)