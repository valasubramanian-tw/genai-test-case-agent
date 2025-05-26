import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    # General settings
    app_name: str = "Test Case Web Agent"
    version: str = "1.0.0"
    description: str = "A web interface for managing test cases and stories."
    
    # Logging settings
    log_level: str = "INFO"

    # API settings
    api_base_url: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    
settings = Settings()