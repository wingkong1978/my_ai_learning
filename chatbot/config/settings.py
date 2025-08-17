"""
Configuration settings for the demo chatbot.
"""
import os
from typing import Optional
from pathlib import Path

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file."""
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    os.environ[key] = value

# Load .env file
load_env_file()

class Config:
    """Base configuration class."""
    
    # API Configuration
    MOONSHOT_API_KEY: Optional[str] = os.getenv("MOONSHOT_API_KEY")
    MOONSHOT_BASE_URL: str = "https://api.moonshot.cn/v1"
    
    # Model Configuration
    DEFAULT_MODEL: str = "moonshot-v1-8k"
    DEFAULT_TEMPERATURE: float = 0.8
    DEFAULT_MAX_TOKENS: int = 100
    
    # LangChain Configuration
    LANGCHAIN_MODEL: str = "kimi-latest"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.MOONSHOT_API_KEY:
            raise ValueError("MOONSHOT_API_KEY is required. Please check your .env file.")
        return True

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG: bool = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG: bool = False

# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}