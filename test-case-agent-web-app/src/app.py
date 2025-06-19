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

async def stream_test_cases(story_id: str, format: str = "Markdown", number: int = 5) -> None:
    api_url = f"{settings.api_base_url}/stream/jira/{story_id}/tests?format={format}&limit={number}"
    logger.info(f"Streaming story details from: {api_url}")

    message_container = st.empty()
    full_message = ""

    try:
        timeout = httpx.Timeout(60.0, connect=20.0)
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
    """ Create a left sidebar with the title and description."""
    st.sidebar.title("AI-Powered Test Case Agent")
    st.sidebar.write("From Stories to Test Cases – Automatically generate test cases from your user stories.")
    st.sidebar.write("Transform acceptance criteria into actionable test cases in one click.")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.text_input(
        "**:blue[Atlassian URL: ]**",
            placeholder="e.g., myaccount.atlassian.net",
            value="twks.atlassian.net",
        ).strip()
    st.sidebar.text_input(
        "**:blue[Atlassian API Key: ]**",
            placeholder="e.g., ****************",
            value="****************",
            type="password"
        ).strip()

    # Initialize session state
    init_session_state()

    # Group input fields in the same row using columns
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        story_key = st.text_input(
            "**:blue[Enter Jira Story Number: ]**", 
            placeholder="e.g., PROJ-123"
        ).strip()
    with col2:
        format = st.selectbox(
            "Select Output Format:",
            options=["Markdown", "Table", "JSON"],
            index=0,
            help="Choose the format for the generated test cases."
        )
    with col3:
        number = st.number_input(
            "Number of Test Cases to Generate:",
            min_value=5,
            max_value=20,
            value=10,
            help="Specify how many test cases you want to generate."
        )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        custom_instructions = st.text_input(
            "Custom Instructions (optional):",
            placeholder="Add any specific instructions for generating test cases."
        )
    with col2:
        st.write("")  # One line of space
        st.write("")  # Another line of space
        generate_clicked = st.button("Generate Test Cases", key="generate_test_cases", type="primary")

    if generate_clicked:
        if story_key:
            with st.spinner("Generating test cases..."):
                await stream_test_cases(story_key, format, number)
            
            with st.container():
                col1 = st.columns(1)[0]
                col1.write("")
                col1.chat_input(
                    placeholder="Ask a question or any specific test cases to generate"
                )
                col1.write("")
            
            with st.container():
                col1, col2, = st.columns([3, 1])
                framework = col1.selectbox(
                    "**Select Framework:**",
                    options=["Python - Pytest", "Java - JUnit", "React - Jest", "C# - MSTest", "Ruby - RSpec", "JavaScript - Mocha"],
                    index=0,
                    help="Choose the framework for the generated test script files."
                )
                col2.write("")
                col2.write("")
                col2.button("Generate Test Scripts", key="generate_test_scripts", type="primary")
            

if __name__ == "__main__":
    asyncio.run(main())