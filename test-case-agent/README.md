# Test Case Agent API

A FastAPI-based Agentic AI application that generates test cases using MCP, integrating with Jira for story details.

## Setup

### Prerequisites
- Python 3.8+
- uv
- FastAPI
- Streamlit
- LLM provider API key
- LangChain
- LangGraph

### Installation
```bash
# Clone the repository
git clone <repository-url>

# Install dependencies
uv add -r requirements.txt

# Set up environment variables
export LLM_API_KEY=<your-api-key>
export LLM_BASE_URL=<your-llm-base-url>
export LLM_MODEL=<your-llm-model>
```

## API Documentation

### Endpoints

#### Get Jira Story Details
```
GET /jira/story/{story_id}
```
Retrieves details for a specific Jira story.

**Response Format:**
```json
{
    "key": "story identifier",
    "summary": "brief story summary",
    "description": "detailed story description",
    "status": "current story status"
}
```

## Project Structure

```
test-case-agent-app/
├── src/
│   ├── api/        # FastAPI application
│   ├── core/       # Core business logic
│   │   ├── agent/  # Test case agent implementation
│   │   ├── llm/    # LLM integration
│   │   └── prompts/# Prompt templates
│   └── web/        # Streamlit based Web application
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
- OpenAI or Ollama as the LLM provider
- Pydantic for data validation
