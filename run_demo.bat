@echo off
setlocal enabledelayedexpansion

REM Check if running in Windows
ver | findstr /i "Windows" > nul
if errorlevel 1 (
    echo [ERROR] This script must be run in Windows
    pause
    exit /b 1
)

echo [INFO] =================================================================
echo [INFO]                    Demo Chatbot - Script Launcher
echo [INFO] =================================================================
echo.
echo Available options:
echo 1. Run Demo Agent (Interactive)
echo 2. Run MCP Server
echo 3. Test Demo Agent
echo 4. Test MCP Server
echo 5. Run Master Menu
echo 6. Exit
echo.
set /p choice="Select option (1-6): "

if "%choice%"=="1" goto run_agent
if "%choice%"=="2" goto run_mcp
if "%choice%"=="3" goto test_agent
if "%choice%"=="4" goto test_mcp
if "%choice%"=="5" goto run_menu
if "%choice%"=="6" goto exit

echo [ERROR] Invalid choice. Please select 1-6.
pause
goto exit

:run_agent
echo [INFO] Starting Demo Agent...
cd /d "%~dp0\scripts"
python demo_agent.py
if errorlevel 1 echo [ERROR] Failed to run Demo Agent
goto exit

:run_mcp
echo [INFO] Starting MCP Server...
cd /d "%~dp0\scripts"
python mcp_server.py
if errorlevel 1 echo [ERROR] Failed to run MCP Server
goto exit

:test_agent
echo [INFO] Testing Demo Agent...
cd /d "%~dp0\scripts"
python test_agent.py
if errorlevel 1 echo [ERROR] Failed to test Demo Agent
goto exit

:test_mcp
echo [INFO] Testing MCP Server...
cd /d "%~dp0\scripts"
python test_mcp.py
if errorlevel 1 echo [ERROR] Failed to test MCP Server
goto exit

:run_menu
echo [INFO] Starting Master Menu...
cd /d "%~dp0\scripts"
python run_demo.py
if errorlevel 1 echo [ERROR] Failed to run Master Menu
goto exit

:exit
echo [INFO] Exiting...
endlocal
pause
exit /b 0