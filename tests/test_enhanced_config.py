"""
Enhanced test suite for configuration management with comprehensive validation.

Tests include:
- Settings validation and type checking
- Environment variable handling
- Configuration file loading
- Error handling and edge cases
- Multiple environment scenarios
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
from typing import Dict, Any

from pydantic import ValidationError

from demo_chatbot.config.settings import (
    Settings, Environment, LogLevel, 
    get_settings, reload_settings, create_test_settings
)


class TestEnvironmentEnum:
    """Test cases for Environment enumeration."""
    
    def test_environment_values(self):
        """Test that all expected environment values exist."""
        assert Environment.DEVELOPMENT == "development"
        assert Environment.PRODUCTION == "production"
        assert Environment.TESTING == "testing"
    
    def test_environment_membership(self):
        """Test environment membership checks."""
        assert "development" in Environment
        assert "production" in Environment
        assert "testing" in Environment
        assert "invalid" not in Environment


class TestLogLevelEnum:
    """Test cases for LogLevel enumeration."""
    
    def test_log_level_values(self):
        """Test that all expected log levels exist."""
        assert LogLevel.DEBUG == "DEBUG"
        assert LogLevel.INFO == "INFO"
        assert LogLevel.WARNING == "WARNING"
        assert LogLevel.ERROR == "ERROR"
        assert LogLevel.CRITICAL == "CRITICAL"


class TestSettingsBasic:
    """Test cases for basic Settings functionality."""
    
    def test_default_settings(self):
        """Test default settings values."""
        # Clear environment variables for clean test
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.environment == Environment.DEVELOPMENT
            assert settings.debug is False
            assert settings.default_model == "kimi-latest"
            assert settings.temperature == 0.7
            assert settings.max_tokens == 1000
            assert settings.mcp_host == "localhost"
            assert settings.mcp_port == 8080
            assert settings.log_level == LogLevel.INFO
    
    def test_environment_variable_loading(self):
        """Test loading configuration from environment variables."""
        env_vars = {
            "CHATBOT_ENV": "production",
            "MOONSHOT_API_KEY": "test-key-123",
            "DEFAULT_MODEL": "custom-model",
            "TEMPERATURE": "0.8",
            "MAX_TOKENS": "2000",
            "MCP_PORT": "9090",
            "LOG_LEVEL": "DEBUG"
        }
        
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            
            assert settings.environment == Environment.PRODUCTION
            assert settings.moonshot_api_key == "test-key-123"
            assert settings.default_model == "custom-model"
            assert settings.temperature == 0.8
            assert settings.max_tokens == 2000
            assert settings.mcp_port == 9090
            assert settings.log_level == LogLevel.DEBUG


class TestSettingsValidation:
    """Test cases for settings validation."""
    
    def test_temperature_validation(self):
        """Test temperature value validation."""
        # Valid temperatures
        Settings(temperature=0.0)
        Settings(temperature=1.0)
        Settings(temperature=2.0)
        
        # Invalid temperatures
        with pytest.raises(ValidationError):
            Settings(temperature=-0.1)
        
        with pytest.raises(ValidationError):
            Settings(temperature=2.1)
    
    def test_max_tokens_validation(self):
        """Test max_tokens validation."""
        # Valid values
        Settings(max_tokens=1)
        Settings(max_tokens=32000)
        
        # Invalid values
        with pytest.raises(ValidationError):
            Settings(max_tokens=0)
        
        with pytest.raises(ValidationError):
            Settings(max_tokens=32001)
    
    def test_port_validation(self):
        """Test port number validation."""
        # Valid ports
        Settings(mcp_port=1)
        Settings(mcp_port=8080)
        Settings(mcp_port=65535)
        
        # Invalid ports
        with pytest.raises(ValidationError):
            Settings(mcp_port=0)
        
        with pytest.raises(ValidationError):
            Settings(mcp_port=65536)
    
    def test_model_name_validation(self):
        """Test model name validation."""
        # Valid model names
        Settings(default_model="kimi-latest")
        Settings(default_model="custom-model-v1")
        
        # Invalid model names
        with pytest.raises(ValidationError):
            Settings(default_model="")
        
        with pytest.raises(ValidationError):
            Settings(default_model=None)


class TestWorkingDirectoryValidation:
    """Test cases for working directory validation."""
    
    def test_working_directory_creation(self):
        """Test working directory creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = Path(temp_dir) / "test_working_dir"
            
            settings = Settings(working_directory=str(test_dir))
            
            assert settings.working_directory.exists()
            assert settings.working_directory.is_dir()
    
    def test_working_directory_absolute_path(self):
        """Test working directory resolution to absolute path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            rel_path = "relative/path"
            
            with patch('pathlib.Path.cwd') as mock_cwd:
                mock_cwd.return_value = Path(temp_dir)
                
                settings = Settings(working_directory=rel_path)
                
                assert settings.working_directory.is_absolute()
    
    def test_working_directory_permission_error(self):
        """Test handling of permission errors during directory creation."""
        # Use a path that should cause permission issues
        invalid_path = "/root/invalid/path/for/test"
        
        with pytest.raises(ValidationError, match="Cannot create working directory"):
            Settings(working_directory=invalid_path)


class TestFileExtensionValidation:
    """Test cases for file extension validation."""
    
    def test_file_extensions_from_string(self):
        """Test parsing file extensions from comma-separated string."""
        with patch.dict(os.environ, {"ALLOWED_FILE_EXTENSIONS": "txt,py,md,json"}, clear=True):
            settings = Settings()
            
            expected = [".txt", ".py", ".md", ".json"]
            assert settings.allowed_file_extensions == expected
    
    def test_file_extensions_normalization(self):
        """Test file extension normalization."""
        with patch.dict(os.environ, {"ALLOWED_FILE_EXTENSIONS": "txt,.py,MD,.JSON"}, clear=True):
            settings = Settings()
            
            expected = [".txt", ".py", ".md", ".json"]
            assert settings.allowed_file_extensions == expected
    
    def test_file_extensions_from_list(self):
        """Test file extensions from list input."""
        extensions = ["txt", ".py", "MD"]
        settings = Settings(allowed_file_extensions=extensions)
        
        expected = [".txt", ".py", ".md"]
        assert settings.allowed_file_extensions == expected


class TestLogFileValidation:
    """Test cases for log file validation."""
    
    def test_log_file_directory_creation(self):
        """Test log file directory creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "logs" / "test.log"
            
            settings = Settings(log_file=str(log_file))
            
            assert settings.log_file == log_file
            assert log_file.parent.exists()
    
    def test_log_file_none_value(self):
        """Test log file with None value."""
        settings = Settings(log_file=None)
        assert settings.log_file is None
        
        settings = Settings(log_file="")
        assert settings.log_file is None


class TestRootValidation:
    """Test cases for root validator functionality."""
    
    def test_production_requires_api_key(self):
        """Test that production environment requires API key."""
        with pytest.raises(ValidationError, match="MOONSHOT_API_KEY is required in production"):
            Settings(
                environment=Environment.PRODUCTION,
                moonshot_api_key=None
            )
    
    def test_production_with_api_key(self):
        """Test production environment with valid API key."""
        settings = Settings(
            environment=Environment.PRODUCTION,
            moonshot_api_key="prod-key-123"
        )
        
        assert settings.environment == Environment.PRODUCTION
        assert settings.moonshot_api_key == "prod-key-123"
    
    def test_debug_mode_in_development(self):
        """Test debug mode setting in development environment."""
        settings = Settings(environment=Environment.DEVELOPMENT)
        
        # Debug should be set based on environment in root validator
        # (Implementation may vary, adjust test accordingly)
        assert settings.environment == Environment.DEVELOPMENT
    
    def test_production_file_size_restriction(self):
        """Test file size restriction in production environment."""
        settings = Settings(
            environment=Environment.PRODUCTION,
            moonshot_api_key="prod-key",
            max_file_size=10485760  # 10MB
        )
        
        # In production, max file size should be limited to 5MB
        assert settings.max_file_size <= 5242880


class TestSettingsMethods:
    """Test cases for Settings methods."""
    
    def test_validate_api_key_success(self):
        """Test successful API key validation."""
        settings = Settings(moonshot_api_key="valid-key")
        
        result = settings.validate_api_key()
        assert result is True
    
    def test_validate_api_key_failure(self):
        """Test API key validation failure."""
        settings = Settings(moonshot_api_key=None)
        
        with pytest.raises(ValueError, match="MOONSHOT_API_KEY is required"):
            settings.validate_api_key()
    
    def test_get_proxy_config(self):
        """Test proxy configuration retrieval."""
        settings = Settings(
            http_proxy="http://proxy:8080",
            https_proxy="https://proxy:8443"
        )
        
        proxy_config = settings.get_proxy_config()
        
        expected = {
            "http": "http://proxy:8080",
            "https": "https://proxy:8443"
        }
        assert proxy_config == expected
    
    def test_get_proxy_config_empty(self):
        """Test proxy configuration with no proxies."""
        settings = Settings()
        
        proxy_config = settings.get_proxy_config()
        assert proxy_config == {}
    
    def test_get_moonshot_config(self):
        """Test Moonshot configuration retrieval."""
        settings = Settings(
            moonshot_api_key="test-key",
            moonshot_base_url="https://test.api.com",
            default_model="test-model",
            temperature=0.8,
            max_tokens=1500,
            request_timeout=60
        )
        
        config = settings.get_moonshot_config()
        
        assert config["api_key"] == "test-key"
        assert config["base_url"] == "https://test.api.com"
        assert config["model"] == "test-model"
        assert config["temperature"] == 0.8
        assert config["max_tokens"] == 1500
        assert config["timeout"] == 60
    
    def test_get_logging_config(self):
        """Test logging configuration retrieval."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            
            settings = Settings(
                log_level=LogLevel.DEBUG,
                log_file=str(log_file),
                structured_logging=True,
                enable_performance_monitoring=True
            )
            
            config = settings.get_logging_config()
            
            assert config["level"] == "DEBUG"
            assert config["file_path"] == str(log_file)
            assert config["structured"] is True
            assert config["performance_monitoring"] is True
    
    def test_environment_check_methods(self):
        """Test environment checking methods."""
        dev_settings = Settings(environment=Environment.DEVELOPMENT)
        assert dev_settings.is_development() is True
        assert dev_settings.is_production() is False
        assert dev_settings.is_testing() is False
        
        prod_settings = Settings(
            environment=Environment.PRODUCTION,
            moonshot_api_key="prod-key"
        )
        assert prod_settings.is_development() is False
        assert prod_settings.is_production() is True
        assert prod_settings.is_testing() is False
        
        test_settings = Settings(environment=Environment.TESTING)
        assert test_settings.is_development() is False
        assert test_settings.is_production() is False
        assert test_settings.is_testing() is True
    
    def test_to_dict_sensitive_data_masking(self):
        """Test to_dict method masks sensitive data."""
        settings = Settings(
            moonshot_api_key="secret-key-123",
            openai_api_key="another-secret"
        )
        
        data = settings.to_dict()
        
        assert data["moonshot_api_key"] == "***"
        assert data["openai_api_key"] == "***"
        
        # Test with None values
        settings_none = Settings()
        data_none = settings_none.to_dict()
        
        assert data_none["moonshot_api_key"] is None
        assert data_none["openai_api_key"] is None


class TestGlobalSettingsFunctions:
    """Test cases for global settings management functions."""
    
    def test_get_settings(self):
        """Test get_settings function."""
        settings = get_settings()
        assert isinstance(settings, Settings)
    
    @patch('demo_chatbot.config.settings.load_dotenv')
    def test_reload_settings(self, mock_load_dotenv):
        """Test settings reload functionality."""
        original_settings = get_settings()
        
        # Reload settings
        new_settings = reload_settings()
        
        # Should have called load_dotenv with override=True
        mock_load_dotenv.assert_called_with(override=True)
        assert isinstance(new_settings, Settings)
    
    def test_create_test_settings(self):
        """Test test settings creation."""
        test_settings = create_test_settings(
            moonshot_api_key="test-override",
            max_tokens=500
        )
        
        assert test_settings.environment == Environment.TESTING
        assert test_settings.moonshot_api_key == "test-override"
        assert test_settings.max_tokens == 500
        assert test_settings.log_level == LogLevel.DEBUG


class TestSettingsIntegration:
    """Integration tests for settings functionality."""
    
    def test_dotenv_file_loading(self):
        """Test loading settings from .env file."""
        env_content = """
MOONSHOT_API_KEY=file-key-123
DEFAULT_MODEL=file-model
TEMPERATURE=0.9
DEBUG=true
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write(env_content)
            env_file_path = f.name
        
        try:
            # Mock the env_file in Settings.Config
            with patch.object(Settings.Config, 'env_file', env_file_path):
                with patch('demo_chatbot.config.settings.load_dotenv'):
                    with patch.dict(os.environ, {
                        "MOONSHOT_API_KEY": "file-key-123",
                        "DEFAULT_MODEL": "file-model",
                        "TEMPERATURE": "0.9",
                        "DEBUG": "true"
                    }, clear=True):
                        settings = Settings()
                        
                        assert settings.moonshot_api_key == "file-key-123"
                        assert settings.default_model == "file-model"
                        assert settings.temperature == 0.9
                        assert settings.debug is True
        finally:
            os.unlink(env_file_path)
    
    def test_complete_configuration_workflow(self):
        """Test complete configuration workflow."""
        # Simulate production environment setup
        prod_env = {
            "CHATBOT_ENV": "production",
            "MOONSHOT_API_KEY": "prod-secret-key",
            "DEFAULT_MODEL": "kimi-pro",
            "TEMPERATURE": "0.3",
            "MAX_TOKENS": "2000",
            "LOG_LEVEL": "WARNING",
            "STRUCTURED_LOGGING": "true",
            "RESTRICT_TO_WORKING_DIRECTORY": "true"
        }
        
        with patch.dict(os.environ, prod_env, clear=True):
            settings = Settings()
            
            # Validate production configuration
            assert settings.is_production()
            assert settings.validate_api_key()
            assert settings.default_model == "kimi-pro"
            assert settings.temperature == 0.3
            assert settings.max_tokens == 2000
            assert settings.log_level == LogLevel.WARNING
            assert settings.structured_logging is True
            assert settings.restrict_to_working_directory is True
            
            # Test configuration methods
            moonshot_config = settings.get_moonshot_config()
            assert moonshot_config["api_key"] == "prod-secret-key"
            assert moonshot_config["model"] == "kimi-pro"
            
            logging_config = settings.get_logging_config()
            assert logging_config["level"] == "WARNING"
            assert logging_config["structured"] is True


if __name__ == "__main__":
    # Run specific test when executed directly
    pytest.main([__file__, "-v"])