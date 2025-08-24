@echo off
REM Web Server Startup Script for Demo Chatbot
REM Run this from the project root directory

echo Starting Demo Chatbot Web Server...

REM Check if Python is available
venv\Scripts\python.exe --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Virtual environment not found or Python not available
    echo Please run setup.bat first to create the virtual environment
    pause
    exit /b 1
)

REM Check if web dependencies are installed
echo [INFO] Checking web server dependencies...
venv\Scripts\python.exe -c "import fastapi, uvicorn" > nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing web server dependencies...
    venv\Scripts\pip.exe install -e .
    if errorlevel 1 (
        echo [ERROR] Failed to install web dependencies
        pause
        exit /b 1
    )
)

REM Start the web server
echo [INFO] Starting web server...
echo [INFO] Access the chat interface at: http://127.0.0.1:8000
echo [INFO] API documentation at: http://127.0.0.1:8000/api/docs
echo [WARN] Press Ctrl+C to stop the server
echo.

venv\Scripts\demo-chatbot.exe web --host 127.0.0.1 --port 8000

if errorlevel 1 (
    echo [ERROR] Failed to start web server
    pause
    exit /b 1
)

echo.
echo [OK] Web server stopped
pause