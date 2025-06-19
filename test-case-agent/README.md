# Test Case Agent API

A FastAPI-based Agentic AI application that generates test cases using MCP, integrating with Jira for story details.

## Setup

### Prerequisites
- Python 3.8+
- [uv](https://github.com/astral-sh/uv)
- FastAPI
- Streamlit
- LLM provider API key (OpenAI, Ollama, Groq, etc.)
- LangChain
- LangGraph

### Installation
```bash
# Clone the repository
git clone <repository-url>

# Install dependencies
uv add -r requirements.txt

# Set up environment variables (see .env.example or below)
export LLM_API_KEY=<your-api-key>
export LLM_BASE_URL=<your-llm-base-url>
export LLM_MODEL=<your-llm-model>
```

## Environment Variables

Create a `.env` file in the root directory with the following content:
```
LLM_BASE_URL=http://localhost:11434
LLM_API_KEY=sk-not-needed
LLM_MODEL=llama3.2:latest
LLM_TEMPERATURE=0.7
```

## API Documentation

### Endpoints

#### Get Jira Story Details
```
GET /jira/{story_id}/details
```
Retrieves details for a specific Jira story.

**Response Format:**
```json
{
    "response": {
        "key": "story identifier",
        "summary": "brief story summary",
        "description": "detailed story description",
        "status": "current story status"
    }
}
```

#### Generate Test Cases by Story ID
```
GET /jira/{story_id}/tests
```
Generates test cases for a Jira story by its ID.

**Response Format:**
```json
{
    "response": "<test cases in requested format or error>"
}
```

#### Generate Test Cases by Story Object
```
POST /jira/tests
```
Request body:
```json
{
    "story": {
        "key": "story identifier",
        "summary": "story summary",
        "description": "story description",
        "status": "story status"
    },
    "format": "markdown",
    "limit": 10
}
```
**Response Format:**
```json
{
    "response": "<test cases in requested format or error>"
}
```

#### Streaming Test Cases
```
POST /stream/jira/tests
GET /stream/jira/{story_id}/tests
```
Returns a streaming response (SSE) with generated test cases.

## Project Structure

```
test-case-agent/
├── src/
│   ├── app.py            # FastAPI application
│   ├── config/           # Configuration and settings
│   ├── core/
│   │   ├── agent/        # Agent implementations
│   │   ├── llm/          # LLM integrations (OpenAI, Ollama, Groq)
│   │   ├── prompts/      # Prompt templates and examples
│   │   └── tools/        # MCP/Jira tool integrations
│   ├── models/           # Pydantic models
│   └── web/              # Streamlit-based web application
├── requirements.txt
├── .env
├── README.md
```

## Running the FastAPI Application

```bash
# Start the FastAPI server
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

Access the API documentation at: http://localhost:8000/docs

## Running the Streamlit Web Application
```bash
streamlit run src/web/app.py
```

## Development

- The application uses FastAPI for the REST API
- LangChain for LLM integration
- LangGraph for Agentic AI development
- Supports OpenAI, Ollama, and Groq as LLM providers
- Pydantic for data validation

## Notes

- For local LLMs (like Ollama), ensure the model is downloaded and running.
- For MCP/Jira integration, ensure the MCP server is accessible and configured.
- The API supports both synchronous and streaming endpoints for test case generation.
