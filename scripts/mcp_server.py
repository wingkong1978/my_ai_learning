#!/usr/bin/env python3
"""
Simple MCP Server Implementation
A working demo of the Model Context Protocol server
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.types as types


# Create server instance
server = Server("demo-chatbot-mcp")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="read_file",
            description="Read contents of a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the file to read"},
                    "encoding": {"type": "string", "default": "utf-8", "description": "File encoding"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the file to write"},
                    "content": {"type": "string", "description": "Content to write"},
                    "encoding": {"type": "string", "default": "utf-8", "description": "File encoding"}
                },
                "required": ["file_path", "content"]
            }
        ),
        Tool(
            name="list_directory",
            description="List contents of a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory_path": {"type": "string", "default": ".", "description": "Directory path to list"}
                }
            }
        ),
        Tool(
            name="get_system_info",
            description="Get basic system information",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls"""
    
    if name == "read_file":
        file_path = arguments.get("file_path")
        encoding = arguments.get("encoding", "utf-8")
        
        try:
            path = Path(file_path)
            if not path.exists():
                return [TextContent(type="text", text=f"Error: File not found: {file_path}")]
            
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()
            
            return [TextContent(type="text", text=f"File: {file_path}\nContent:\n{content}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error reading file: {e}")]
    
    elif name == "write_file":
        file_path = arguments.get("file_path")
        content = arguments.get("content")
        encoding = arguments.get("encoding", "utf-8")
        
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)
            
            return [TextContent(type="text", text=f"Successfully wrote to {file_path} ({len(content)} bytes)")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error writing file: {e}")]
    
    elif name == "list_directory":
        directory_path = arguments.get("directory_path", ".")
        
        try:
            path = Path(directory_path)
            if not path.exists():
                return [TextContent(type="text", text=f"Error: Directory not found: {directory_path}")]
            
            items = []
            for item in path.iterdir():
                item_type = "DIR" if item.is_dir() else "FILE"
                items.append(f"{item_type} {item.name}")
            
            return [TextContent(type="text", text=f"Directory: {path.absolute()}\n\n" + "\n".join(items))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error listing directory: {e}")]
    
    elif name == "get_system_info":
        try:
            import platform
            info = {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "python_version": platform.python_version(),
                "cwd": os.getcwd()
            }
            
            return [TextContent(type="text", text=f"System Information:\n{json.dumps(info, indent=2)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting system info: {e}")]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Main function to start the MCP server"""
    print("Starting MCP Demo Server...")
    print("Server: demo-chatbot-mcp")
    print("Available tools: read_file, write_file, list_directory, get_system_info")
    print("Server starting... Use Ctrl+C to stop")
    
    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")


if __name__ == "__main__":
    asyncio.run(main())