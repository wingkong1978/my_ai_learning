@echo off
REM Demo Examples for demo-chatbot - Windows CMD Version
echo [INFO] Running demo-chatbot examples...
echo [INFO] Current directory: %CD%

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Set PYTHONPATH
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

REM Check dependencies
echo [INFO] Checking Python dependencies...
python -c "import sys; sys.path.insert(0, '.'); import chatbot.config.settings; print('Dependencies OK')" 2>nul
if errorlevel 1 (
    echo [INFO] Installing missing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check API key
echo [INFO] Validating API configuration...
python check_config.py
if errorlevel 1 (
    echo [ERROR] Configuration validation failed
    pause
    exit /b 1
)

echo [INFO] Starting examples demonstration...
echo.
echo ================================================
echo Running LangChain Basic Example...
echo ================================================
python chatbot/examples/basic/langchain_basic.py
echo.
echo ================================================
echo Running OpenAI Basic Example...
echo ================================================
python chatbot/examples/basic/openai_basic.py
echo.
echo ================================================
echo Examples completed!
echo ================================================
echo [OK] All examples finished successfully
pause