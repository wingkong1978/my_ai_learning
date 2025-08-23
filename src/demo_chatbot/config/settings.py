"""
Configuration settings for the demo chatbot.

Provides:
- Environment-based configuration with validation
- Type-safe configuration classes
- Default value management
- Configuration validation and error reporting
- Support for multiple environments (dev, prod, test)
"""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Environment(str, Enum):
    """Supported deployment environments."""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class LogLevel(str, Enum):
    """Supported log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings:
    """Main configuration settings for the demo chatbot.
    
    Provides environment-based configuration with validation and type safety.
    """
    
    def __init__(self, **overrides):
        """Initialize settings with environment variables and overrides."""
        # Environment Configuration
        self.environment = Environment(os.getenv("CHATBOT_ENV", Environment.DEVELOPMENT.value))
        self.debug = self._get_bool("DEBUG", False)
        
        # API Configuration
        self.moonshot_api_key = os.getenv("MOONSHOT_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.moonshot_base_url = os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1")
        
        # Model Configuration
        self.default_model = os.getenv("DEFAULT_MODEL", "kimi-latest")
        self.temperature = self._get_float("TEMPERATURE", 0.7, 0.0, 2.0)
        self.max_tokens = self._get_int("MAX_TOKENS", 1000, 1, 32000)
        
        # MCP Server Configuration
        self.mcp_server_name = os.getenv("MCP_SERVER_NAME", "demo-chatbot-mcp")
        self.mcp_host = os.getenv("MCP_HOST", "localhost")
        self.mcp_port = self._get_int("MCP_PORT", 8080, 1, 65535)
        
        # File System Configuration
        self.working_directory = self._get_path("WORKING_DIRECTORY", Path("."))
        self.max_file_size = self._get_int("MAX_FILE_SIZE", 10485760, 1)
        self.allowed_file_extensions = self._get_list("ALLOWED_FILE_EXTENSIONS", 
                                                      [".txt", ".py", ".md", ".json", ".yaml", ".yml"])
        
        # Proxy Configuration
        self.http_proxy = os.getenv("HTTP_PROXY")
        self.https_proxy = os.getenv("HTTPS_PROXY")
        
        # Logging Configuration
        self.log_level = LogLevel(os.getenv("LOG_LEVEL", LogLevel.INFO.value))
        self.log_file = self._get_path("LOG_FILE", None, required=False)
        self.structured_logging = self._get_bool("STRUCTURED_LOGGING", False)
        
        # Performance Configuration
        self.enable_performance_monitoring = self._get_bool("ENABLE_PERFORMANCE_MONITORING", False)
        self.request_timeout = self._get_int("REQUEST_TIMEOUT", 30, 1)
        
        # Security Configuration
        self.allow_file_operations = self._get_bool("ALLOW_FILE_OPERATIONS", True)
        self.restrict_to_working_directory = self._get_bool("RESTRICT_TO_WORKING_DIRECTORY", True)
        
        # Apply overrides
        for key, value in overrides.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Post-init validation
        self._post_init_validation()
    
    def _get_bool(self, key: str, default: bool) -> bool:
        """Get boolean value from environment."""
        value = os.getenv(key, "").lower()
        if value in ("true", "1", "yes", "on"):
            return True
        elif value in ("false", "0", "no", "off"):
            return False
        return default
    
    def _get_int(self, key: str, default: int, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
        """Get integer value from environment with validation."""
        try:
            value = int(os.getenv(key, str(default)))
            if min_val is not None and value < min_val:
                raise ValueError(f"{key} must be >= {min_val}")
            if max_val is not None and value > max_val:
                raise ValueError(f"{key} must be <= {max_val}")
            return value
        except ValueError as e:
            if "invalid literal" in str(e):
                return default
            raise
    
    def _get_float(self, key: str, default: float, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
        """Get float value from environment with validation."""
        try:
            value = float(os.getenv(key, str(default)))
            if min_val is not None and value < min_val:
                raise ValueError(f"{key} must be >= {min_val}")
            if max_val is not None and value > max_val:
                raise ValueError(f"{key} must be <= {max_val}")
            return value
        except ValueError as e:
            if "invalid literal" in str(e):
                return default
            raise
    
    def _get_path(self, key: str, default: Optional[Path], required: bool = True) -> Optional[Path]:
        """Get path value from environment with validation."""
        value = os.getenv(key)
        if not value:
            if required and default is None:
                raise ValueError(f"{key} is required but not set")
            return default
        
        path = Path(value)
        if not path.is_absolute():
            path = Path.cwd() / path
        path = path.resolve()
        
        # Create directory if it doesn't exist (for working directory)
        if key == "WORKING_DIRECTORY":
            try:
                path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise ValueError(f"Cannot create directory {path}: {e}")
        elif key == "LOG_FILE" and path:
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise ValueError(f"Cannot create log directory {path.parent}: {e}")
        
        return path
    
    def _get_list(self, key: str, default: List[str]) -> List[str]:
        """Get list value from environment."""
        value = os.getenv(key)
        if not value:
            return default
        
        items = [item.strip() for item in value.split(",")]
        # Normalize file extensions
        if "EXTENSIONS" in key:
            normalized = []
            for item in items:
                if not item.startswith("."):
                    item = f".{item}"
                normalized.append(item.lower())
            return normalized
        return items
    
    def _post_init_validation(self):
        """Perform post-initialization validation."""
        # Require API key in production
        if self.environment == Environment.PRODUCTION:
            if not self.moonshot_api_key:
                raise ValueError("MOONSHOT_API_KEY is required in production environment")
        
        # Set debug mode based on environment if not explicitly set
        if not hasattr(self, '_debug_set_explicitly'):
            if self.environment == Environment.DEVELOPMENT:
                self.debug = True
        
        # Adjust settings based on environment
        if self.environment == Environment.PRODUCTION:
            # More restrictive settings for production
            self.restrict_to_working_directory = True
            self.max_file_size = min(self.max_file_size, 5242880)  # Max 5MB in prod
        
        # Validate model name
        if not self.default_model or not isinstance(self.default_model, str):
            raise ValueError("Model name must be a non-empty string")
    
    def validate_api_key(self) -> bool:
        """Validate that required API keys are present.
        
        Returns:
            True if validation passes
            
        Raises:
            ValueError: If required API keys are missing
        """
        if not self.moonshot_api_key:
            raise ValueError(
                "MOONSHOT_API_KEY is required. Please set it in your .env file or environment variables."
            )
        return True
    
    def get_proxy_config(self) -> Dict[str, str]:
        """Get proxy configuration for HTTP requests.
        
        Returns:
            Dictionary with proxy configuration
        """
        proxy_config = {}
        if self.http_proxy:
            proxy_config["http"] = self.http_proxy
        if self.https_proxy:
            proxy_config["https"] = self.https_proxy
        return proxy_config
    
    def get_moonshot_config(self) -> Dict[str, Any]:
        """Get Moonshot AI configuration.
        
        Returns:
            Dictionary with Moonshot configuration
        """
        self.validate_api_key()
        
        return {
            "api_key": self.moonshot_api_key,
            "base_url": self.moonshot_base_url,
            "model": self.default_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.request_timeout,
            "proxies": self.get_proxy_config()
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration.
        
        Returns:
            Dictionary with logging configuration
        """
        return {
            "level": self.log_level.value,
            "file_path": str(self.log_file) if self.log_file else None,
            "structured": self.structured_logging,
            "performance_monitoring": self.enable_performance_monitoring
        }
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == Environment.DEVELOPMENT
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == Environment.PRODUCTION
    
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.environment == Environment.TESTING
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary (excluding sensitive data).
        
        Returns:
            Dictionary representation of settings
        """
        data = {}
        for key in dir(self):
            if not key.startswith('_') and not callable(getattr(self, key)):
                data[key] = getattr(self, key)
        
        # Remove sensitive information
        sensitive_keys = ["moonshot_api_key", "openai_api_key"]
        for key in sensitive_keys:
            if key in data:
                data[key] = "***" if data[key] else None
        
        # Convert Path objects to strings
        for key, value in data.items():
            if isinstance(value, Path):
                data[key] = str(value)
        
        return data
    
    class Config:
        """Configuration class."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance.
    
    Returns:
        Settings instance
    """
    return settings


def reload_settings() -> Settings:
    """Reload settings from environment variables.
    
    Returns:
        New settings instance
    """
    global settings
    load_dotenv(override=True)  # Reload .env file
    settings = Settings()
    return settings


def create_test_settings(**overrides) -> Settings:
    """Create settings instance for testing.
    
    Args:
        **overrides: Configuration overrides
        
    Returns:
        Test settings instance
    """
    test_config = {
        "environment": Environment.TESTING,
        "moonshot_api_key": "test-key",
        "working_directory": Path("/tmp/test"),
        "log_level": LogLevel.DEBUG,
        **overrides
    }
    
    return Settings(**test_config)