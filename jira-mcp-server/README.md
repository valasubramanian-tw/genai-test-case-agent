# JIRA MCP Server

This project provides a MCP Server to fetch the details of a JIRA story from the JIRA API.

## Features
- Retrieve JIRA story details such as summary, description, status, and more.

## Usage
The main function takes a JIRA story key as input and returns the details of the story.

**Arguments:**
- `key` (`str`): The JIRA story key.

**Returns:**
- `dict`: The details of the JIRA story.
- `None`: If the story is not found or an error occurs.

---

## Local Setup
```bash
cd jira-mcp-server
uv venv
source .venv/bin/activate
```

## Install Dependencies
```bash
uv add -r requirements.txt
```

## Environment Variables
Create a `.env` file in the `jira-mcp-server` directory with the following variables:

```env
ATLASSIAN_SERVER_URL=<your-jira-server-url>
ATLASSIAN_USER_NAME=<your-atlassian-username>
ATLASSIAN_API_KEY=<your-atlassian-api-key>
```

## Debug MCP Server
To debug the MCP server, run:
```bash
npx @modelcontextprotocol/inspector uv run server.py