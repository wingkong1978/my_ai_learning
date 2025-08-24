@echo off
REM Development Web Server Script with Auto-Reload
REM Run this from the project root directory for development

echo Starting Demo Chatbot Web Server in Development Mode...

REM Check virtual environment
venv\Scripts\python.exe --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Install/update dependencies
echo [INFO] Installing/updating dependencies...
venv\Scripts\pip.exe install -e .

REM Start development server with auto-reload
echo [INFO] Starting development server with auto-reload...
echo [INFO] Server will restart automatically when files change
echo [INFO] Access: http://127.0.0.1:8000
echo [INFO] API Docs: http://127.0.0.1:8000/api/docs
echo [WARN] Press Ctrl+C to stop the server
echo.

venv\Scripts\demo-chatbot.exe web --host 127.0.0.1 --port 8000 --reload

echo.
echo [OK] Development server stopped
pause