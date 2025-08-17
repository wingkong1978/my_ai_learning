#!/usr/bin/env python3
"""
Demo Agent with MCP Integration
A simple AI agent that can use MCP tools to interact with the file system
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class DemoAgent:
    """Simple demo agent with MCP tool integration"""
    
    def __init__(self):
        self.name = "DemoAgent"
        self.tools = {
            'read_file': self.read_file,
            'write_file': self.write_file,
            'list_directory': self.list_directory,
            'get_system_info': self.get_system_info
        }
    
    async def read_file(self, file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
        """Read file contents"""
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
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def write_file(self, file_path: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
        """Write content to file"""
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
    
    async def list_directory(self, directory_path: str = ".") -> Dict[str, Any]:
        """List directory contents"""
        try:
            path = Path(directory_path)
            if not path.exists():
                return {"success": False, "error": "Directory not found"}
            
            items = []
            files = []
            directories = []
            
            for item in path.iterdir():
                item_info = {
                    "name": item.name,
                    "path": str(item.absolute()),
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else 0
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
    
    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        try:
            import platform
            return {
                "success": True,
                "system": {
                    "platform": platform.system(),
                    "platform_version": platform.version(),
                    "python_version": platform.python_version(),
                    "cwd": os.getcwd(),
                    "agent_name": self.name
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def process_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """Process user commands using available tools"""
        command = command.lower().strip()
        
        if command == "help":
            return {
                "success": True,
                "response": """
Available commands:
- help: Show this help message
- read <file_path>: Read a file
- write <file_path> <content>: Write to a file
- ls [directory]: List directory contents
- info: Get system information
- exit: Exit the agent
                """.strip()
            }
        
        elif command.startswith("read "):
            file_path = command[5:].strip()
            return await self.read_file(file_path)
        
        elif command.startswith("write "):
            parts = command[6:].split(" ", 1)
            if len(parts) != 2:
                return {"success": False, "error": "Usage: write <file_path> <content>"}
            file_path, content = parts
            return await self.write_file(file_path, content)
        
        elif command.startswith("ls"):
            directory = command[2:].strip() or "."
            return await self.list_directory(directory)
        
        elif command == "info":
            return await self.get_system_info()
        
        else:
            return {"success": False, "error": f"Unknown command: {command}"}
    
    async def interactive_session(self):
        """Start an interactive session with the agent"""
        print(f"=== {self.name} Demo Agent ===")
        print("Type 'help' for available commands or 'exit' to quit")
        print("-" * 30)
        
        while True:
            try:
                user_input = input("\nAgent> ").strip()
                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("Goodbye!")
                    break
                
                result = await self.process_command(user_input)
                
                if result.get("success"):
                    if "response" in result:
                        print(result["response"])
                    else:
                        print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print(f"Error: {result.get('error', 'Unknown error')}")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


async def main():
    """Main function to run the demo agent"""
    agent = DemoAgent()
    await agent.interactive_session()


if __name__ == "__main__":
    asyncio.run(main())