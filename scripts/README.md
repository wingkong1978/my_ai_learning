# Demo Chatbot Scripts

This directory contains Windows batch scripts for easy project management and initialization.

## 📋 Script Overview

| Script | Purpose | Usage |
|--------|---------|--------|
| `init.bat` | **Project Initialization** | First-time setup, creates directories and .env file |
| `setup.bat` | **Environment Setup** | Install dependencies and configure virtual environment |
| `check.bat` | **Environment Validation** | Check all requirements and configuration |
| `demo.bat` | **Run Demo** | Execute comprehensive feature demonstration |
| `interactive.bat` | **Interactive Chat** | Start interactive chat with the AI agent |
| `test.bat` | **Run Tests** | Execute test suite and validation |

## 🚀 Quick Start

### For New Users

1. **First Time Setup:**
   ```cmd
   scripts\init.bat
   ```

2. **Install Dependencies:**
   ```cmd
   scripts\setup.bat
   ```

3. **Validate Setup:**
   ```cmd
   scripts\check.bat
   ```

4. **Run Demo:**
   ```cmd
   scripts\demo.bat
   ```

### Daily Usage

| Task | Command |
|------|---------|
| Interactive Chat | `scripts\interactive.bat` |
| Run Tests | `scripts\test.bat` |
| Check Environment | `scripts\check.bat` |
| Run Demo | `scripts\demo.bat` |

## 📝 Detailed Instructions

### 1. Project Initialization (`init.bat`)

**Purpose:** Sets up the project structure for the first time

**What it does:**
- Creates required directories (`logs/`, `data/`, `temp/`, etc.)
- Creates `.env` file with default configuration
- Validates Python installation
- Provides next steps guidance

**Usage:**
```cmd
scripts\init.bat
```

### 2. Environment Setup (`setup.bat`)

**Purpose:** Configures the Python environment and installs dependencies

**What it does:**
- Creates Python virtual environment
- Installs all dependencies from `requirements.txt`
- Installs package in development mode
- Validates the installation

**Usage:**
```cmd
scripts\setup.bat
```

### 3. Environment Check (`check.bat`)

**Purpose:** Validates that everything is correctly configured

**What it checks:**
- Python installation and version
- Virtual environment status
- All required dependencies
- API key configuration
- Directory structure
- Basic functionality

**Usage:**
```cmd
scripts\check.bat
```

### 4. Demo Runner (`demo.bat`)

**Purpose:** Runs comprehensive demonstrations of all features

**What it demonstrates:**
- Basic conversation
- File operations (create, read, write)
- Mathematical calculations
- Directory listing
- Web search (mock)
- Python script creation

**Usage:**
```cmd
scripts\demo.bat
```

### 5. Interactive Chat (`interactive.bat`)

**Purpose:** Starts an interactive chat session with the AI agent

**Features:**
- Rich terminal interface with colors
- Real-time conversation
- Built-in help system
- Command shortcuts (quit, help, clear, status)
- Error handling

**Usage:**
```cmd
scripts\interactive.bat
```

**Available Commands:**
- `quit`, `exit`, `q` - Exit the chat
- `help` - Show help information
- `clear` - Clear the screen
- `status` - Show system status

### 6. Test Runner (`test.bat`)

**Purpose:** Runs comprehensive tests and validation

**What it tests:**
- All Python imports
- Configuration settings
- Basic functionality
- Available test suites
- Environment validation

**Usage:**
```cmd
scripts\test.bat
```

## 🔧 Troubleshooting

### Common Issues

1. **"Python not found"**
   - Install Python 3.8+ from python.org
   - Add Python to PATH

2. **"Virtual environment not found"**
   - Run `scripts\setup.bat` first

3. **"API key missing"**
   - Edit `.env` file and add your `MOONSHOT_API_KEY`

4. **"Dependencies missing"**
   - Run `scripts\setup.bat` again

### Debug Mode

For detailed logging, set environment variables before running scripts:

```cmd
set LOG_LEVEL=DEBUG
scripts\interactive.bat
```

## 📁 Script Directory Structure

```
scripts/
├── init.bat          # Project initialization
├── setup.bat         # Environment setup
├── check.bat         # Environment validation
├── demo.bat          # Run demo
├── interactive.bat   # Interactive chat
├── test.bat          # Run tests
└── README.md         # This file
```

## 🎯 Usage Examples

### Complete Setup Workflow

```cmd
# 1. Clone and initialize
git clone <repository>
cd demo_chatbot
scripts\init.bat

# 2. Add API key to .env file
notepad .env

# 3. Setup environment
scripts\setup.bat

# 4. Validate setup
scripts\check.bat

# 5. Run demo
scripts\demo.bat

# 6. Start interactive chat
scripts\interactive.bat
```

### Quick Commands

```cmd
# Check everything is working
scripts\check.bat

# Start chatting immediately
scripts\interactive.bat

# Run full test suite
scripts\test.bat

# See all features in action
scripts\demo.bat
```

## 📝 Notes

- All scripts are designed for **Windows CMD** (Command Prompt)
- Scripts automatically activate the virtual environment
- Scripts provide helpful error messages and next steps
- Scripts include color output for better readability
- Scripts are idempotent (can be run multiple times safely)

## 🚀 Next Steps

After running the scripts:

1. **Development:** Use `scripts\interactive.bat` for testing
2. **Integration:** Use the CLI: `demo-chatbot --help`
3. **Customization:** Edit `.env` file for configuration
4. **Testing:** Use `scripts\test.bat` for validation
5. **Examples:** Check `examples/` directory for more usage patterns