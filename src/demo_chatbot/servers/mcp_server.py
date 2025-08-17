"""
MCP (Model Context Protocol) Server Implementation
Provides tools for the agent to interact with external systems
"""

import os
import json
import asyncio
from typing import Any, Dict, List, Optional
from pathlib import Path
from mcp.server import Server
from pydantic import BaseModel


class FileReadInput(BaseModel):
    """Input for file reading tool"""
    file_path: str
    encoding: str = "utf-8"


class FileWriteInput(BaseModel):
    """Input for file writing tool"""
    file_path: str
    content: str
    encoding: str = "utf-8"


class ListDirectoryInput(BaseModel):
    """Input for directory listing tool"""
    directory_path: str = "."


class WebSearchInput(BaseModel):
    """Input for web search tool"""
    query: str
    max_results: int = 5


class MCPServer:
    """MCP Server with tool implementations"""
    
    def __init__(self):
        self.server = Server("demo-chatbot-mcp")
        self.setup_tools()
    
    def setup_tools(self):
        """Setup available tools for the MCP server"""
        
        @self.server.tool()
        async def read_file(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
            """Read contents of a file"""
            try:
                path = Path(file_path)
                if not path.exists():
                    return {"success": False, "error": "File not found"}
                
                with open(path, 'r', encoding=encoding) as f:
                    content = f.read()
                
                return {
                    "success": True,
                    "content": content,
                    "file_size": len(content),
                    "file_path": str(path.absolute())
                }
            except UnicodeDecodeError:
                return {"success": False, "error": "File encoding error"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.server.tool()
        async def write_file(file_path: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
            """Write content to a file"""
            try:
                path = Path(file_path)
                path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(path, 'w', encoding=encoding) as f:
                    f.write(content)
                
                return {
                    "success": True,
                    "message": f"File written successfully",
                    "file_path": str(path.absolute()),
                    "file_size": len(content)
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.server.tool()
        async def list_directory(directory_path: str = ".") -> Dict[str, Any]:
            """List contents of a directory"""
            try:
                path = Path(directory_path)
                if not path.exists():
                    return {"success": False, "error": "Directory not found"}
                
                if not path.is_dir():
                    return {"success": False, "error": "Path is not a directory"}
                
                items = []
                files = []
                directories = []
                
                for item in path.iterdir():
                    item_info = {
                        "name": item.name,
                        "path": str(item.absolute()),
                        "size": item.stat().st_size if item.is_file() else 0,
                        "modified": item.stat().st_mtime
                    }
                    
                    if item.is_file():
                        files.append(item_info)
                    elif item.is_dir():
                        directories.append(item_info)
                
                return {
                    "success": True,
                    "directory": str(path.absolute()),
                    "files": files,
                    "directories": directories,
                    "total_items": len(files) + len(directories)
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.server.tool()
        async def search_web(query: str, max_results: int = 5) -> Dict[str, Any]:
            """Perform a web search (mock implementation)"""
            # This is a mock implementation
            # In real implementation, integrate with actual search APIs like:
            # - Google Custom Search API
            # - DuckDuckGo API
            # - Brave Search API
            
            mock_results = [
                {
                    "title": f"Result {i+1} for '{query}'",
                    "url": f"https://example.com/search?q={query.replace(' ', '+')}&result={i+1}",
                    "snippet": f"This is a mock search result {i+1} for the query '{query}'...",
                    "source": "mock-search-engine"
                }
                for i in range(min(max_results, 10))
            ]
            
            return {
                "success": True,
                "query": query,
                "results": mock_results,
                "total_results": len(mock_results),
                "search_engine": "mock"
            }
        
        @self.server.tool()
        async def get_system_info() -> Dict[str, Any]:
            """Get system information"""
            try:
                import platform
                import psutil
                
                return {
                    "success": True,
                    "system": {
                        "platform": platform.system(),
                        "platform_version": platform.version(),
                        "python_version": platform.python_version(),
                        "cpu_count": psutil.cpu_count(),
                        "memory_total": psutil.virtual_memory().total,
                        "memory_available": psutil.virtual_memory().available,
                        "disk_usage": psutil.disk_usage('/')._asdict()
                    }
                }
            except ImportError:
                return {
                    "success": True,
                    "system": {
                        "platform": "Unknown",
                        "python_version": "Unknown",
                        "note": "psutil not available"
                    }
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
    
    async def start(self):
        """Start the MCP server"""
        await self.server.run()
    
    async def start_async(self):
        """Start the MCP server asynchronously"""
        await self.start()


async def main():
    """Main entry point for the MCP server"""
    server = MCPServer()
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())