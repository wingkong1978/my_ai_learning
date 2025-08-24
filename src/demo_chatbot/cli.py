"""
Command-line interface for the demo chatbot.

Provides:
- Environment validation and setup
- Interactive chat modes
- Comprehensive demos and examples
- Server management
- Enhanced error handling and user feedback
"""

import asyncio
import os
import sys
import traceback
import signal
from pathlib import Path
from typing import Optional, Dict, Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.status import Status

from demo_chatbot.agents.langgraph_agent import LangGraphAgent, AgentConfig
from demo_chatbot.config.settings import get_settings, LogLevel
from demo_chatbot.utils.logger import setup_logger, log_performance

# Initialize console and logger
console = Console(stderr=True)
logger = setup_logger(__name__)

# Global state
_agent_instance: Optional[LangGraphAgent] = None
_graceful_shutdown = False


def handle_cli_error(func):
    """Decorator for handling CLI errors gracefully."""
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user[/yellow]")
            sys.exit(1)
        except Exception as e:
            logger.error(f"CLI error in {func.__name__}: {e}")
            console.print(f"[red]Error: {e}[/red]")
            if get_settings().debug:
                console.print("[dim]" + traceback.format_exc() + "[/dim]")
            sys.exit(1)
    return wrapper


def get_agent() -> LangGraphAgent:
    """Get or create agent instance with caching."""
    global _agent_instance
    
    if _agent_instance is None:
        try:
            settings = get_settings()
            config = AgentConfig(
                model_name=settings.default_model,
                temperature=settings.temperature,
                max_tokens=settings.max_tokens,
                max_file_size=settings.max_file_size,
                allowed_extensions=settings.allowed_file_extensions
            )
            _agent_instance = LangGraphAgent(config)
            logger.info("Agent instance created successfully")
        except Exception as e:
            logger.error(f"Failed to create agent: {e}")
            raise
    
    return _agent_instance


@click.group()
@click.version_option(version="0.1.0")
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.option('--config-file', type=click.Path(exists=True), help='Custom configuration file')
@click.pass_context
def cli(ctx, debug: bool, config_file: Optional[str]):
    """Demo Chatbot - LangChain + LangGraph + MCP + Agent Integration
    
    A comprehensive AI chatbot demonstrating modern agent technologies.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Store configuration in context
    ctx.obj['debug'] = debug
    ctx.obj['config_file'] = config_file
    
    # Update settings based on CLI options
    settings = get_settings()
    if debug:
        settings.debug = True
        settings.log_level = LogLevel.DEBUG
    
    logger.debug(f"CLI initialized with debug={debug}, config_file={config_file}")


@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Show detailed information')
@handle_cli_error
def check(verbose: bool):
    """Check environment setup and configuration."""
    console.print("[bold blue]🔍 Environment Health Check[/bold blue]\n")
    
    settings = get_settings()
    checks_passed = 0
    total_checks = 0
    issues = []
    
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
        task = progress.add_task("Running checks...", total=100)
        
        # Check API key
        total_checks += 1
        progress.update(task, advance=20, description="Checking API configuration...")
        try:
            settings.validate_api_key()
            console.print("✅ MOONSHOT_API_KEY is configured")
            checks_passed += 1
        except ValueError as e:
            console.print(f"❌ API Key: {e}")
            issues.append("Set MOONSHOT_API_KEY in .env file")
        
        # Check Python version
        total_checks += 1
        progress.update(task, advance=20, description="Checking Python version...")
        if sys.version_info >= (3, 8):
            console.print(f"✅ Python {sys.version.split()[0]} is compatible")
            checks_passed += 1
        else:
            console.print(f"❌ Python {sys.version.split()[0]} is too old (requires 3.8+)")
            issues.append("Upgrade Python to version 3.8 or higher")
        
        # Check working directory
        total_checks += 1
        progress.update(task, advance=20, description="Checking working directory...")
        working_dir = getattr(settings, 'working_directory', None)
        if working_dir and working_dir.exists():
            console.print(f"✅ Working directory: {working_dir}")
            checks_passed += 1
        else:
            console.print(f"❌ Working directory not found: {working_dir}")
            issues.append(f"Create working directory: {working_dir}")
        
        # Check dependencies
        total_checks += 1
        progress.update(task, advance=20, description="Checking dependencies...")
        try:
            import langchain
            import langgraph
            import openai
            console.print("✅ Required dependencies are installed")
            checks_passed += 1
        except ImportError as e:
            console.print(f"❌ Missing dependencies: {e}")
            issues.append("Install dependencies: pip install -e .")
        
        # Check configuration
        total_checks += 1
        progress.update(task, advance=20, description="Validating configuration...")
        try:
            config_issues = []
            
            if settings.max_file_size <= 0:
                config_issues.append("Invalid max_file_size")
            
            if not settings.allowed_file_extensions:
                config_issues.append("No allowed file extensions configured")
            
            if config_issues:
                console.print(f"⚠️  Configuration warnings: {', '.join(config_issues)}")
            else:
                console.print("✅ Configuration is valid")
                checks_passed += 1
                
        except Exception as e:
            console.print(f"❌ Configuration error: {e}")
            issues.append("Review configuration settings")
        
        progress.update(task, completed=100, description="Health check completed")
    
    # Show summary
    console.print(f"\n[bold]Health Check Summary[/bold]")
    console.print(f"Checks passed: {checks_passed}/{total_checks}")
    
    if checks_passed == total_checks:
        console.print("[bold green]🎉 All checks passed! Environment is ready.[/bold green]")
    else:
        console.print("[bold yellow]⚠️  Some issues found:[/bold yellow]")
        for issue in issues:
            console.print(f"  • {issue}")
    
    # Verbose output
    if verbose:
        console.print("\n[bold]Detailed Configuration[/bold]")
        config_table = Table("Setting", "Value", "Status")
        
        config_data = settings.to_dict()
        for key, value in config_data.items():
            if key.startswith('_'):
                continue
                
            status = "✅" if value is not None else "❌"
            display_value = str(value) if not key.endswith('_key') else "***" if value else "Not set"
            config_table.add_row(key, display_value, status)
        
        console.print(config_table)
    
    return checks_passed == total_checks


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
@click.option('--quick', is_flag=True, help='Run quick demo with fewer examples')
@click.option('--thread-id', default='demo', help='Thread ID for demo session')
@handle_cli_error
def demo(quick: bool, thread_id: str):
    """Run a comprehensive demo of the chatbot capabilities."""
    console.print("[bold blue]🤖 Starting LangGraph Agent Demo[/bold blue]\n")
    
    settings = get_settings()
    
    try:
        settings.validate_api_key()
    except ValueError as e:
        console.print(f"[red]❌ {e}[/red]")
        console.print("[yellow]Please configure your API key and try again.[/yellow]")
        return
    
    asyncio.run(_run_demo(quick, thread_id))


async def _run_demo(quick: bool = False, thread_id: str = "demo"):
    """Run the demo asynchronously with enhanced features."""
    # Welcome panel
    welcome_panel = Panel(
        "[bold]Welcome to the LangGraph Agent Demo![/bold]\n\n"
        "This demo showcases the agent's capabilities including:\n"
        "• File operations (read, write, list)\n"
        "• Mathematical calculations\n"
        "• Conversation memory\n"
        "• Tool integration\n"
        "• Error handling",
        title="Demo Chatbot",
        style="bold blue"
    )
    console.print(welcome_panel)
    
    try:
        with log_performance(logger, "agent_initialization"):
            agent = get_agent()
        
        # Define demo queries based on mode
        if quick:
            demo_queries = [
                "Hello! What can you do?",
                "Calculate 15 * 3 + 7",
                "List files in the current directory"
            ]
        else:
            demo_queries = [
                "Hello! What can you do? Please introduce yourself.",
                "List the files in the current directory and tell me about them",
                "Create a new file called 'demo.txt' with the content 'Hello from the LangGraph agent! This is a demo file.'",
                "Calculate the result of (25 * 4 + 10) / 2",
                "Read the content of the demo.txt file you just created",
                "Search the web for 'artificial intelligence trends 2024'",
                "What's the current system information?"
            ]
        
        console.print(f"\n[dim]Running {'quick' if quick else 'full'} demo with {len(demo_queries)} examples...[/dim]\n")
        
        for i, query in enumerate(demo_queries, 1):
            console.print(f"\n[bold cyan]{i}. User:[/bold cyan] {query}")
            
            try:
                with console.status("[bold green]Agent is thinking..."):
                    with log_performance(logger, f"demo_query_{i}", query=query):
                        response = await agent.run(query, thread_id=thread_id)
                
                # Format response for better display
                if len(response) > 500:
                    response = response[:500] + "...[truncated]"
                
                console.print(f"[green]   Agent:[/green] {response}")
                
                # Small delay between queries for better UX
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Demo query {i} failed: {e}")
                console.print(f"[red]   Error:[/red] {e}")
                
                # Ask if user wants to continue
                if not Confirm.ask("\n[yellow]Continue with remaining examples?[/yellow]"):
                    break
        
        # Demo completion
        completion_panel = Panel(
            "[bold green]Demo completed successfully![/bold green]\n\n"
            "To continue exploring:\n"
            "• Run 'demo-chatbot interactive' for interactive chat\n"
            "• Run 'demo-chatbot examples' for more examples\n"
            "• Run 'demo-chatbot --help' to see all commands",
            title="Demo Complete",
            style="bold green"
        )
        console.print(f"\n{completion_panel}")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        console.print(f"[red]Demo failed: {e}[/red]")
        
        if get_settings().debug:
            console.print("[dim]" + traceback.format_exc() + "[/dim]")


@cli.command()
@click.option('--thread-id', default='interactive', help='Thread ID for conversation memory')
@click.option('--save-history', is_flag=True, help='Save conversation history to file')
@handle_cli_error
def interactive(thread_id: str, save_history: bool):
    """Start enhanced interactive chat mode with conversation memory."""
    console.print("[bold blue]🎯 Interactive Chat Mode[/bold blue]")
    console.print(f"[dim]Thread ID: {thread_id}[/dim]")
    console.print("[dim]Type 'quit' to exit, 'help' for commands, 'clear' to clear history[/dim]\n")
    
    settings = get_settings()
    
    try:
        settings.validate_api_key()
    except ValueError as e:
        console.print(f"[red]❌ {e}[/red]")
        return
    
    asyncio.run(_run_interactive(thread_id, save_history))


async def _run_interactive(thread_id: str = "interactive", save_history: bool = False):
    """Run interactive mode with enhanced features."""
    conversation_history = []
    
    try:
        with log_performance(logger, "interactive_session_start"):
            agent = get_agent()
        
        session_info = Panel(
            f"[bold]Interactive Session Started[/bold]\n"
            f"Thread ID: {thread_id}\n"
            f"Model: {get_settings().default_model}\n"
            f"Save History: {'Yes' if save_history else 'No'}",
            title="Session Info",
            style="blue"
        )
        console.print(session_info)
        
        while not _graceful_shutdown:
            try:
                user_input = Prompt.ask("[bold blue]You[/bold blue]")
                
                if not user_input.strip():
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    console.print("[bold green]Goodbye! 👋[/bold green]")
                    break
                
                if user_input.lower() == 'help':
                    _show_interactive_help()
                    continue
                
                if user_input.lower() == 'clear':
                    if Confirm.ask("Clear conversation history?"):
                        agent.clear_conversation(thread_id)
                        conversation_history.clear()
                        console.print("[yellow]Conversation history cleared.[/yellow]")
                    continue
                
                if user_input.lower() == 'history':
                    _show_conversation_history(conversation_history)
                    continue
                
                if user_input.lower() == 'status':
                    _show_session_status(agent, thread_id)
                    continue
                
                # Process user input
                conversation_history.append({"role": "user", "content": user_input, "timestamp": asyncio.get_event_loop().time()})
                
                with console.status("[bold green]Thinking..."):
                    with log_performance(logger, "interactive_query", query=user_input[:50]):
                        response = await agent.run(user_input, thread_id=thread_id)
                
                console.print(f"[bold green]Agent:[/bold green] {response}")
                conversation_history.append({"role": "agent", "content": response, "timestamp": asyncio.get_event_loop().time()})
                
                # Save history if requested
                if save_history:
                    _save_conversation_history(conversation_history, thread_id)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'quit' to exit gracefully[/yellow]")
                continue
            except Exception as e:
                logger.error(f"Interactive session error: {e}")
                console.print(f"[red]Error: {e}[/red]")
                
                if get_settings().debug:
                    console.print("[dim]" + traceback.format_exc() + "[/dim]")
    
    finally:
        if save_history and conversation_history:
            _save_conversation_history(conversation_history, thread_id)
        
        logger.info(f"Interactive session ended for thread {thread_id}")


def _show_interactive_help():
    """Show enhanced help information for interactive mode."""
    help_table = Table(title="Interactive Commands")
    help_table.add_column("Command", style="cyan", no_wrap=True)
    help_table.add_column("Description", style="green")
    
    commands = [
        ("quit/exit/q", "Exit the interactive session"),
        ("help", "Show this help message"),
        ("clear", "Clear conversation history"),
        ("history", "Show conversation history"),
        ("status", "Show session status"),
        ("Any text", "Chat with the agent")
    ]
    
    for command, description in commands:
        help_table.add_row(command, description)
    
    console.print(help_table)


def _show_conversation_history(history: list):
    """Show conversation history in a formatted table."""
    if not history:
        console.print("[yellow]No conversation history available.[/yellow]")
        return
    
    history_table = Table(title="Conversation History")
    history_table.add_column("#", style="dim", width=3)
    history_table.add_column("Role", style="cyan", width=10)
    history_table.add_column("Message", style="white")
    history_table.add_column("Time", style="dim", width=8)
    
    for i, entry in enumerate(history[-10:], 1):  # Show last 10 entries
        role = entry["role"].title()
        message = entry["content"][:100] + "..." if len(entry["content"]) > 100 else entry["content"]
        timestamp = f"{entry['timestamp']:.1f}s"
        
        history_table.add_row(str(i), role, message, timestamp)
    
    console.print(history_table)
    
    if len(history) > 10:
        console.print(f"[dim]Showing last 10 of {len(history)} messages[/dim]")


def _show_session_status(agent: LangGraphAgent, thread_id: str):
    """Show current session status."""
    settings = get_settings()
    
    status_info = [
        ("Thread ID", thread_id),
        ("Model", settings.default_model),
        ("Temperature", str(settings.temperature)),
        ("Max Tokens", str(settings.max_tokens)),
        ("Working Directory", str(settings.working_directory)),
        ("Debug Mode", "Yes" if settings.debug else "No")
    ]
    
    status_table = Table(title="Session Status")
    status_table.add_column("Setting", style="cyan")
    status_table.add_column("Value", style="green")
    
    for setting, value in status_info:
        status_table.add_row(setting, value)
    
    console.print(status_table)


def _save_conversation_history(history: list, thread_id: str):
    """Save conversation history to file."""
    try:
        import json
        from datetime import datetime
        
        filename = f"conversation_{thread_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = Path(filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Conversation history saved to {filepath}")
        
    except Exception as e:
        logger.error(f"Failed to save conversation history: {e}")


@cli.command()
@click.option('--examples', is_flag=True, help='Run examples')
def examples(examples: bool):
    """Run comprehensive examples."""
    console.print("[bold blue]📚 Running comprehensive examples...[/bold blue]")
    
    settings = get_settings()
    
    try:
        settings.validate_api_key()
    except ValueError as e:
        console.print(f"[red]❌ {e}[/red]")
        return
    
    asyncio.run(_run_examples())


async def _run_examples():
    """Run all examples asynchronously."""
    try:
        from demo_chatbot.examples import run_all_examples
        await run_all_examples()
    except ImportError:
        console.print("[yellow]Examples module not found[/yellow]")


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
    
    settings = get_settings()
    
    try:
        settings.validate_api_key()
    except ValueError as e:
        console.print(f"[red]❌ {e}[/red]")
        return
    
    asyncio.run(_run_chat(thread_id))


async def _run_chat(thread_id: str):
    """Run chat session with thread memory."""
    try:
        agent = get_agent()
        
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
                
    except Exception as e:
        console.print(f"[red]Failed to start chat session: {e}[/red]")


@cli.command()
@click.option('--host', default='127.0.0.1', help='Web server host')
@click.option('--port', default=8000, help='Web server port')
@click.option('--reload', is_flag=True, help='Enable auto-reload for development')
@handle_cli_error
def web(host: str, port: int, reload: bool):
    """Start the web server for browser-based chat interface."""
    console.print(f"[bold blue]🌐 Starting Web Server on http://{host}:{port}[/bold blue]")
    
    settings = get_settings()
    
    try:
        settings.validate_api_key()
    except ValueError as e:
        console.print(f"[red]❌ {e}[/red]")
        return
    
    try:
        from demo_chatbot.web_server import run_server
        
        console.print(f"[dim]Access the chat interface at: http://{host}:{port}[/dim]")
        console.print(f"[dim]API documentation at: http://{host}:{port}/api/docs[/dim]")
        console.print("[yellow]Press Ctrl+C to stop the server[/yellow]\n")
        
        run_server(host=host, port=port, reload=reload)
        
    except ImportError as e:
        console.print(f"[red]❌ Web server dependencies not installed: {e}[/red]")
        console.print("[yellow]Install web dependencies with: pip install -e .[dev][/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Failed to start web server: {e}[/red]")


def main():
    """Main entry point for the demo-chatbot CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()