import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    # General settings
    app_name: str = "Test Case Agent"
    version: str = "1.0.0"
    description: str = "A tool for managing test cases and stories."
    
    # LLM settings
    llm_model: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1/chat/completions")
    llm_api_key: str = os.getenv("LLM_API_KEY", "your_openai_api_key")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    
    # Logging settings
    log_level: str = "INFO"
    
    # API settings
    api_prefix: str = "/api/v1"
    
settings = Settings()