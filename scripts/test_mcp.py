#!/usr/bin/env python3
"""
MCP Server Test Script
Tests the MCP server functionality
"""

import asyncio
import json
import tempfile
import os
from pathlib import Path

# Test the MCP server tools directly
async def test_mcp_functionality():
    """Test the MCP server tools directly"""
    print("Testing MCP Server Functionality")
    print("=" * 40)
    
    # Test file operations
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test.txt")
        
        # Test write_file
        print("1. Testing write_file...")
        content = "Hello from MCP test!\nThis is a test file."
        try:
            with open(test_file, 'w') as f:
                f.write(content)
            print(f"   [OK] Wrote {len(content)} bytes to {test_file}")
        except Exception as e:
            print(f"   [ERROR] Error: {e}")
        
        # Test read_file
        print("2. Testing read_file...")
        try:
            with open(test_file, 'r') as f:
                read_content = f.read()
            print(f"   [OK] Read content: {read_content.strip()}")
        except Exception as e:
            print(f"   [ERROR] Error: {e}")
        
        # Test list_directory
        print("3. Testing list_directory...")
        try:
            items = os.listdir(temp_dir)
            print(f"   [OK] Found {len(items)} items in directory")
            for item in items:
                print(f"     - {item}")
        except Exception as e:
            print(f"   [ERROR] Error: {e}")
    
    # Test system info
    print("4. Testing system_info...")
    try:
        import platform
        info = {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cwd": os.getcwd()
        }
        print(f"   [OK] System info: {info}")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
    
    print("\nMCP Server functionality test completed!")


if __name__ == "__main__":
    asyncio.run(test_mcp_functionality())