"""
Tests for agent implementations.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from demo_chatbot.agents.langgraph_agent import LangGraphAgent


class TestLangGraphAgent:
    """Test cases for LangGraphAgent"""
    
    @pytest.fixture
    def mock_moonshot_api_key(self):
        """Mock environment variable for Moonshot API key"""
        with patch.dict('os.environ', {'MOONSHOT_API_KEY': 'test-key-123'}):
            yield
    
    @pytest.fixture
    def agent(self, mock_moonshot_api_key):
        """Create a LangGraphAgent instance for testing"""
        with patch('demo_chatbot.agents.langgraph_agent.MoonshotChat'):
            return LangGraphAgent()
    
    def test_agent_initialization(self, agent):
        """Test agent initialization"""
        assert agent.llm is not None
        assert agent.tools is not None
        assert agent.graph is not None
        assert len(agent.tools) > 0
    
    @pytest.mark.asyncio
    async def test_basic_chat(self, agent):
        """Test basic chat functionality"""
        with patch.object(agent.llm, 'invoke') as mock_invoke:
            mock_invoke.return_value = MagicMock(content="Hello! I'm an AI assistant.")
            
            response = await agent.run("Hello")
            assert response == "Hello! I'm an AI assistant."
            mock_invoke.assert_called_once()
    
    def test_tools_setup(self, agent):
        """Test that all tools are properly set up"""
        tool_names = [tool.name for tool in agent.tools]
        expected_tools = ['file_reader', 'file_writer', 'list_directory', 'calculator', 'web_search']
        
        for tool_name in expected_tools:
            assert tool_name in tool_names
    
    def test_calculator_tool(self, agent):
        """Test calculator tool"""
        calculator_tool = next(tool for tool in agent.tools if tool.name == 'calculator')
        
        # Test valid calculation
        result = calculator_tool.func("2 + 2")
        assert result == "4"
        
        # Test invalid characters
        result = calculator_tool.func("2 + abc")
        assert "Error" in result
    
    def test_file_reader_tool(self, agent, tmp_path):
        """Test file reading tool"""
        file_reader = next(tool for tool in agent.tools if tool.name == 'file_reader')
        
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")
        
        result = file_reader.func(str(test_file))
        assert "Hello, World!" in result
    
    def test_file_writer_tool(self, agent, tmp_path):
        """Test file writing tool"""
        file_writer = next(tool for tool in agent.tools if tool.name == 'file_writer')
        
        test_file = tmp_path / "output.txt"
        result = file_writer.func(str(test_file), "Test content")
        
        assert "Successfully wrote" in result
        assert test_file.read_text() == "Test content"