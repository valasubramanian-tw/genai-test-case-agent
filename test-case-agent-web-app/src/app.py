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

async def stream_test_cases(story_id: str):
    api_url = f"{settings.api_base_url}/stream/jira/{story_id}/tests"
    logger.info(f"Streaming story details from: {api_url}")

    message_container = st.empty()
    full_message = ""

    try:
        timeout = httpx.Timeout(30.0, connect=20.0) 
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream('GET', api_url) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            # Remove "data: " prefix and parse JSON
                            data = json.loads(line[6:])
                            if data["type"] == "message":
                                # Accumulate the content
                                full_message += data["content"]
                                # Update the message container with the accumulated content
                                message_container.markdown(full_message)
                        except json.JSONDecodeError as e:
                            st.error(f"Error parsing response: {e}")
    except httpx.TimeoutException as e:
        st.error(f"Request timed out: {e}")
        logger.error(f"Timeout error: {e}")
    except httpx.HTTPStatusError as e:
        st.error(f"HTTP error: {e}")
        logger.error(f"HTTP error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        logger.error(f"Unexpected error: {e}")
                        
async def fetch_story_details(story_key: str) -> Optional[Dict[str, Any]]:
    if not story_key:
        logger.error("Empty story key provided")
        st.error("Please enter a valid Jira story key")
        return None
        
    api_url = f"{settings.api_base_url}/jira/{story_key}/details"
    logger.info(f"Fetching story details from: {api_url}")
    
    async with httpx.AsyncClient() as client:
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
    if 'test_cases' not in st.session_state:
        st.session_state.test_cases = None

async def main():
    """Main application function."""
    st.title("Test Case Agent App")
    st.write("Your personal assistant for automating test cases generation.")
    st.divider()

    # Initialize session state
    init_session_state()

    # Input field for Jira story key
    story_key = st.text_input(
        "Enter Jira Story Key:", 
        value="RETAILPRD-1", 
        placeholder="e.g., PROJ-123"
    ).strip()
    
    if st.button("Generate Test Cases", key="generate_test_cases"):
        if story_key:
            with st.spinner("Generating test cases..."):
                # Stream the test cases
                await stream_test_cases(story_key)

if __name__ == "__main__":
    asyncio.run(main())