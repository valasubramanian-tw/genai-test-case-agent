# GenAI Test Case Agent Application

The GenAI Test Case Agent is a FastAPI-based application that leverages AI and MCP features to generate test cases and integrates with Jira for story management.

## Features
- **Jira Integration**: Fetch Jira story details using story IDs.
- **AI-Powered Test Case Generation**: Uses Groq's LLM to generate test cases.
- **Extensible Architecture**: Built with modular components for easy customization.

### Key Components
- **LLM Integration**: Uses LangChain's `ChatOpenAI` for AI-powered responses.
- **Prompt Management**: Centralized prompt templates for consistent communication with the LLM.
- **Jira MCP Client**: Handles Jira API interactions.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

## License
This project is licensed under the MIT License.
