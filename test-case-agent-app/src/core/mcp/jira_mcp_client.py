from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "JIRA MCP Server": {
            "command": "/opt/homebrew/bin/uv",
            "args": [
                "run",
                "--with",
                "mcp[cli]",
                "mcp",
                "run",
                "/Users/valasubramanian/Documents/source/repos/ai/gen-ai/genai-test-case-agent/jira-mcp-server/server.py"
            ],
            "transport": "stdio",
        }
    }
)