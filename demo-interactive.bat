@echo off
REM Interactive Mode Script for demo-chatbot - Windows CMD Version

echo [INFO] Starting interactive mode...
echo [INFO] Current directory: %CD%

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Set PYTHONPATH for module imports
set PYTHONPATH=%CD%

REM Check for .env file
if exist .env (
    echo [INFO] Loading configuration from .env file...
    for /f "usebackq tokens=*" %%i in (".env") do (
        set "%%i"
    )
) else (
    echo [WARNING] .env file not found. Please create .env with MOONSHOT_API_KEY=your_key
)

REM Check dependencies and configuration
echo [INFO] Checking dependencies...
python -c "import sys; sys.path.insert(0, '.'); from chatbot.config.settings import Config; Config.validate(); print('[INFO] Configuration validated')" 2>nul
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
    python -c "from chatbot.config.settings import Config; Config.validate()" 2>nul
    if errorlevel 1 (
        echo [ERROR] Configuration validation failed
        pause
        exit /b 1
    )
)

echo [INFO] Starting interactive demo...
echo.
echo ================================================
echo Demo Chatbot - Interactive Mode
echo ================================================
python interactive_simple.py
if errorlevel 1 (
    echo [ERROR] Interactive mode failed to run
    pause
    exit /b 1
)

echo.
echo [OK] Interactive session ended
pause