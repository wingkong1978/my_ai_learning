@echo off
REM Project Initialization Script for demo-chatbot
REM Usage: Run from project root directory

echo 🚀 Initializing demo-chatbot project...
echo.

REM Check if we're in the correct directory
if not exist "pyproject.toml" (
    echo ❌ Error: Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo 📁 Creating project structure...

REM Create directories if they don't exist
if not exist "logs" mkdir logs
if not exist "data" mkdir data  
if not exist "temp" mkdir temp
if not exist "examples" mkdir examples
if not exist "docs" mkdir docs

REM Create logs subdirectories
if not exist "logs\agent" mkdir logs\agent
if not exist "logs\mcp" mkdir logs\mcp
if not exist "logs\cli" mkdir logs\cli

echo ✅ Project directories created

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    echo # Demo Chatbot Configuration > .env
    echo. >> .env
    echo # Required: Moonshot AI API Key >> .env
    echo MOONSHOT_API_KEY=your_moonshot_api_key_here >> .env
    echo. >> .env
    echo # Optional: Model Configuration >> .env
    echo DEFAULT_MODEL=kimi-latest >> .env
    echo TEMPERATURE=0.7 >> .env
    echo MAX_TOKENS=1000 >> .env
    echo. >> .env
    echo # MCP Server Configuration >> .env
    echo MCP_SERVER_NAME=demo-chatbot-mcp >> .env
    echo MCP_HOST=localhost >> .env
    echo MCP_PORT=8080 >> .env
    echo. >> .env
    echo # File System Configuration >> .env
    echo WORKING_DIRECTORY=. >> .env
    echo MAX_FILE_SIZE=10485760 >> .env
    echo ALLOWED_FILE_EXTENSIONS=.txt,.py,.md,.json,.yaml,.yml >> .env
    echo. >> .env
    echo # Logging Configuration >> .env
    echo LOG_LEVEL=INFO >> .env
    echo LOG_FILE=./logs/chatbot.log >> .env
    echo. >> .env
    echo ✅ .env file created - please edit with your API key
) else (
    echo ⚠️  .env file already exists - skipping
)

echo.
echo 🔧 Running basic validation...

REM Check Python version
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python detected

REM Create requirements check file
echo import sys > temp\check_python.py
echo print(f"Python version: {sys.version}") >> temp\check_python.py
echo print(f"Python executable: {sys.executable}") >> temp\check_python.py
python temp\check_python.py
del temp\check_python.py

echo.
echo 📋 Initialization Summary:
echo =========================
echo ✅ Project directories created
echo ✅ .env file created/validated
echo ✅ Python environment checked
echo.
echo 📝 Next Steps:
echo 1. Edit .env file with your MOONSHOT_API_KEY
echo 2. Run: scripts\setup.bat to install dependencies
echo 3. Run: scripts\check.bat to validate setup
echo 4. Run: scripts\demo.bat to test the demo
echo.
pause