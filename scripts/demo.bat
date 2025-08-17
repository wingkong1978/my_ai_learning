@echo off
REM Demo Script for demo-chatbot
REM Runs comprehensive demonstrations of all features

echo 🤖 Starting demo-chatbot comprehensive demo...
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
echo 🎯 Starting LangGraph Agent Demo...
echo ======================================

python -c "
import asyncio
from demo_chatbot.agents.langgraph_agent import LangGraphAgent

async def run_demo():
    agent = LangGraphAgent()
    
    demo_queries = [
        'Hello! What can you do?',
        'List the files in the current directory',
        'Create a new file called demo_test.txt with the content Hello from the demo!',
        'Calculate 25 * 4 + 10',
        'Read the content of the demo_test.txt file you just created',
        'What is the square root of 144?',
        'Search for Python programming tutorials (mock search)',
        'Create a simple Python script that prints \"Hello World\"',
        'List all Python files in the current directory',
        'Thank you for the demonstration!'
    ]
    
    print('🚀 Starting comprehensive demo...')
    print()
    
    for i, query in enumerate(demo_queries, 1):
        print(f'[{i}/10] User: {query}')
        try:
            response = await agent.run(query)
            print(f'    🤖 Agent: {response}')
            print()
        except Exception as e:
            print(f'    ❌ Error: {e}')
            print()
    
    print('✅ Demo completed successfully!')

asyncio.run(run_demo())
"

echo.
echo 🧹 Cleaning up demo files...
if exist "demo_test.txt" del demo_test.txt
if exist "hello_world.py" del hello_world.py

echo.
echo 🎉 Demo completed!
echo.
echo 📖 Available next steps:
echo   scripts\interactive.bat - Start interactive chat
echo   scripts\test.bat       - Run full test suite
echo   python src\demo_chatbot\cli.py --help - Show CLI commands
echo.
pause