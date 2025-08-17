@echo off
REM Windows Setup Script for demo-chatbot
REM Run this from the project root directory

echo Setting up demo-chatbot project...

REM Check if Python is available
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [OK] Python detected

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip
    pause
    exit /b 1
)

REM Install package in development mode
echo [INFO] Installing package in development mode...
pip install -e ".[dev]"
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating .env file...
    copy .env.example .env > nul
    if errorlevel 1 (
        echo [ERROR] Failed to create .env file
        pause
        exit /b 1
    )
    echo [WARN] Please edit .env file with your MOONSHOT_API_KEY
)

REM Create directories
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "temp" mkdir temp

echo.
echo [OK] Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your MOONSHOT_API_KEY
echo 2. Run: demo-check.bat
echo 3. Run: demo-demo.bat
echo 4. Run: demo-interactive.bat
echo.
pause