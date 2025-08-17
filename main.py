"""
Main integration script for LangChain + LangGraph + MCP + Agent setup
This script provides a unified interface to run the complete system
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Import our modules
from langgraph_agent import LangGraphAgent
from mcp_server import MCPServer

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = ["MOONSHOT_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file or environment")
        return False
    
    print("✅ Environment variables are set correctly")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    os.system("pip install -r requirements.txt")
    print("✅ Dependencies installed")

async def run_agent_demo():
    """Run a demo of the LangGraph agent"""
    print("\n🤖 Starting LangGraph Agent Demo...")
    
    agent = LangGraphAgent()
    
    demo_queries = [
        "Hello! What can you do?",
        "List the files in the current directory",
        "Create a new file called 'demo.txt' with the content 'Hello from the agent!'",
        "Calculate 25 * 4 + 10",
        "Read the content of the demo.txt file you just created"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{i}. User: {query}")
        try:
            response = await agent.run(query)
            print(f"   Agent: {response}")
        except Exception as e:
            print(f"   Error: {e}")

def run_mcp_server():
    """Run the MCP server"""
    print("🔧 Starting MCP Server...")
    print("Note: MCP server implementation is a template. Run with: python mcp_server.py")

async def interactive_mode():
    """Run in interactive mode"""
    print("\n🎯 Interactive Mode Started")
    print("Type 'quit' to exit, 'help' for available commands")
    
    agent = LangGraphAgent()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("- quit/exit/q: Exit the program")
                print("- help: Show this help message")
                print("- Any other text: Chat with the agent")
                continue
            
            if user_input:
                response = await agent.run(user_input)
                print(f"Agent: {response}")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="LangChain + LangGraph + MCP + Agent Demo")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--demo", action="store_true", help="Run agent demo")
    parser.add_argument("--mcp", action="store_true", help="Show MCP server info")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--check", action="store_true", help="Check environment setup")
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        # No arguments provided, show help
        parser.print_help()
        print("\nQuick start:")
        print("1. python main.py --check    # Check environment")
        print("2. python main.py --install  # Install dependencies")
        print("3. python main.py --demo     # Run demo")
        print("4. python main.py --interactive  # Interactive chat")
        return
    
    if args.install:
        install_dependencies()
        return
    
    if args.check:
        check_environment()
        return
    
    if not check_environment():
        return
    
    if args.mcp:
        run_mcp_server()
        return
    
    if args.demo:
        asyncio.run(run_agent_demo())
        return
    
    if args.interactive:
        asyncio.run(interactive_mode())
        return

if __name__ == "__main__":
    main()