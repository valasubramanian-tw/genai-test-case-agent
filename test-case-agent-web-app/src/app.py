"""
Test Case Agent App
Streamlit application for generating test cases based on Jira stories.

Usage:
    streamlit run src/app.py
"""
import json
import httpx
import asyncio
import logging
import streamlit as st
from typing import Optional, Dict, Any
from config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example client code
async def stream_story_details(story_id: str):
    api_url = f"{settings.api_base_url}/stream/jira/story/{story_id}"
    logger.info(f"Streaming story details from: {api_url}")
    
    timeout_settings = httpx.Timeout(
        connect=5.0, # Maximum time to wait for connection establishment
        read=90.0, # Maximum time to wait for reading data
        write=10.0, # Maximum time to wait for writing data
        pool=2.0 # Maximum time to wait for connection from pool
    )
    try:
        async with httpx.AsyncClient(timeout=timeout_settings) as client:
            async with client.stream('GET', api_url) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            if chunk.get("type") == "error":
                                st.error(chunk["content"])
                                break
                            elif chunk.get("type") == "intermediate":
                                st.info(f"Processing: {chunk['content']}")
                            else:
                                st.write("Story Update:", chunk)
                        except json.JSONDecodeError as e:
                            st.error(f"Error parsing response: {e}")
    except httpx.TimeoutException as e:
        st.error(f"Request timed out: {e}")
        logger.error(f"Timeout error: {e}")
        return None
    except httpx.HTTPStatusError as e:
        st.error(f"HTTP error: {e}")
        logger.error(f"HTTP error: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        logger.error(f"Unexpected error: {e}")
        return None
                        
async def fetch_story_details(story_key: str) -> Optional[Dict[str, Any]]:
    """
    Fetch story details from the API.
    
    Args:
        story_key: The Jira story key to fetch details for
        
    Returns:
        Optional[Dict[str, Any]]: Story details if successful, None otherwise
    """
    if not story_key:
        logger.error("Empty story key provided")
        st.error("Please enter a valid Jira story key")
        return None
        
    api_url = f"{settings.api_base_url}/jira/story/{story_key}"
    logger.info(f"Fetching story details from: {api_url}")
    
    timeout_settings = httpx.Timeout(
        connect=5.0, # Maximum time to wait for connection establishment
        read=90.0, # Maximum time to wait for reading data
        write=10.0, # Maximum time to wait for writing data
        pool=2.0 # Maximum time to wait for connection from pool
    )
    
    async with httpx.AsyncClient(timeout=timeout_settings) as client:
        try:
            response = await client.get(api_url)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error: {e}")
            st.error(f"Request timed out: {e}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            st.error(f"Failed to fetch story details: {e}")
        except Exception as e:
            logger.error(f"Error fetching story details: {e}")
            st.error(f"An unexpected error occurred: {e}")
        return None

def init_session_state() -> None:
    """Initialize session state variables."""
    if 'story_details' not in st.session_state:
        st.session_state.story_details = None

def display_story_details(story_details: Dict[str, Any]) -> None:
    """
    Display the story details in the Streamlit UI.
    
    Args:
        story_details: Dictionary containing story information
    """
    st.divider()
    st.subheader("Story Details:")
    st.write(f"JIRA Number: {story_details.get('key', 'N/A')}")
    st.write(f"Status: {story_details.get('status', 'N/A')}")
    st.write(f"Title: {story_details.get('title', 'N/A')}")
    st.write("Description:")
    st.write(story_details.get('description', 'No description available'))
    st.write("Acceptance Criteria:")
    for criteria in story_details.get('acceptance_criteria', []):
        st.write(f"- {criteria}")

def main():
    """Main application function."""
    st.title("Test Case Agent App")
    st.write("Your personal assistant for automating test cases generation.")
    st.divider()

    # Initialize session state
    init_session_state()

    # Input field for Jira story key
    story_key = st.text_input(
        "Enter Jira Story Key:", 
        value="PROJ-123", 
        placeholder="e.g., PROJ-123"
    ).strip()

    if st.button("Fetch Story Details", key="fetch_story_details"):
        if story_key:
            with st.spinner("Fetching story details..."):
                # Run async function in sync context
                result = asyncio.run(fetch_story_details(story_key))
                story_details = result['response'] if result['response'] else None
                if story_details:
                    st.session_state.story_details = story_details

    # Display story details if available
    if st.session_state.story_details:
        display_story_details(st.session_state.story_details)

if __name__ == "__main__":
    main()