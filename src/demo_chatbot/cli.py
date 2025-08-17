"""
Command-line interface for the demo chatbot.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from demo_chatbot.agents.langgraph_agent import LangGraphAgent
from demo_chatbot.config.settings import settings
from demo_chatbot.utils.logger import setup_logger

console = Console()
logger = setup_logger(__name__)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Demo Chatbot - LangChain + LangGraph + MCP + Agent Integration"""
    pass


@cli.command()
def check():
    """Check environment setup."""
    console.print("[bold blue]🔍 Checking environment setup...[/bold blue]")
    
    # Check API key
    if settings.MOONSHOT_API_KEY:
        console.print("✅ MOONSHOT_API_KEY is set")
    else:
        console.print("❌ MOONSHOT_API_KEY is missing")
        return False
    
    # Check Python version
    if sys.version_info >= (3, 8):
        console.print(f"✅ Python {sys.version} is compatible")
    else:
        console.print(f"❌ Python {sys.version} is too old (requires 3.8+)")
    
    # Check working directory
    if settings.WORKING_DIRECTORY.exists():
        console.print(f"✅ Working directory: {settings.WORKING_DIRECTORY}")
    else:
        console.print(f"❌ Working directory not found: {settings.WORKING_DIRECTORY}")
    
    console.print("[bold green]Environment check completed![/bold green]")
    return True


@cli.command()
def install():
    """Install required dependencies."""
    console.print("[bold blue]📦 Installing dependencies...[/bold blue]")
    
    import subprocess
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        console.print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        console.print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


@cli.command()
def demo():
    """Run a comprehensive demo."""
    console.print("[bold blue]🤖 Starting LangGraph Agent Demo...[/bold blue]")
    
    if not settings.MOONSHOT_API_KEY:
        console.print("❌ Please set MOONSHOT_API_KEY in your .env file")
        return
    
    asyncio.run(_run_demo())


async def _run_demo():
    """Run the demo asynchronously."""
    print(Panel("Welcome to the LangGraph Agent Demo!", title="Demo Chatbot", style="bold blue"))
    agent = LangGraphAgent()
    
    demo_queries = [
        "Hello! What can you do?",
        "List the files in the current directory",
        "Create a new file called 'demo.txt' with the content 'Hello from the agent!'",
        "Calculate 25 * 4 + 10",
        "Read the content of the demo.txt file you just created"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        console.print(f"\n[bold cyan]{i}. User:[/bold cyan] {query}")
        
        try:
            response = await agent.run(query)
            console.print(f"[green]   Agent:[/green] {response}")
        except Exception as e:
            console.print(f"[red]   Error:[/red] {e}")


@cli.command()
def interactive():
    """Start interactive chat mode."""
    console.print("[bold blue]🎯 Interactive Mode Started[/bold blue]")
    console.print("Type 'quit' to exit, 'help' for available commands\n")
    
    if not settings.MOONSHOT_API_KEY:
        console.print("❌ Please set MOONSHOT_API_KEY in your .env file")
        return
    
    asyncio.run(_run_interactive())


async def _run_interactive():
    """Run interactive mode asynchronously."""
    agent = LangGraphAgent()
    
    while True:
        try:
            user_input = Prompt.ask("[bold blue]You[/bold blue]")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("[bold green]Goodbye![/bold green]")
                break
            
            if user_input.lower() == 'help':
                _show_help()
                continue
            
            if user_input.strip():
                with console.status("[bold green]Thinking..."):
                    response = await agent.run(user_input)
                console.print(f"[bold green]Agent:[/bold green] {response}")
                
        except KeyboardInterrupt:
            console.print("\n[bold green]Goodbye![/bold green]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")


def _show_help():
    """Show help information."""
    table = Table(title="Available Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")
    
    table.add_row("quit/exit/q", "Exit the program")
    table.add_row("help", "Show this help message")
    table.add_row("Any text", "Chat with the agent")
    
    console.print(table)


@cli.command()
def examples():
    """Run comprehensive examples."""
    console.print("[bold blue]📚 Running comprehensive examples...[/bold blue]")
    
    if not settings.MOONSHOT_API_KEY:
        console.print("❌ Please set MOONSHOT_API_KEY in your .env file")
        return
    
    asyncio.run(_run_examples())


async def _run_examples():
    """Run all examples asynchronously."""
    from demo_chatbot.examples import run_all_examples
    await run_all_examples()


@cli.command()
@click.option('--host', default='localhost', help='MCP server host')
@click.option('--port', default=8080, help='MCP server port')
def mcp_server(host: str, port: int):
    """Start the MCP server."""
    console.print(f"[bold blue]🔧 Starting MCP server on {host}:{port}...[/bold blue]")
    console.print("Note: MCP server implementation is a template")
    console.print("Use: python -m demo_chatbot.servers.mcp_server")


@cli.command()
@click.option('--thread-id', default='cli', help='Thread ID for conversation memory')
def chat(thread_id: str):
    """Start a chat session with conversation memory."""
    console.print(f"[bold blue]💬 Chat Session Started (Thread ID: {thread_id})[/bold blue]")
    
    if not settings.MOONSHOT_API_KEY:
        console.print("❌ Please set MOONSHOT_API_KEY in your .env file")
        return
    
    asyncio.run(_run_chat(thread_id))


async def _run_chat(thread_id: str):
    """Run chat session with thread memory."""
    agent = LangGraphAgent()
    
    console.print("[dim]Conversation memory is enabled for this session[/dim]\n")
    
    while True:
        try:
            user_input = Prompt.ask("[bold blue]You[/bold blue]")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("[bold green]Goodbye![/bold green]")
                break
            
            if user_input.strip():
                with console.status("[bold green]Thinking..."):
                    response = await agent.run(user_input, thread_id=thread_id)
                console.print(f"[bold green]Agent:[/bold green] {response}")
                
        except KeyboardInterrupt:
            console.print("\n[bold green]Goodbye![/bold green]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")


if __name__ == "__main__":
    cli()