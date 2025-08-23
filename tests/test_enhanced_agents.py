"""
Enhanced test suite for LangGraph Agent with comprehensive coverage.

Tests include:
- Agent initialization and configuration
- Tool functionality and error handling
- Conversation memory and threading
- Performance and edge cases
- Mock testing for external dependencies
"""

import pytest
import asyncio
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any

from demo_chatbot.agents.langgraph_agent import LangGraphAgent, AgentConfig, AgentState
from demo_chatbot.config.settings import create_test_settings
from demo_chatbot.utils.logger import setup_logger


class TestAgentConfig:
    """Test cases for AgentConfig validation."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = AgentConfig()
        
        assert config.model_name == "kimi-latest"
        assert config.temperature == 0.7
        assert config.max_tokens == 1000
        assert config.max_file_size == 10485760
        assert ".txt" in config.allowed_extensions
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Valid config
        config = AgentConfig(
            model_name="test-model",
            temperature=0.5,
            max_tokens=500
        )
        assert config.model_name == "test-model"
        
        # Invalid model name
        with pytest.raises(ValueError):
            AgentConfig(model_name="")
        
        # Invalid temperature
        with pytest.raises(ValueError):
            AgentConfig(temperature=3.0)
        
        # Invalid max_tokens
        with pytest.raises(ValueError):
            AgentConfig(max_tokens=0)


class TestLangGraphAgent:
    """Test cases for LangGraphAgent functionality."""
    
    @pytest.fixture
    def mock_settings(self):
        """Create mock settings for testing."""
        return create_test_settings(
            moonshot_api_key="test-key-123",
            working_directory=Path(tempfile.mkdtemp()),
            max_file_size=1024,
            allowed_file_extensions=[".txt", ".json"]
        )
    
    @pytest.fixture
    def agent_config(self):
        """Create test agent configuration."""
        return AgentConfig(
            model_name="test-model",
            temperature=0.5,
            max_tokens=100,
            max_file_size=1024
        )
    
    @patch('demo_chatbot.agents.langgraph_agent.settings')
    def test_agent_initialization(self, mock_settings_module, mock_settings, agent_config):
        """Test agent initialization with proper configuration."""
        mock_settings_module.return_value = mock_settings
        
        with patch('demo_chatbot.agents.langgraph_agent.MoonshotChat') as mock_chat:
            mock_chat.return_value = Mock()
            
            agent = LangGraphAgent(agent_config)
            
            assert agent.config == agent_config
            assert agent.llm is not None
            assert len(agent.tools) == 5  # Expected number of tools
            assert agent.graph is not None
    
    @patch('demo_chatbot.agents.langgraph_agent.settings')
    def test_agent_initialization_failure(self, mock_settings_module, mock_settings):
        """Test agent initialization failure handling."""
        # Mock missing API key
        mock_settings.moonshot_api_key = None
        mock_settings_module.return_value = mock_settings
        
        with pytest.raises(ValueError, match="MOONSHOT_API_KEY is required"):
            LangGraphAgent()
    
    @patch('demo_chatbot.agents.langgraph_agent.settings')
    async def test_agent_run_basic(self, mock_settings_module, mock_settings, agent_config):
        """Test basic agent run functionality."""
        mock_settings_module.return_value = mock_settings
        
        with patch('demo_chatbot.agents.langgraph_agent.MoonshotChat') as mock_chat:
            # Setup mock LLM
            mock_llm = Mock()
            mock_chat.return_value = mock_llm
            
            # Mock the graph invoke method
            mock_response = Mock()
            mock_response.content = "Test response"
            
            with patch.object(LangGraphAgent, '_create_graph') as mock_graph:
                mock_graph_instance = Mock()
                mock_graph_instance.invoke.return_value = {
                    "messages": [mock_response],
                    "error": None
                }
                mock_graph.return_value = mock_graph_instance
                
                agent = LangGraphAgent(agent_config)
                response = await agent.run("Test input")
                
                assert response == "Test response"
    
    async def test_agent_run_empty_input(self):
        """Test agent behavior with empty input."""
        with patch('demo_chatbot.agents.langgraph_agent.settings') as mock_settings:
            mock_settings.moonshot_api_key = "test-key"
            
            with patch('demo_chatbot.agents.langgraph_agent.MoonshotChat'):
                agent = LangGraphAgent()
                
                with pytest.raises(ValueError, match="User input cannot be empty"):
                    await agent.run("")
    
    @patch('demo_chatbot.agents.langgraph_agent.settings')
    async def test_agent_error_handling(self, mock_settings_module, mock_settings, agent_config):
        """Test agent error handling during execution."""
        mock_settings_module.return_value = mock_settings
        
        with patch('demo_chatbot.agents.langgraph_agent.MoonshotChat'):
            with patch.object(LangGraphAgent, '_create_graph') as mock_graph:
                # Mock graph to raise exception
                mock_graph_instance = Mock()
                mock_graph_instance.invoke.side_effect = Exception("Test error")
                mock_graph.return_value = mock_graph_instance
                
                agent = LangGraphAgent(agent_config)
                response = await agent.run("Test input")
                
                assert "error" in response.lower()


class TestAgentTools:
    """Test cases for agent tools functionality."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        return Path(tempfile.mkdtemp())
    
    @pytest.fixture
    async def agent(self, temp_dir):
        """Create agent instance for tool testing."""
        config = AgentConfig(
            max_file_size=1024,
            allowed_extensions=[".txt", ".json"]
        )
        
        with patch('demo_chatbot.agents.langgraph_agent.settings') as mock_settings:
            mock_settings.moonshot_api_key = "test-key"
            mock_settings.working_directory = temp_dir
            
            with patch('demo_chatbot.agents.langgraph_agent.MoonshotChat'):
                agent = LangGraphAgent(config)
                return agent
    
    async def test_file_reader_tool(self, agent, temp_dir):
        """Test file reader tool functionality."""
        # Create test file
        test_file = temp_dir / "test.txt"
        test_content = "Hello, World!"
        test_file.write_text(test_content)
        
        # Get file reader tool
        file_reader = agent.tools[0]  # Assuming first tool is file_reader
        
        # Test reading existing file
        result = file_reader.invoke({"file_path": str(test_file)})
        assert test_content in result
        
        # Test reading non-existent file
        result = file_reader.invoke({"file_path": "nonexistent.txt"})
        assert "Error" in result
    
    async def test_file_writer_tool(self, agent, temp_dir):
        """Test file writer tool functionality."""
        # Get file writer tool
        file_writer = agent.tools[1]  # Assuming second tool is file_writer
        
        test_file = temp_dir / "output.txt"
        test_content = "Test content"
        
        # Test writing file
        result = file_writer.invoke({
            "file_path": str(test_file),
            "content": test_content
        })
        
        assert "Successfully" in result
        assert test_file.exists()
        assert test_file.read_text() == test_content
    
    async def test_calculator_tool(self, agent):
        """Test calculator tool functionality."""
        # Get calculator tool
        calculator = agent.tools[3]  # Assuming calculator is 4th tool
        
        # Test valid calculation
        result = calculator.invoke({"expression": "2 + 2"})
        assert "4" in result
        
        # Test invalid expression
        result = calculator.invoke({"expression": "import os"})
        assert "Error" in result
        
        # Test division by zero
        result = calculator.invoke({"expression": "1/0"})
        assert "Error" in result
    
    async def test_directory_listing_tool(self, agent, temp_dir):
        """Test directory listing tool functionality."""
        # Create test files
        (temp_dir / "file1.txt").write_text("content1")
        (temp_dir / "file2.txt").write_text("content2")
        (temp_dir / "subdir").mkdir()
        
        # Get directory listing tool
        list_dir = agent.tools[2]  # Assuming list_directory is 3rd tool
        
        result = list_dir.invoke({"directory_path": str(temp_dir)})
        
        assert "file1.txt" in result
        assert "file2.txt" in result
        assert "subdir" in result
    
    async def test_web_search_tool(self, agent):
        """Test web search tool functionality."""
        # Get web search tool
        web_search = agent.tools[4]  # Assuming web_search is 5th tool
        
        result = web_search.invoke({"query": "test query"})
        
        assert "Search results" in result
        assert "test query" in result


class TestAgentConversation:
    """Test cases for conversation memory and threading."""
    
    @pytest.fixture
    async def agent(self):
        """Create agent for conversation testing."""
        with patch('demo_chatbot.agents.langgraph_agent.settings') as mock_settings:
            mock_settings.moonshot_api_key = "test-key"
            
            with patch('demo_chatbot.agents.langgraph_agent.MoonshotChat'):
                return LangGraphAgent()
    
    async def test_different_thread_isolation(self, agent):
        """Test that different threads maintain separate conversations."""
        with patch.object(agent.graph, 'invoke') as mock_invoke:
            mock_response = Mock()
            mock_response.content = "Response"
            mock_invoke.return_value = {
                "messages": [mock_response],
                "error": None
            }
            
            # Test different thread IDs
            await agent.run("Hello", thread_id="user1")
            await agent.run("Hello", thread_id="user2")
            
            # Verify graph was called with different thread configs
            assert mock_invoke.call_count == 2
            
            call_configs = [call[0][1] for call in mock_invoke.call_args_list]
            assert call_configs[0]["configurable"]["thread_id"] == "user1"
            assert call_configs[1]["configurable"]["thread_id"] == "user2"
    
    async def test_conversation_history_methods(self, agent):
        """Test conversation history management methods."""
        # Test get_conversation_history
        history = agent.get_conversation_history("test_thread")
        assert isinstance(history, list)
        
        # Test clear_conversation
        result = agent.clear_conversation("test_thread")
        assert isinstance(result, bool)


class TestAgentPerformance:
    """Test cases for agent performance and edge cases."""
    
    @pytest.fixture
    async def agent(self):
        """Create agent for performance testing."""
        config = AgentConfig(max_tokens=50)  # Small tokens for testing
        
        with patch('demo_chatbot.agents.langgraph_agent.settings') as mock_settings:
            mock_settings.moonshot_api_key = "test-key"
            
            with patch('demo_chatbot.agents.langgraph_agent.MoonshotChat'):
                return LangGraphAgent(config)
    
    async def test_concurrent_requests(self, agent):
        """Test agent handling concurrent requests."""
        with patch.object(agent.graph, 'invoke') as mock_invoke:
            mock_response = Mock()
            mock_response.content = "Concurrent response"
            mock_invoke.return_value = {
                "messages": [mock_response],
                "error": None
            }
            
            # Create multiple concurrent requests
            tasks = [
                agent.run(f"Request {i}", thread_id=f"thread_{i}")
                for i in range(3)
            ]
            
            responses = await asyncio.gather(*tasks)
            
            assert len(responses) == 3
            assert all("Concurrent response" in response for response in responses)
    
    async def test_large_input_handling(self, agent):
        """Test agent handling of large inputs."""
        large_input = "A" * 10000  # Very large input
        
        with patch.object(agent.graph, 'invoke') as mock_invoke:
            mock_response = Mock()
            mock_response.content = "Large input handled"
            mock_invoke.return_value = {
                "messages": [mock_response],
                "error": None
            }
            
            response = await agent.run(large_input)
            assert response == "Large input handled"
    
    @pytest.mark.asyncio
    async def test_streaming_functionality(self, agent):
        """Test agent streaming capabilities."""
        with patch.object(agent.graph, 'stream') as mock_stream:
            # Mock streaming chunks
            mock_chunks = [
                {"agent": "chunk1"},
                {"tools": "chunk2"},
                {"agent": "chunk3"}
            ]
            
            async def async_generator():
                for chunk in mock_chunks:
                    yield chunk
            
            mock_stream.return_value = async_generator()
            
            chunks = []
            async for chunk in agent.stream("Test streaming"):
                chunks.append(chunk)
            
            assert len(chunks) == 3


class TestAgentIntegration:
    """Integration tests for complete agent workflows."""
    
    @pytest.fixture
    async def real_agent(self):
        """Create agent with more realistic setup for integration testing."""
        # Use test configuration that's closer to real usage
        test_settings = create_test_settings(
            moonshot_api_key="test-integration-key"
        )
        
        with patch('demo_chatbot.agents.langgraph_agent.get_settings') as mock_get_settings:
            mock_get_settings.return_value = test_settings
            
            with patch('demo_chatbot.agents.langgraph_agent.MoonshotChat') as mock_chat:
                # Create a more realistic mock
                mock_llm = Mock()
                mock_llm.bind_tools.return_value = mock_llm
                mock_chat.return_value = mock_llm
                
                agent = LangGraphAgent()
                
                # Mock the graph with more realistic behavior
                with patch.object(agent, 'graph') as mock_graph:
                    mock_graph.invoke.return_value = {
                        "messages": [Mock(content="Integration test response")],
                        "current_step": "completed",
                        "error": None
                    }
                    
                    yield agent
    
    async def test_complete_workflow(self, real_agent):
        """Test complete agent workflow from input to output."""
        test_input = "Hello, can you help me with a file operation?"
        
        response = await real_agent.run(test_input, thread_id="integration_test")
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert "Integration test response" in response
    
    async def test_error_recovery(self, real_agent):
        """Test agent error recovery in integration scenarios."""
        # Simulate an error during processing
        with patch.object(real_agent.graph, 'invoke') as mock_invoke:
            mock_invoke.side_effect = Exception("Simulated error")
            
            response = await real_agent.run("Test error recovery")
            
            assert "error" in response.lower()


if __name__ == "__main__":
    # Run specific test when executed directly
    pytest.main([__file__, "-v"])