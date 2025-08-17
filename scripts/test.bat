@echo off
REM Test Script for demo-chatbot
REM Runs comprehensive tests and validation

echo 🧪 Running demo-chatbot test suite...
echo.

REM Check if we're in the correct directory
if not exist "pyproject.toml" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if setup is complete
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Error: Virtual environment not found
    echo Run: scripts\setup.bat first
    pause
    exit /b 1
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📋 Running test validation...

REM Run pytest if available
python -c "
import subprocess
import sys

try:
    import pytest
    print('✅ pytest available')
    
    # Run tests
    print('')
    print('🧪 Running pytest test suite...')
    result = subprocess.run([sys.executable, '-m', 'pytest', '-v'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print('✅ All tests passed!')
        print(result.stdout)
    else:
        print('❌ Some tests failed:')
        print(result.stdout)
        if result.stderr:
            print('Errors:')
            print(result.stderr)
            
except ImportError:
    print('⚠️  pytest not available, running basic validation...')
    
    # Basic validation without pytest
    import os
    import sys
    
    tests_to_run = [
        'import demo_chatbot',
        'from demo_chatbot.config.settings import settings',
        'from demo_chatbot.agents.langgraph_agent import LangGraphAgent',
        'from demo_chatbot.servers.mcp_server import MCPServer'
    ]
    
    print('Running basic import tests...')
    for test in tests_to_run:
        try:
            exec(test)
            print('✅ %s' % test)
        except Exception as e:
            print('❌ %s: %s' % (test, str(e)))
            sys.exit(1)
    
    print('✅ Basic validation passed')
"

echo.
echo 🔍 Running additional validation...

python -c "
import os
import sys
from pathlib import Path
from demo_chatbot.config.settings import settings

print('Additional Validation:')
print('=' * 40)

# Check file structure
check_paths = [
    'src/demo_chatbot',
    'tests',
    'scripts',
    'logs',
    'data',
    '.env'
]

for path in check_paths:
    if os.path.exists(path):
        print('✅ %s' % path)
    else:
        print('❌ %s' % path)

# Check configuration
print('')
print('Configuration:')
try:
    settings.validate()
    print('✅ Settings validation passed')
except Exception as e:
    print('❌ Settings validation failed: %s' % str(e))

# Check Python version
print('')
print('Python Environment:')
print('  Python: %s' % sys.version)
print('  Executable: %s' % sys.executable)
print('  Platform: %s' % sys.platform)

# Check package info
try:
    from demo_chatbot import __version__
    print('  Package Version: %s' % __version__)
except:
    print('  Package Version: Unknown')

print('')
print('📊 Test Summary:')
print('  Run scripts\check.bat for detailed environment check')
print('  Run scripts\demo.bat for feature demonstration')
print('  Run scripts\interactive.bat for manual testing')
"

echo.
echo 🎯 Test suite completed!
echo.
echo 📈 Next steps:
echo   scripts\check.bat     - Detailed validation
echo   scripts\demo.bat      - Feature demonstration  
echo   scripts\interactive.bat - Manual testing
echo   python src\demo_chatbot\cli.py --help - CLI usage
echo.
pause