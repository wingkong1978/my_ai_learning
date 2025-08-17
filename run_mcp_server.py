#!/usr/bin/env python3
"""
Simple MCP Server Runner
A working demo of the MCP (Model Context Protocol) server
"""

import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from demo_chatbot.servers.mcp_server import MCPServer


async def main():
    """Main function to start the MCP server"""
    print("🚀 Starting MCP Demo Server...")
    print("📡 Server: demo-chatbot-mcp")
    print("🔧 Available tools:")
    print("   - read_file: Read file contents")
    print("   - write_file: Write content to files")
    print("   - list_directory: List directory contents")
    print("   - search_web: Web search (mock)")
    print("   - get_system_info: System information")
    print("\n⚡ Server starting... Press Ctrl+C to stop\n")
    
    try:
        server = MCPServer()
        await server.start()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")


if __name__ == "__main__":
    asyncio.run(main())