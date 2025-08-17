"""
MCP (Model Context Protocol) Server Implementation
Provides tools for the agent to interact with external systems
"""

import json
import os
from typing import Any, Dict, List, Optional
from mcp import Server, Tool
from pydantic import BaseModel
import asyncio


class FileReadTool(BaseModel):
    """Tool to read file contents"""
    file_path: str


class FileWriteTool(BaseModel):
    """Tool to write content to file"""
    file_path: str
    content: str


class ListDirectoryTool(BaseModel):
    """Tool to list directory contents"""
    directory_path: str = "."


class WebSearchTool(BaseModel):
    """Tool to perform web searches"""
    query: str
    max_results: int = 5


class MCPServer:
    def __init__(self):
        self.server = Server("demo-chatbot-mcp")
        self.setup_tools()
    
    def setup_tools(self):
        """Setup available tools for the MCP server"""
        
        @self.server.tool()
        async def read_file(file_path: str) -> Dict[str, Any]:
            """Read contents of a file"""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {"success": True, "content": content}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.server.tool()
        async def write_file(file_path: str, content: str) -> Dict[str, Any]:
            """Write content to a file"""
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return {"success": True, "message": f"File written to {file_path}"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.server.tool()
        async def list_directory(directory_path: str = ".") -> Dict[str, Any]:
            """List contents of a directory"""
            try:
                items = os.listdir(directory_path)
                files = []
                dirs = []
                for item in items:
                    item_path = os.path.join(directory_path, item)
                    if os.path.isfile(item_path):
                        files.append(item)
                    else:
                        dirs.append(item)
                return {
                    "success": True,
                    "files": files,
                    "directories": dirs,
                    "path": os.path.abspath(directory_path)
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.server.tool()
        async def search_web(query: str, max_results: int = 5) -> Dict[str, Any]:
            """Perform a web search (mock implementation)"""
            # This is a mock implementation
            # In real implementation, integrate with actual search APIs
            mock_results = [
                {"title": f"Result {i+1} for '{query}'", "url": f"https://example.com/result{i+1}"}
                for i in range(max_results)
            ]
            return {"success": True, "results": mock_results}
    
    async def start(self):
        """Start the MCP server"""
        await self.server.run()


if __name__ == "__main__":
    server = MCPServer()
    asyncio.run(server.start())