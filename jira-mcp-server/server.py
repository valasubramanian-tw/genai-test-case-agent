"""
https://github.com/open-webui/mcpo

uvx mcpo --port 4000 --config /Users/valasubramanian/Documents/source/repos/ai/gen-ai/genai-test-case-agent/jira-mcp-server/config.json
"""
import os
import httpx
import logging
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from urllib.parse import urljoin, quote

load_dotenv()
logging.basicConfig(level=logging.INFO)

USER_AGENT = "jira-mcp-server/1.0"
ATLASSIAN_API_KEY = os.getenv("ATLASSIAN_API_KEY")
ATLASSIAN_SERVER_URL = os.getenv("ATLASSIAN_SERVER_URL")
ATLASSIAN_USER_NAME = os.getenv("ATLASSIAN_USER_NAME")

mcp = FastMCP("JIRA MCP Server")

@mcp.tool()
async def get_jira_story_details(key: str) -> dict | None:
    """
        Get the details of a JIRA story from the JIRA API.
        This function takes a JIRA story key as input and returns the details of the story.
        The details include summary, description, status, etc.
        Args:
            key (str): The JIRA story key.
        Returns:
            dict: The details of the JIRA story.
            None: If the story is not found or an error occurs.
    """
    if ATLASSIAN_API_KEY is None or ATLASSIAN_SERVER_URL is None or ATLASSIAN_USER_NAME is None:
        logging.info("Missing required environment variables.")
        return None
    
    if not key:
        logging.info("No JIRA story key provided.")
        return None
    
    try:
        logging.info(f"Initializing JIRA client for story retrieval.")
        async with httpx.AsyncClient() as client:
            url = urljoin(ATLASSIAN_SERVER_URL, f"/rest/api/2/issue/{key}")
            headers = {
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            }
            response = await client.get(
                url=url,
                headers=headers,
                timeout=30.0,
                auth=(ATLASSIAN_USER_NAME, ATLASSIAN_API_KEY)
            )
            response.raise_for_status()
            story = response.json()
            story_data = {
                "key": story["key"],
                "summary": story["fields"]["summary"],
                "description": story["fields"]["description"],
                "status": story["fields"]["status"]["name"]
            }
            return story_data
    except httpx.HTTPStatusError as e:
        logging.info(f"An error occurred: {e}")
        return None
    except httpx.RequestError as e:
        logging.info(f"An unexpected error occurred: {e}")  
        return None
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")
        return None
    return None

if __name__ == "__main__":
    mcp.run()