#!/usr/bin/env python3
"""
Root Launcher for Demo Chatbot
Simple launcher to run all available scripts
"""

import os
import sys
from pathlib import Path

def main():
    """Simple launcher for all demo scripts"""
    scripts_dir = Path(__file__).parent / "scripts"
    
    print("=== Demo Chatbot Launcher ===")
    print("1. Run Demo Agent (Interactive)")
    print("2. Run MCP Server")
    print("3. Test Demo Agent")
    print("4. Test MCP Server")
    print("5. Run Master Menu")
    print("6. Exit")
    
    try:
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            os.system(f'python "{scripts_dir / "demo_agent.py"}"')
        elif choice == "2":
            os.system(f'python "{scripts_dir / "mcp_server.py"}"')
        elif choice == "3":
            os.system(f'python "{scripts_dir / "test_agent.py"}"')
        elif choice == "4":
            os.system(f'python "{scripts_dir / "test_mcp.py"}"')
        elif choice == "5":
            os.system(f'python "{scripts_dir / "run_demo.py"}"')
        elif choice == "6":
            print("Goodbye!")
        else:
            print("Invalid choice. Please select 1-6.")
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()