"""
Tests for configuration management.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch

from demo_chatbot.config.settings import Settings, settings


class TestSettings:
    """Test cases for Settings"""
    
    def test_default_settings(self):
        """Test default settings values"""
        assert Settings.DEFAULT_MODEL == "kimi-latest"
        assert Settings.TEMPERATURE == 0.7
        assert Settings.MAX_TOKENS == 1000
        assert Settings.MCP_SERVER_NAME == "demo-chatbot-mcp"
        assert Settings.MCP_PORT == 8080
    
    def test_environment_override(self):
        """Test environment variable overrides"""
        test_env = {
            'DEFAULT_MODEL': 'test-model',
            'TEMPERATURE': '0.5',
            'MAX_TOKENS': '500',
            'MCP_PORT': '9000',
            'WORKING_DIRECTORY': '/tmp/test',
            'ALLOWED_FILE_EXTENSIONS': '.py,.js,.html'
        }
        
        with patch.dict('os.environ', test_env):
            assert Settings.DEFAULT_MODEL == 'test-model'
            assert Settings.TEMPERATURE == 0.5
            assert Settings.MAX_TOKENS == 500
            assert Settings.MCP_PORT == 9000
            assert Settings.WORKING_DIRECTORY == Path('/tmp/test')
            assert Settings.ALLOWED_FILE_EXTENSIONS == ['.py', '.js', '.html']
    
    def test_validate_success(self):
        """Test successful validation"""
        with patch.dict('os.environ', {'MOONSHOT_API_KEY': 'test-key'}):
            assert Settings.validate() is True
    
    def test_validate_failure(self):
        """Test validation failure"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="MOONSHOT_API_KEY"):
                Settings.validate()
    
    def test_proxy_config(self):
        """Test proxy configuration"""
        test_env = {
            'HTTP_PROXY': 'http://proxy:8080',
            'HTTPS_PROXY': 'https://proxy:8443'
        }
        
        with patch.dict('os.environ', test_env):
            proxy_config = Settings.get_proxy_config()
            assert proxy_config['http'] == 'http://proxy:8080'
            assert proxy_config['https'] == 'https://proxy:8443'
    
    def test_no_proxy_config(self):
        """Test proxy configuration when no proxies are set"""
        with patch.dict('os.environ', {}, clear=True):
            proxy_config = Settings.get_proxy_config()
            assert proxy_config == {}
    
    def test_settings_instance(self):
        """Test that settings instance is properly created"""
        assert settings is not None
        assert isinstance(settings, Settings)