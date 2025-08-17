@echo off
echo Testing batch file functionality...

REM Test 1: Check Python
python --version
echo Python check complete

REM Test 2: Check .env loading
if exist .env (
    echo Found .env file
    for /f "tokens=*" %%i in (.env) do (
        echo Loaded: %%i
    )
) else (
    echo .env file not found
)

REM Test 3: Check Python import
python -c "import sys; sys.path.insert(0, '.'); import chatbot.config.settings; print('Import successful')"

REM Test 4: Run actual examples
echo Running LangChain example...
python chatbot/examples/basic/langchain_basic.py
echo.
echo Running OpenAI example...
python chatbot/examples/basic/openai_basic.py

echo Test complete
pause