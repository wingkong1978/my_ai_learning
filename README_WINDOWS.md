# Demo Chatbot - Windows Setup Guide

A comprehensive demo of LangChain + LangGraph + MCP + Agent integration, optimized for Windows environments.

## 🚀 Quick Start for Windows

### 1. Automatic Setup (Recommended)

**Run from project root directory**:
```cmd
setup.bat
```

### 2. Manual Setup

If you prefer manual setup:

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat

# Install package
pip install -e ".[dev]"

# Create .env file
copy .env.example .env
# Edit .env with your MOONSHOT_API_KEY
```

## 🎯 Windows Commands

After setup, use these Windows-friendly commands (all in project root):

```cmd
# Basic commands
demo-check.bat        # Check environment setup
demo-demo.bat         # Run agent demo
demo-interactive.bat  # Start interactive mode
demo-examples.bat     # Run all examples

# Direct Python commands (after activating venv)
venv\Scripts\activate.bat
python -m demo_chatbot.cli check
python -m demo_chatbot.cli demo
python -m demo_chatbot.cli interactive
```

## 🔧 Windows-Specific Configuration

### Environment Variables (.env file)
```ini
# Moonshot AI API Key (required)
MOONSHOT_API_KEY=your_moonshot_api_key_here

# Optional: Windows-specific paths
WORKING_DIRECTORY=C:\Users\YourName\Projects\demo_chatbot
LOG_FILE=logs\chatbot.log

# Optional: Proxy settings for corporate networks
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=https://proxy.company.com:8080
```

### Windows Path Considerations

- Use backslashes (`\`) in .env file paths
- Working directory defaults to project root
- Log files are created in `logs\` directory

## 🛠️ Troubleshooting

### Common Windows Issues

**1. Python not found**:
```cmd
# Check Python installation
python --version
where python

# If not found, add to PATH or use full path
C:\Python39\python.exe -m venv venv
```

**2. Virtual environment activation fails**:
```cmd
# Manual activation
venv\Scripts\activate.bat

# Or use PowerShell
venv\Scripts\Activate.ps1
```

**3. Package installation issues**:
```cmd
# Upgrade pip first
python -m pip install --upgrade pip

# Install with specific Python version
python -m pip install -e ".[dev]"

# Or try without extras
pip install -e .
```

**4. PowerShell execution policy**:
```powershell
# Run as Administrator if needed
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📁 Windows File Structure

After setup, your project will look like:
```
demo_chatbot/
├── venv/                      # Virtual environment
├── src/
│   └── demo_chatbot/
├── demo-check.bat            # Check environment
├── demo-demo.bat             # Run demo
├── demo-interactive.bat      # Interactive mode
├── demo-examples.bat         # Run examples
├── setup.bat                 # Setup script
├── logs/                     # Log files
├── data/                     # Application data
├── .env                      # Your environment file
└── ...
```

## 🚀 Getting Started

1. **Download/clone the project**
2. **Open Command Prompt in project directory**
3. **Run setup**:
   ```cmd
   setup.bat
   ```
4. **Check everything is working**:
   ```cmd
   demo-check.bat
   ```
5. **Run demo**:
   ```cmd
   demo-demo.bat
   ```
6. **Start chatting**:
   ```cmd
   demo-interactive.bat
   ```

## 📊 Performance Tips for Windows

- **Use SSD storage** for better file I/O performance
- **Exclude venv from antivirus scans** to improve speed
- **Use Windows Terminal** instead of Command Prompt
- **Enable long path support** if needed:
  ```cmd
  reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1
  ```

## 🔍 Testing on Windows

```cmd
# Run tests
venv\Scripts\activate.bat
python -m pytest tests\ -v

# Run specific test
python -m pytest tests\test_agents.py -v

# Run with coverage
python -m pytest tests\ --cov=demo_chatbot --cov-report=html
```

## 🎉 Ready to Use!

After setup, you can immediately start:

```cmd
# Simple chat
demo-interactive.bat

# Run examples
demo-examples.bat

# Check system
demo-check.bat
```

**All batch files work directly from the project root directory - no need to navigate to scripts folder!**