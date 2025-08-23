"""
Tests for LangGraph integration
"""

import pytest
import asyncio
import os
from unittest.mock import Mock, patch

from chatbot.api.langgraph.langgraph_client import LangGraphChatClient
from chatbot.api.langgraph.langgraph_workflows import ChatWorkflow, ToolWorkflow, AdvancedWorkflow


class TestLangGraphIntegration:
    """Test suite for LangGraph integration"""
    
    @pytest.fixture
    def api_key(self):
        """Test API key"""
        return "test-api-key"
    
    @pytest.fixture
    def mock_api_key(self):
        """Mock API key for testing"""
        return "sk-test123456789"
    
    def test_langgraph_client_initialization(self, mock_api_key):
        """Test LangGraph client initialization"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            client = LangGraphChatClient()
            assert client.api_key == mock_api_key
            assert client.model is not None
            assert client.graph is not None
    
    def test_langgraph_client_no_api_key(self):
        """Test error when no API key is provided"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="MOONSHOT_API_KEY is required"):
                LangGraphChatClient()
    
    def test_chat_workflow_initialization(self, mock_api_key):
        """Test chat workflow initialization"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            workflow = ChatWorkflow()
            assert workflow.api_key == mock_api_key
            assert workflow.model is not None
            assert workflow.graph is not None
    
    def test_tool_workflow_initialization(self, mock_api_key):
        """Test tool workflow initialization"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            workflow = ToolWorkflow()
            assert workflow.api_key == mock_api_key
            assert workflow.model is not None
            assert workflow.tools is not None
            assert workflow.graph is not None
    
    def test_advanced_workflow_initialization(self, mock_api_key):
        """Test advanced workflow initialization"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            workflow = AdvancedWorkflow()
            assert workflow.api_key == mock_api_key
            assert workflow.langchain_client is not None
            assert workflow.openai_client is not None
            assert workflow.graph is not None
    
    @pytest.mark.asyncio
    async def test_chat_workflow_run(self, mock_api_key):
        """Test chat workflow execution"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            with patch('langchain_community.chat_models.moonshot.MoonshotChat.invoke') as mock_invoke:
                mock_invoke.return_value = Mock(content="Test response")
                
                workflow = ChatWorkflow()
                messages = [{"role": "user", "content": "Hello"}]
                response = await workflow.run(messages)
                
                assert response == "Test response"
                mock_invoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_tool_workflow_run(self, mock_api_key):
        """Test tool workflow execution"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            with patch('langchain_community.chat_models.moonshot.MoonshotChat.invoke') as mock_invoke:
                mock_invoke.return_value = Mock(content="Tool response")
                
                workflow = ToolWorkflow()
                response = await workflow.run("List files")
                
                assert response == "Tool response"
                mock_invoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_advanced_workflow_run(self, mock_api_key):
        """Test advanced workflow execution"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            with patch('langchain_community.chat_models.moonshot.MoonshotChat.invoke') as mock_invoke:
                mock_invoke.return_value = Mock(content="Advanced response")
                
                workflow = AdvancedWorkflow()
                response = await workflow.run("Compare clients")
                
                assert response == "Advanced response"
                mock_invoke.assert_called_once()
    
    def test_tools_setup(self, mock_api_key):
        """Test tools setup in tool workflow"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            workflow = ToolWorkflow()
            
            assert len(workflow.tools) >= 5
            tool_names = [tool.name for tool in workflow.tools]
            
            expected_tools = ["read_file", "write_file", "list_files", "calculate", "get_system_info"]
            for tool_name in expected_tools:
                assert tool_name in tool_names
    
    def test_client_integration(self, mock_api_key):
        """Test client integration in LangGraph client"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            client = LangGraphChatClient()
            
            assert client.langchain_client is not None
            assert client.openai_client is not None
            assert client.chat_model is not None
            assert len(client.tools) >= 3
    
    @pytest.mark.asyncio
    async def test_conversation_memory(self, mock_api_key):
        """Test conversation memory functionality"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            with patch('langchain_community.chat_models.moonshot.MoonshotChat.invoke') as mock_invoke:
                mock_invoke.return_value = Mock(content="Memory response")
                
                client = LangGraphChatClient()
                
                # Test with different thread IDs
                response1 = await client.chat("Hello", thread_id="test1")
                response2 = await client.chat("Hello", thread_id="test2")
                
                assert response1 == "Memory response"
                assert response2 == "Memory response"


class TestLangGraphExamples:
    """Test suite for LangGraph examples"""
    
    @pytest.fixture
    def mock_api_key(self):
        """Mock API key for testing"""
        return "sk-test123456789"
    
    def test_examples_initialization(self, mock_api_key):
        """Test examples initialization"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            from chatbot.examples.langgraph_examples import LangGraphExamples
            examples = LangGraphExamples()
            assert examples.api_key == mock_api_key
    
    @pytest.mark.asyncio
    async def test_basic_chat_example(self, mock_api_key):
        """Test basic chat example"""
        with patch.dict(os.environ, {'MOONSHOT_API_KEY': mock_api_key}):
            with patch('langchain_community.chat_models.moonshot.MoonshotChat.invoke') as mock_invoke:
                mock_invoke.return_value = Mock(content="Chat response")
                
                from chatbot.examples.langgraph_examples import LangGraphExamples
                examples = LangGraphExamples()
                
                # Mock the basic chat example
                client = LangGraphChatClient(api_key=mock_api_key)
                response = await client.chat("What is LangGraph?")
                assert response == "Chat response"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])