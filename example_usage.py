"""
Example usage script demonstrating LangChain + LangGraph + MCP integration
"""

import asyncio
import os
from pathlib import Path
from langgraph_agent import LangGraphAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def example_1_basic_chat():
    """Basic chat functionality"""
    print("=== Example 1: Basic Chat ===")
    agent = LangGraphAgent()
    
    response = await agent.run("Hello! Can you introduce yourself?")
    print(f"Agent: {response}")
    print()

async def example_2_file_operations():
    """File operations using agent tools"""
    print("=== Example 2: File Operations ===")
    agent = LangGraphAgent()
    
    # Create a file
    await agent.run("Create a file called 'todo.txt' with a simple todo list")
    
    # Read the file
    content = await agent.run("Read the content of todo.txt")
    print(f"File content: {content}")
    
    # List directory
    files = await agent.run("List all files in the current directory")
    print(f"Files: {files}")
    print()

async def example_3_calculator():
    """Mathematical calculations"""
    print("=== Example 3: Calculator ===")
    agent = LangGraphAgent()
    
    queries = [
        "Calculate 25 * 4 + 10",
        "Calculate (100 - 50) * 2",
        "Calculate 3.14 * 10^2"
    ]
    
    for query in queries:
        response = await agent.run(query)
        print(f"{query} = {response}")
    print()

async def example_4_conversation_memory():
    """Demonstrate conversation memory"""
    print("=== Example 4: Conversation Memory ===")
    agent = LangGraphAgent()
    
    # First message
    response1 = await agent.run("My name is Alice", thread_id="memory_demo")
    print(f"Agent 1: {response1}")
    
    # Second message (should remember the name)
    response2 = await agent.run("What's my name?", thread_id="memory_demo")
    print(f"Agent 2: {response2}")
    print()

async def example_5_complex_workflow():
    """Complex workflow combining multiple tools"""
    print("=== Example 5: Complex Workflow ===")
    agent = LangGraphAgent()
    
    workflow = """
    Create a Python script that:
    1. Calculates the area of a circle with radius 5
    2. Writes the result to a file called 'circle_area.txt'
    3. Lists all Python files in the current directory
    """
    
    response = await agent.run(workflow)
    print(f"Workflow result: {response}")
    print()

async def run_all_examples():
    """Run all examples"""
    print("🚀 LangChain + LangGraph + MCP Agent Examples\n")
    
    # Check if API key is set
    if not os.getenv("MOONSHOT_API_KEY"):
        print("❌ Please set your MOONSHOT_API_KEY in .env file")
        print("Copy .env.example to .env and add your API key")
        return
    
    try:
        await example_1_basic_chat()
        await example_2_file_operations()
        await example_3_calculator()
        await example_4_conversation_memory()
        await example_5_complex_workflow()
        
        print("✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")

if __name__ == "__main__":
    asyncio.run(run_all_examples())