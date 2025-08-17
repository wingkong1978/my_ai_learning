@echo off
REM Environment Check Script for demo-chatbot
REM Validates all requirements and configuration

echo 🔍 Checking demo-chatbot environment...
echo.

REM Check if we're in the correct directory
if not exist "pyproject.toml" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

echo 📋 Checking requirements...

REM Check Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
) else (
    python --version
    echo ✅ Python is available
)

REM Check virtual environment
if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
) else (
    echo ❌ Virtual environment not found
    echo Run: scripts\setup.bat
    pause
    exit /b 1
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📦 Checking dependencies...
python -c "
import sys
import importlib

required_packages = [
    'demo_chatbot',
    'langchain',
    'langgraph',
    'langchain_community',
    'langchain_core',
    'openai',
    'pydantic',
    'python_dotenv',
    'click',
    'rich'
]

missing = []
for package in required_packages:
    try:
        importlib.import_module(package)
        print('✅ %s' % package)
    except ImportError:
        print('❌ %s' % package)
        missing.append(package)

if missing:
    print('')
    print('❌ Missing packages: %s' % str(missing))
    sys.exit(1)
else:
    print('')
    print('✅ All dependencies are installed')
"

if errorlevel 1 (
    echo ❌ Some dependencies are missing
    echo Run: scripts\setup.bat
    pause
    exit /b 1
)

echo 🔑 Checking configuration...
python -c "
import os
import sys
from pathlib import Path
from demo_chatbot.config.settings import settings

print('Configuration Check:')
print('=' * 30)

# Check API key
if settings.MOONSHOT_API_KEY:
    print('✅ MOONSHOT_API_KEY is set')
    print('   Model: %s' % settings.DEFAULT_MODEL)
    print('   Temperature: %s' % settings.TEMPERATURE)
    print('   Max Tokens: %s' % settings.MAX_TOKENS)
else:
    print('❌ MOONSHOT_API_KEY is missing')
    print('   Please add it to your .env file')

# Check directories
required_dirs = ['logs', 'data', 'temp', 'examples', 'docs']
for dir_name in required_dirs:
    if os.path.exists(dir_name):
        print('✅ %s/ directory exists' % dir_name)
    else:
        print('❌ %s/ directory missing' % dir_name)

# Check working directory
if settings.WORKING_DIRECTORY.exists():
    print('✅ Working directory: %s' % settings.WORKING_DIRECTORY)
else:
    print('❌ Working directory not found: %s' % settings.WORKING_DIRECTORY)

print('')
print('Environment Summary:')
print('  Python: %s' % sys.version)
venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
print('  Virtual Environment: %s' % ('Active' if venv_active else 'Inactive'))
print('  Package: demo-chatbot v0.1.0')
"

echo.
echo 🧪 Running basic functionality test...
python -c "
import asyncio
import sys
from demo_chatbot.config.settings import settings

async def test_basic():
    try:
        from demo_chatbot.agents.langgraph_agent import LangGraphAgent
        print('✅ LangGraphAgent import successful')
        
        if settings.MOONSHOT_API_KEY:
            agent = LangGraphAgent()
            print('✅ Agent initialization successful')
        else:
            print('⚠️  Skipping agent test (API key missing)')
            
    except Exception as e:
        print('❌ Basic test failed: %s' % str(e))

asyncio.run(test_basic())
"

echo.
echo 🎯 Environment check complete!
echo.
echo 🚀 Ready to use:
echo   scripts\demo.bat       - Run comprehensive demo
echo   scripts\interactive.bat - Start interactive chat
echo   scripts\test.bat       - Run full test suite
echo.
pause