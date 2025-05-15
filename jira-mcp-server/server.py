import os
import jira
import logging
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = "jira-mcp-server/1.0"
ATLASSIAN_API_KEY = os.getenv("ATLASSIAN_API_KEY")
ATLASSIAN_SERVER_URL = os.getenv("ATLASSIAN_SERVER_URL")
ATLASSIAN_USER_NAME = os.getenv("ATLASSIAN_USER_NAME")

mcp = FastMCP("jira-mcp-server", "1.0")

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
        jira_client = jira.JIRA(
            server=ATLASSIAN_SERVER_URL,
            basic_auth=(ATLASSIAN_USER_NAME, ATLASSIAN_API_KEY))
        story = jira_client.issue(key)
        story_data = {
            "key": story.key,
            "summary": story.fields.summary,
            "description": story.fields.description,
            "status": story.fields.status.name
        }
        return story_data
    except jira.exceptions.JIRAError as e:
        logging.info(f"An error occurred: {e}")
        return None
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mcp.run()