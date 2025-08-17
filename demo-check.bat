@echo off
REM Environment Check Script for demo-chatbot

echo [INFO] Checking environment setup...

REM Check if virtual environment is activated
python -c "import sys; exit(0 if sys.prefix != sys.base_prefix else 1)"
if errorlevel 1 (
    echo [ERROR] Virtual environment is not activated
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo [OK] Virtual environment is activated

REM Check if required packages are installed
python -c "import dotenv" 2>nul
if errorlevel 1 (
    echo [ERROR] Required packages are not installed
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo [OK] Required packages are installed

REM Check if .env file exists
if not exist ".env" (
    echo [ERROR] .env file not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo [OK] .env file exists

echo [OK] All checks passed!
pause