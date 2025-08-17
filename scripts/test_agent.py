#!/usr/bin/env python3
"""
Test script for the Demo Agent
Tests the agent's functionality without interactive mode
"""

import asyncio
import tempfile
import os
from pathlib import Path
from demo_agent import DemoAgent


async def test_agent():
    """Test the demo agent functionality"""
    print("Testing Demo Agent Functionality")
    print("=" * 40)
    
    agent = DemoAgent()
    
    # Test 1: System info
    print("1. Testing system_info...")
    result = await agent.get_system_info()
    if result["success"]:
        print("   [OK] System info retrieved")
        print(f"   Platform: {result['system']['platform']}")
        print(f"   Python: {result['system']['python_version']}")
    else:
        print(f"   [ERROR] {result['error']}")
    
    # Test 2: Directory listing
    print("\n2. Testing directory listing...")
    result = await agent.list_directory(".")
    if result["success"]:
        print(f"   [OK] Found {result['total_items']} items in current directory")
        print(f"   Files: {len(result['files'])}")
        print(f"   Directories: {len(result['directories'])}")
    else:
        print(f"   [ERROR] {result['error']}")
    
    # Test 3: File operations
    print("\n3. Testing file operations...")
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "agent_test.txt")
        test_content = "Hello from Demo Agent!"
        
        # Write file
        result = await agent.write_file(test_file, test_content)
        if result["success"]:
            print("   [OK] File written successfully")
            print(f"   Wrote {result['file_size']} bytes")
        else:
            print(f"   [ERROR] {result['error']}")
        
        # Read file
        result = await agent.read_file(test_file)
        if result["success"]:
            print("   [OK] File read successfully")
            print(f"   Content: {result['content']}")
        else:
            print(f"   [ERROR] {result['error']}")
    
    # Test 4: Command processing
    print("\n4. Testing command processing...")
    
    # Test help command
    result = await agent.process_command("help")
    if result["success"]:
        print("   [OK] Help command works")
    else:
        print(f"   [ERROR] {result['error']}")
    
    # Test unknown command
    result = await agent.process_command("unknown_command")
    if not result["success"]:
        print("   [OK] Unknown command properly handled")
    
    print("\nDemo Agent test completed!")


if __name__ == "__main__":
    asyncio.run(test_agent())