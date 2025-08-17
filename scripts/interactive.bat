@echo off
REM Interactive Chat Script for demo-chatbot
REM Starts an interactive chat session with the AI agent

echo 🎯 Starting interactive chat mode...
echo Type 'quit' to exit, 'help' for available commands

echo.

REM Check if we're in the correct directory
if not exist "pyproject.toml" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if setup is complete
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Error: Virtual environment not found
    echo Run: scripts\setup.bat first
    pause
    exit /b 1
)

if not exist ".env" (
    echo ❌ Error: .env file not found
    echo Run: scripts\init.bat first
    pause
    exit /b 1
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo 🔑 Checking API configuration...
python -c "
import os
from demo_chatbot.config.settings import settings
try:
    settings.validate()
    print('✅ API configuration valid')
except ValueError as e:
    print(f'❌ {e}')
    print('Please set MOONSHOT_API_KEY in your .env file')
    exit(1)
"
if errorlevel 1 (
    pause
    exit /b 1
)

echo.
echo 🚀 Starting interactive chat...
echo =================================

python -c "
import asyncio
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from demo_chatbot.agents.langgraph_agent import LangGraphAgent

console = Console()

async def interactive_chat():
    agent = LangGraphAgent()
    
    console.print(Panel.fit(
        '''[bold blue]🤖 Interactive Chat with LangGraph Agent[/bold blue]
        
[dim]Available commands:[/dim]
• quit/exit/q - Exit the chat
• help - Show this help
• clear - Clear screen
• status - Show system status
• Any other text - Chat with the agent
        ''',
        border_style="blue"
    ))
    
    message_count = 0
    
    while True:
        try:
            user_input = Prompt.ask(f"\n[bold blue]You[/bold blue]")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("\n[bold green]👋 Goodbye! Thanks for chatting![/bold green]")
                break
            
            if user_input.lower() == 'help':
                table = Table(title="Available Commands", show_header=True, header_style="bold cyan")
                table.add_column("Command", style="cyan")
                table.add_column("Description", style="white")
                
                table.add_row("quit, exit, q", "Exit the chat")
                table.add_row("help", "Show this help message")
                table.add_row("clear", "Clear the screen")
                table.add_row("status", "Show system status")
                table.add_row("Any text", "Chat with the AI agent")
                
                console.print(table)
                continue
            
            if user_input.lower() == 'clear':
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                console.print("[dim]Screen cleared[/dim]")
                continue
                
            if user_input.lower() == 'status':
                import datetime
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                status_table = Table(title="System Status", show_header=False)
                status_table.add_column("Property", style="cyan")
                status_table.add_column("Value", style="white")
                
                status_table.add_row("Agent Type", "LangGraph Agent")
                status_table.add_row("Model", "kimi-latest")
                status_table.add_row("Memory", "Enabled (per session)")
                status_table.add_row("Messages", str(message_count))
                status_table.add_row("Current Time", now)
                
                console.print(status_table)
                continue
            
            if user_input.strip():
                message_count += 1
                
                with console.status("[bold green]🤖 Thinking..."):
                    try:
                        response = await agent.run(user_input)
                        
                        # Format response nicely
                        console.print(f"\n[bold green]🤖 Agent:[/bold green]")
                        console.print(Panel(response, border_style="green", expand=False))
                        
                    except Exception as e:
                        console.print(f"\n[red]❌ Error:[/red] {str(e)}")
                        console.print("[dim]Please check your API key and internet connection[/dim]")
                        
        except KeyboardInterrupt:
            console.print("\n\n[bold green]👋 Goodbye! Thanks for chatting![/bold green]")
            break
        except EOFError:
            console.print("\n\n[bold green]👋 Goodbye! Thanks for chatting![/bold green]")
            break
        except Exception as e:
            console.print(f"\n[red]❌ Unexpected error: {e}[/red]")
            console.print("[dim]Please restart the chat[/dim]")

asyncio.run(interactive_chat())
"

pause