#!/usr/bin/env python3
"""
LangGraph Demo Runner
Unified script to run LangGraph demonstrations and examples
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set"""
    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        print("❌ MOONSHOT_API_KEY is not set")
        print("Please set it in your .env file:")
        print("MOONSHOT_API_KEY=your_actual_api_key_here")
        return False
    
    print("✅ MOONSHOT_API_KEY is set")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("✅ Dependencies installed successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

async def run_basic_demo():
    """Run basic LangGraph demo"""
    print("\n🎯 Basic LangGraph Demo")
    print("=" * 50)
    
    try:
        from chatbot.api.langgraph.langgraph_client import LangGraphChatClient
        
        client = LangGraphChatClient()
        
        demo_queries = [
            "Hello! What is LangGraph?",
            "How does LangGraph differ from regular chat APIs?",
            "Can you explain the benefits of using LangGraph?"
        ]
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n{i}. ❓ {query}")
            response = await client.chat(query)
            print(f"   💡 {response}")
            
    except Exception as e:
        print(f"❌ Error in basic demo: {e}")
        return False
    
    return True

async def run_tool_demo():
    """Run tool-based demo"""
    print("\n🛠️ Tool-Based Demo")
    print("=" * 50)
    
    try:
        from chatbot.api.langgraph.langgraph_workflows import ToolWorkflow
        
        workflow = ToolWorkflow()
        
        commands = [
            "List files in the current directory",
            "Create a demo file called 'langgraph_test.txt' with content 'Hello from LangGraph!'",
            "Read the content of langgraph_test.txt",
            "Calculate 25 * 4 + 10",
            "Get system information"
        ]
        
        for i, command in enumerate(commands, 1):
            print(f"\n{i}. 📝 {command}")
            response = await workflow.run(command)
            print(f"   ✅ {response}")
            
    except Exception as e:
        print(f"❌ Error in tool demo: {e}")
        return False
    
    return True

async def run_interactive_mode():
    """Run interactive mode"""
    print("\n💬 Interactive LangGraph Mode")
    print("Type 'quit' to exit, 'help' for available commands")
    print("=" * 50)
    
    try:
        from chatbot.api.langgraph.langgraph_client import LangGraphChatClient
        
        client = LangGraphChatClient()
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    show_help()
                    continue
                
                if user_input:
                    print("🤖 Bot: ", end="")
                    response = await client.chat(user_input)
                    print(response)
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Error in interactive mode: {e}")
        return False
    
    return True

async def run_examples():
    """Run comprehensive examples"""
    print("\n📚 Running LangGraph Examples")
    print("=" * 50)
    
    try:
        from chatbot.examples.langgraph_examples import LangGraphExamples
        
        examples = LangGraphExamples()
        await examples.run_all_examples()
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        return False
    
    return True

def show_help():
    """Show help information"""
    print("\n🆘 Available Commands:")
    print("  - quit/exit/q: Exit the program")
    print("  - help: Show this help message")
    print("  - Any other text: Chat with the LangGraph agent")
    print("\n🔧 Available Tools:")
    print("  - File operations (read, write, list)")
    print("  - Mathematical calculations")
    print("  - System information")
    print("  - Multi-client comparison")

def show_menu():
    """Show interactive menu"""
    print("\n🚀 LangGraph Demo Menu")
    print("=" * 30)
    print("1. Basic Demo")
    print("2. Tool Demo")
    print("3. Interactive Mode")
    print("4. Run Examples")
    print("5. Check Environment")
    print("6. Install Dependencies")
    print("7. Exit")
    print("=" * 30)

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="LangGraph Demo Runner")
    parser.add_argument("--basic", action="store_true", help="Run basic demo")
    parser.add_argument("--tools", action="store_true", help="Run tool demo")
    parser.add_argument("--interactive", action="store_true", help="Run interactive mode")
    parser.add_argument("--examples", action="store_true", help="Run examples")
    parser.add_argument("--check", action="store_true", help="Check environment")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--menu", action="store_true", help="Show interactive menu")
    
    args = parser.parse_args()
    
    # If no arguments provided, show menu
    if len(sys.argv) == 1:
        args.menu = True
    
    if args.check:
        check_environment()
        return
    
    if args.install:
        install_dependencies()
        return
    
    if not check_environment():
        return
    
    if args.menu:
        while True:
            show_menu()
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == "1":
                await run_basic_demo()
            elif choice == "2":
                await run_tool_demo()
            elif choice == "3":
                await run_interactive_mode()
            elif choice == "4":
                await run_examples()
            elif choice == "5":
                check_environment()
            elif choice == "6":
                install_dependencies()
            elif choice == "7":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
    
    elif args.basic:
        await run_basic_demo()
    elif args.tools:
        await run_tool_demo()
    elif args.interactive:
        await run_interactive_mode()
    elif args.examples:
        await run_examples()
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())