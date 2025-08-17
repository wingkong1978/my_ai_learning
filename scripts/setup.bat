@echo off
REM Setup Script for demo-chatbot - Install dependencies and configure environment
REM Usage: Run after init.bat

echo 🛠️  Setting up demo-chatbot environment...
echo.

REM Check if we're in the correct directory
if not exist "pyproject.toml" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if init.bat was run
if not exist ".env" (
    echo ❌ Error: .env file not found. Please run scripts\init.bat first
    pause
    exit /b 1
)

echo 📦 Checking Python environment...

REM Check Python version
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

echo ✅ Python detected

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ⚠️  Virtual environment already exists
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo 📈 Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Failed to upgrade pip (continuing anyway)
)

echo ⚙️  Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies from requirements.txt
    echo Trying basic installation...
    pip install langchain langgraph langchain-community langchain-core openai pydantic python-dotenv click rich
    if errorlevel 1 (
        echo ❌ Failed to install basic dependencies
        pause
        exit /b 1
    )
)

echo ✅ Dependencies installed successfully

echo 🔍 Validating installation...
python -c "
import sys
try:
    import demo_chatbot
    print('✅ demo_chatbot package imported successfully')
except ImportError as e:
    print(f'❌ Failed to import demo_chatbot: {e}')
    sys.exit(1)

try:
    from demo_chatbot.config.settings import settings
    print('✅ Settings module loaded')
except ImportError as e:
    print(f'❌ Failed to load settings: {e}')
    sys.exit(1)

print('✅ Basic validation passed')
"

if errorlevel 1 (
    echo ❌ Installation validation failed
    pause
    exit /b 1
)

echo.
echo 🎉 Setup complete!
echo.
echo 🚀 Quick Commands:
echo   scripts\check.bat    - Validate environment
echo   scripts\demo.bat     - Run comprehensive demo
echo   scripts\interactive.bat - Start interactive chat
echo   scripts\test.bat     - Run tests
echo.
echo 📖 Next steps:
echo   1. Edit .env file with your MOONSHOT_API_KEY
echo   2. Run scripts\check.bat to validate setup
echo   3. Run scripts\demo.bat to test features
echo.
pause