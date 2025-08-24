"""
Example usage script demonstrating LangChain + LangGraph + MCP integration
"""

import asyncio
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from demo_chatbot.agents.langgraph_agent import LangGraphAgent
from demo_chatbot.config.settings import settings

console = Console()


async def example_1_basic_chat():
    """Basic chat functionality"""
    console.print(Panel("Example 1: Basic Chat", style="bold blue"))
    
    agent = LangGraphAgent()
    
    response = await agent.run("Hello! Can you introduce yourself and tell me what tools you have access to?")
    console.print(f"Agent: {response}")
    console.print()


async def example_2_file_operations():
    """File operations using agent tools"""
    console.print(Panel("Example 2: File Operations", style="bold blue"))
    
    agent = LangGraphAgent()
    
    # Create a todo list file
    console.print("[yellow]Creating todo.txt...[/yellow]")
    await agent.run("Create a file called 'todo.txt' with a simple todo list for a Python project")
    
    # Read the file
    console.print("[yellow]Reading todo.txt...[/yellow]")
    content = await agent.run("Read the content of todo.txt")
    console.print(f"File content:\n{content}")
    
    # List directory
    console.print("[yellow]Listing directory contents...[/yellow]")
    files = await agent.run("List all Python files in the current directory")
    console.print(f"Python files: {files}")
    console.print()


async def example_3_calculator():
    """Mathematical calculations"""
    console.print(Panel("Example 3: Calculator", style="bold blue"))
    
    agent = LangGraphAgent()
    
    queries = [
        "Calculate the area of a circle with radius 5",
        "Calculate (100 - 50) * 2 + 10",
        "Calculate 3.14159 * 10^2",
    ]
    
    for query in queries:
        response = await agent.run(query)
        console.print(f"{query} = {response}")
    console.print()


async def example_4_conversation_memory():
    """Demonstrate conversation memory"""
    console.print(Panel("Example 4: Conversation Memory", style="bold blue"))
    
    agent = LangGraphAgent()
    
    # First message
    console.print("[yellow]Setting user name...[/yellow]")
    response1 = await agent.run("My name is Alice and I'm a Python developer", thread_id="memory_demo")
    console.print(f"Agent 1: {response1}")
    
    # Second message (should remember the name)
    console.print("[yellow]Asking about user...[/yellow]")
    response2 = await agent.run("What's my name and what do I do for a living?", thread_id="memory_demo")
    console.print(f"Agent 2: {response2}")
    
    # Third message (continue conversation)
    console.print("[yellow]Following up...[/yellow]")
    response3 = await agent.run("Can you create a simple Python script based on what you know about me?", thread_id="memory_demo")
    console.print(f"Agent 3: {response3}")
    console.print()


async def example_5_complex_workflow():
    """Complex workflow combining multiple tools"""
    console.print(Panel("Example 5: Complex Workflow", style="bold blue"))
    
    agent = LangGraphAgent()
    
    workflow = """
    I need a Python project structure analyzer. Please:
    1. Create a Python script that walks through the current directory
    2. Counts the number of Python files
    3. Calculates the total lines of code
    4. Writes the results to 'project_stats.json'
    5. Also create a summary report in 'project_summary.md'
    """
    
    console.print("[yellow]Running complex workflow...[/yellow]")
    response = await agent.run(workflow)
    console.print(f"Workflow result: {response}")
    console.print()


async def example_6_error_handling():
    """Demonstrate error handling"""
    console.print(Panel("Example 6: Error Handling", style="bold blue"))
    
    agent = LangGraphAgent()
    
    # Test with invalid file
    response = await agent.run("Read the content of 'nonexistent_file.txt'")
    console.print(f"Error handling: {response}")
    
    # Test with invalid calculation
    response = await agent.run("Calculate invalid_expression@#$%")
    console.print(f"Calculation error: {response}")
    console.print()


async def example_7_multi_step_process():
    """Multi-step process with tool chaining"""
    console.print(Panel("Example 7: Multi-step Process", style="bold blue"))
    
    agent = LangGraphAgent()
    
    # Step 1: Create a data file
    console.print("[yellow]Step 1: Creating data file...[/yellow]")
    await agent.run("Create 'data.txt' with numbers 1 to 10 on separate lines")
    
    # Step 2: Read and process the data
    console.print("[yellow]Step 2: Processing data...[/yellow]")
    response = await agent.run("Read data.txt and calculate the sum of all numbers")
    console.print(f"Sum calculation: {response}")
    
    # Step 3: Create analysis report
    console.print("[yellow]Step 3: Creating analysis report...[/yellow]")
    await agent.run("Create 'analysis_report.md' with the sum result and some insights about the data")
    
    # Step 4: Verify report
    console.print("[yellow]Step 4: Verifying report...[/yellow]")
    report = await agent.run("Read analysis_report.md")
    console.print(f"Report content:\n{report}")
    console.print()


async def run_all_examples():
    """Run all examples"""
    console.print("[bold green]🚀 LangChain + LangGraph + MCP Agent Examples[/bold green]\n")
    
    # Check if API key is set
    if not settings.moonshot_api_key:
        console.print("[red]❌ Please set your MOONSHOT_API_KEY in .env file[/red]")
        console.print("Copy .env.example to .env and add your API key")
        return
    
    try:
        await example_1_basic_chat()
        await example_2_file_operations()
        await example_3_calculator()
        await example_4_conversation_memory()
        await example_5_complex_workflow()
        await example_6_error_handling()
        await example_7_multi_step_process()
        
        console.print("[bold green]✅ All examples completed successfully![/bold green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error running examples: {e}[/red]")
        import traceback
        console.print(f"[red]{traceback.format_exc()}[/red]")


async def run_specific_example(example_name: str):
    """Run a specific example by name"""
    examples = {
        "basic": example_1_basic_chat,
        "files": example_2_file_operations,
        "calculator": example_3_calculator,
        "memory": example_4_conversation_memory,
        "workflow": example_5_complex_workflow,
        "error": example_6_error_handling,
        "multistep": example_7_multi_step_process,
    }
    
    if example_name in examples:
        await examples[example_name]()
    else:
        console.print(f"[red]Unknown example: {example_name}[/red]")
        console.print(f"Available examples: {', '.join(examples.keys())}")


async def run_demo():
    """Simple demo that works with the basic chatbot structure."""
    console = Console()
    console.print("[bold green]🚀 Demo Chatbot - Basic Examples[/bold green]\n")
    
    # Simple demo using the basic chatbot clients
    try:
        from ..api.langchain.moonshot_langchain import MoonshotLangChainClient
        from ..api.openai.moonshot_openai import MoonshotOpenAIClient
        
        console.print("[yellow]Testing LangChain integration...[/yellow]")
        langchain_client = MoonshotLangChainClient()
        response1 = langchain_client.chat_completion([
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you introduce yourself?"}
        ])
        console.print(f"LangChain Response: {response1}")
        
        console.print("\n[yellow]Testing OpenAI integration...[/yellow]")
        openai_client = MoonshotOpenAIClient()
        response2 = openai_client.chat_completion([
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you introduce yourself?"}
        ])
        console.print(f"OpenAI Response: {response2}")
        
        console.print("[bold green]✅ Demo completed successfully![/bold green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error in demo: {e}[/red]")
        import traceback
        console.print(f"[red]{traceback.format_exc()}[/red]")

def run_demo_sync():
    """Synchronous version for demo purposes."""
    import asyncio
    asyncio.run(run_demo())

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_all_examples())