#!/usr/bin/env python3
"""
Master Demo Launcher
Unified script to run all demos and tests
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def print_menu():
    """Print available demo options"""
    print("\n=== Demo Chatbot - Available Scripts ===")
    print("1. Run MCP Server")
    print("2. Run Demo Agent (Interactive)")
    print("3. Test MCP Server")
    print("4. Test Demo Agent")
    print("5. Run Original Test Scripts")
    print("6. Exit")
    print("=" * 40)

def run_script(script_name, description):
    """Run a specific script"""
    print(f"\n{description}...")
    try:
        if script_name.endswith('.py'):
            os.system(f'python "{script_name}"')
        else:
            os.system(f'"{script_name}"')
    except Exception as e:
        print(f"Error running {script_name}: {e}")

def main():
    """Main menu system"""
    scripts_dir = Path(__file__).parent
    
    while True:
        print_menu()
        choice = input("Select option (1-6): ").strip()
        
        if choice == "1":
            run_script(scripts_dir / "mcp_server.py", "Starting MCP Server")
        elif choice == "2":
            run_script(scripts_dir / "demo_agent.py", "Starting Demo Agent")
        elif choice == "3":
            run_script(scripts_dir / "test_mcp.py", "Testing MCP Server")
        elif choice == "4":
            run_script(scripts_dir / "test_agent.py", "Testing Demo Agent")
        elif choice == "5":
            run_original_tests(scripts_dir)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-6.")

def run_original_tests(scripts_dir):
    """Run the original test scripts"""
    print("\n=== Running Original Test Scripts ===")
    print("1. Test1.py - LangChain Moonshot")
    print("2. Test2.py - Direct OpenAI API")
    print("3. Test3.py - Additional tests")
    print("4. Back to main menu")
    
    choice = input("Select test (1-4): ").strip()
    
    if choice == "1":
        run_script(Path(__file__).parent.parent / "test1.py", "Running test1.py")
    elif choice == "2":
        run_script(Path(__file__).parent.parent / "test2.py", "Running test2.py")
    elif choice == "3":
        run_script(Path(__file__).parent.parent / "test3.py", "Running test3.py")
    elif choice == "4":
        return
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()