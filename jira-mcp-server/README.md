# JIRA MCP Server

A Model Context Protocol (MCP) server that provides an interface to fetch JIRA story details from the JIRA API.

## Features
- Fetch JIRA story details including summary, description, and status
- Supports both direct HTTP API and JIRA SDK implementations
- Easy integration with Claude Desktop via MCP

## Prerequisites
- Python 3.13 or higher
- UV package manager
- Atlassian JIRA access

## Installation

1. Clone and setup the environment:
```bash
git clone <repository-url>
cd jira-mcp-server
uv venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv add -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file with:
```env
ATLASSIAN_SERVER_URL=https://your-domain.atlassian.net
ATLASSIAN_USER_NAME=your-email@domain.com
ATLASSIAN_API_KEY=your-api-token
```

## Usage

### Running the Server

Start the server using either:

```bash
# Direct HTTP implementation
uv run server.py

# Or using JIRA SDK implementation
uv run server-sdk.py
```

### Debug Mode
For debugging, use the MCP inspector:
```bash
npx @modelcontextprotocol/inspector uv run server.py
```

### Install in Claude Desktop
```bash
uv run mcp install server.py
```

### API Reference

The server exposes the following MCP tool:

#### get_jira_story_details
Fetches details of a JIRA story.

**Parameters:**
- `key` (string): JIRA issue key (e.g., "PROJECT-123")

**Returns:**
- `dict`: Story details containing:
  - `key`: Issue key
  - `summary`: Issue summary
  - `description`: Full description
  - `status`: Current status
- `None`: If story not found or error occurs

## License
MIT

## Contributing
Pull requests are welcome. Please ensure tests pass before submitting.