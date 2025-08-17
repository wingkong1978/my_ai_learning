"""
Configuration settings for the demo chatbot.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Configuration settings for the demo chatbot."""
    
    # API Configuration
    MOONSHOT_API_KEY: Optional[str] = os.getenv("MOONSHOT_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Model Configuration
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "kimi-latest")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1000"))
    
    # MCP Server Configuration
    MCP_SERVER_NAME: str = os.getenv("MCP_SERVER_NAME", "demo-chatbot-mcp")
    MCP_HOST: str = os.getenv("MCP_HOST", "localhost")
    MCP_PORT: int = int(os.getenv("MCP_PORT", "8080"))
    
    # File System Configuration
    WORKING_DIRECTORY: Path = Path(os.getenv("WORKING_DIRECTORY", "."))
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_FILE_EXTENSIONS: list = [
        ext.strip() for ext in os.getenv("ALLOWED_FILE_EXTENSIONS", ".txt,.py,.md,.json,.yaml,.yml").split(",")
    ]
    
    # Proxy Configuration
    HTTP_PROXY: Optional[str] = os.getenv("HTTP_PROXY")
    HTTPS_PROXY: Optional[str] = os.getenv("HTTPS_PROXY")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration settings."""
        if not cls.MOONSHOT_API_KEY:
            raise ValueError("MOONSHOT_API_KEY environment variable is required")
        return True
    
    @classmethod
    def get_proxy_config(cls) -> dict:
        """Get proxy configuration for HTTP requests."""
        proxy_config = {}
        if cls.HTTP_PROXY:
            proxy_config["http"] = cls.HTTP_PROXY
        if cls.HTTPS_PROXY:
            proxy_config["https"] = cls.HTTPS_PROXY
        return proxy_config


# Global settings instance
settings = Settings()