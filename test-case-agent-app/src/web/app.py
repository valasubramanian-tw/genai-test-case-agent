import httpx
import os
import logging
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_test_cases(story_details: dict):
    st.divider()
    st.subheader("Test Cases:")
    st.success("Test cases generated successfully!")
    st.write("1. Verify that the user can add an expense with valid inputs.")
    st.write("2. Verify that the user cannot add an expense with an invalid amount.")
    st.write("3. Verify that the user cannot add an expense with a future expenditure date.")

def fetch_story_details(story_key: str):
    story_details = {
        "story_key": story_key,
        "summary": "Add expense section",
        "description": """As a user, I want to add an expense section with an amount, category, and expenditure date, so that I can track my expenses.
            \nFeatures:
            \n- Amount - number field
            \n- Category - dropdown (Values: Food, Rent, EMI, Entertainment, Transport, Clothing, Others)""",
        "acceptance_criteria": [
            "Given the user is on the add expense screen, When the user inputs amount, category, and expenditure date, Then the expense is added successfully.",
            "Given the user inputs an invalid amount, When they try to add the expense, Then they see an error message indicating amount must be a positive decimal number. ",
            "Given the user inputs a future expenditure date, When they try to add the expense, Then they see an error message indicating date must not be in the future.",
        ],
        "status": "Ready for Development",
        "priority": "High",
    }
    return story_details

st.title("Test Case Agent App")
st.write("Your personal assistant for automating test cases generation.")
st.divider()

# Initialize session state
if 'story_details' not in st.session_state:
    st.session_state.story_details = None

# Input field for Jira story key
story_key = st.text_input("Enter Jira Story Key:", value="PROJ-123", placeholder="e.g., PROJ-123")

if st.button("Fetch Story Details", key="fetch_story_details"):
    if story_key:
        with st.spinner("Fetching story details..."):
            st.session_state.story_details = fetch_story_details(story_key)

# Display story details and test case generation button
if st.session_state.story_details:
    st.divider()
    st.subheader("Story Details:")
    st.write(f"JIRA Number: {st.session_state.story_details.get('story_key')}")
    st.write(f"Status: {st.session_state.story_details.get('status')}")
    st.write(f"Summary: {st.session_state.story_details.get('summary')}")
    st.write(f"Description:")
    st.write(f"{st.session_state.story_details.get('description')}")
    st.write(f"Acceptance Criteria:")
    for criteria in st.session_state.story_details.get('acceptance_criteria', []):
        st.write(f"- {criteria}")
    
    generate_tests = st.button("Generate Test Cases", key="generate_test_cases")
    if generate_tests:
        with st.spinner("Generating test cases..."):
            fetch_test_cases(st.session_state.story_details)