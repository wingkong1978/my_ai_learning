@echo off
REM Demo Script for demo-chatbot - Windows Version

echo [INFO] Starting demo mode...
echo [INFO] Current directory: %CD%

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Set PYTHONPATH to include current directory for imports
set PYTHONPATH=%CD%

REM Check for .env file and load it
if exist .env (
    echo [INFO] Found .env file, loading configuration...
    for /f "tokens=*" %%i in (.env) do (
        set %%i
    )
    echo [INFO] Configuration loaded from .env
) else (
    echo [WARNING] .env file not found
    echo [INFO] Please create .env file with: MOONSHOT_API_KEY=your_key_here
)

REM Install/verify dependencies
echo [INFO] Checking dependencies...
pip show langchain >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing required dependencies...
    pip install langchain langchain-community openai
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Run the demo script
echo [INFO] Running demo script...
python simple_demo.py
if errorlevel 1 (
    echo [ERROR] Demo failed to run
    echo [INFO] Please check your API key and internet connection
    pause
    exit /b 1
)

echo [OK] Demo completed successfully
pause