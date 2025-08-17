"""
Tests for server implementations.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from pathlib import Path

from demo_chatbot.servers.mcp_server import MCPServer


class TestMCPServer:
    """Test cases for MCPServer"""
    
    @pytest.fixture
    def server(self):
        """Create an MCPServer instance"""
        return MCPServer()
    
    def test_server_initialization(self, server):
        """Test server initialization"""
        assert server.server is not None
        assert server.server.name == "demo-chatbot-mcp"
    
    @pytest.mark.asyncio
    async def test_read_file_tool(self, server, tmp_path):
        """Test file reading tool"""
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, MCP!")
        
        # Get the read_file tool
        tools = [tool for tool in server.server._tools.values() if tool.name == "read_file"]
        assert len(tools) == 1
        
        read_file_tool = tools[0]
        result = await read_file_tool.func(str(test_file))
        
        assert result["success"] is True
        assert result["content"] == "Hello, MCP!"
    
    @pytest.mark.asyncio
    async def test_write_file_tool(self, server, tmp_path):
        """Test file writing tool"""
        test_file = tmp_path / "output.txt"
        
        # Get the write_file tool
        tools = [tool for tool in server.server._tools.values() if tool.name == "write_file"]
        assert len(tools) == 1
        
        write_file_tool = tools[0]
        result = await write_file_tool.func(str(test_file), "Test content")
        
        assert result["success"] is True
        assert test_file.read_text() == "Test content"
    
    @pytest.mark.asyncio
    async def test_list_directory_tool(self, server, tmp_path):
        """Test directory listing tool"""
        # Create some test files and directories
        (tmp_path / "file1.txt").write_text("test")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file2.txt").write_text("test2")
        
        # Get the list_directory tool
        tools = [tool for tool in server.server._tools.values() if tool.name == "list_directory"]
        assert len(tools) == 1
        
        list_dir_tool = tools[0]
        result = await list_dir_tool.func(str(tmp_path))
        
        assert result["success"] is True
        assert len(result["files"]) == 1
        assert len(result["directories"]) == 1
        assert result["files"][0]["name"] == "file1.txt"
        assert result["directories"][0]["name"] == "subdir"
    
    @pytest.mark.asyncio
    async def test_search_web_tool(self, server):
        """Test web search tool"""
        # Get the search_web tool
        tools = [tool for tool in server.server._tools.values() if tool.name == "search_web"]
        assert len(tools) == 1
        
        search_tool = tools[0]
        result = await search_tool.func("python programming", max_results=3)
        
        assert result["success"] is True
        assert result["query"] == "python programming"
        assert len(result["results"]) == 3
        assert all("python programming" in res["title"] for res in result["results"])
    
    @pytest.mark.asyncio
    async def test_get_system_info_tool(self, server):
        """Test system info tool"""
        # Get the get_system_info tool
        tools = [tool for tool in server.server._tools.values() if tool.name == "get_system_info"]
        assert len(tools) == 1
        
        system_info_tool = tools[0]
        result = await system_info_tool.func()
        
        assert result["success"] is True
        assert "system" in result
        assert "platform" in result["system"]