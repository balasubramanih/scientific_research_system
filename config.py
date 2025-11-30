import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    """
    Centralized configuration management for the application.
    Loads from environment variables with sensible defaults.
    """
    
    # Google API Key
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Model Configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash-lite")
    
    # Execution Mode: 'parallel' or 'sequential'
    EXECUTION_MODE = os.getenv("EXECUTION_MODE", "sequential").lower()
    
    # Application Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))

    @classmethod
    def validate(cls):
        """Validates critical configuration."""
        if not cls.GOOGLE_API_KEY:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")

# Expose variables directly for backward compatibility if needed, 
# or prefer using Config.VARIABLE
GOOGLE_API_KEY = Config.GOOGLE_API_KEY
MODEL_NAME = Config.MODEL_NAME
EXECUTION_MODE = Config.EXECUTION_MODE

# Validate on import
Config.validate()
