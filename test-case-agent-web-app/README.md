# Test Case Agent Web App

A Streamlit-based web application for generating test cases from Jira stories using AI.

## Features

- Enter a Jira story key and generate test cases automatically.
- Supports multiple output formats (Markdown, Table, JSON).
- Option to generate test scripts for various frameworks.
- Custom instructions for tailored test case generation.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd test-case-agent-web-app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env` and set `API_BASE_URL` as needed.

4. **Run the app:**
   ```bash
   streamlit run src/app.py
   ```

## Configuration

- Edit `src/config/settings.py` or use the `.env` file to set API endpoints and other settings.

## Requirements

- Python 3.13+
- See `requirements.txt` for Python package dependencies.

## License

MIT License.
