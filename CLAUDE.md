# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A demo chatbot repository containing Python scripts that demonstrate integration with AI language models, specifically using Moonshot AI's API through both LangChain and direct OpenAI-compatible endpoints. **Running on Windows platform**.

## Refactored Structure

The project has been reorganized into a clean, modular structure:

```
demo_chatbot/
├── chatbot/                    # Main chatbot package
│   ├── api/                    # API integration modules
│   │   ├── langchain/          # LangChain integration
│   │   │   └── moonshot_langchain.py
│   │   ├── openai/             # OpenAI-compatible client
│   │   │   └── moonshot_openai.py
│   │   └── direct/             # Direct API calls
│   ├── config/                 # Configuration management
│   ├── examples/               # Usage examples
│   ├── tests/                  # Test suites
│   └── utils/                  # Utility functions
├── simple_demo.py              # Simple demo entry point
├── demo-demo.bat               # Windows batch file for demo
└── requirements.txt            # Dependencies
```

## Architecture & Components (Updated)

- **chatbot/api/langchain/moonshot_langchain.py**: Uses LangChain's MoonshotChat wrapper for conversational AI
- **chatbot/api/openai/moonshot_openai.py**: Direct OpenAI API client integration with Moonshot AI
- **simple_demo.py**: Simple demo script for testing both integrations
- Both scripts target Moonshot AI's API (base_url: https://api.moonshot.cn/v1)

## Common Commands (Windows)

### Running Scripts
```cmd
# Run the demo
python simple_demo.py

# Run individual test scripts
python chatbot/examples/basic/langchain_basic.py
python chatbot/examples/basic/openai_basic.py

# Run demo via batch file
demo-demo.bat
```

### Environment Setup (Windows)
```cmd
# Install dependencies
pip install -r requirements.txt

# Or install specific packages
pip install langchain langchain-community openai

# Configuration is automatically loaded from .env file
# Create .env file with your API key:
echo MOONSHOT_API_KEY=your_key_here > .env
```

### Development Workflow
1. Set environment variable: `set MOONSHOT_API_KEY=your_key_here`
2. Install dependencies: `pip install -r requirements.txt`
3. Run demo: `python simple_demo.py` or `demo-demo.bat`
4. Test individual components: `python chatbot/examples/basic/langchain_basic.py`

## Key Libraries Used
- `langchain_community.chat_models.moonshot`: Moonshot AI integration via LangChain
- `openai`: OpenAI Python client (used with Moonshot's compatible endpoint)
- `langchain.schema`: Message classes for conversation formatting

## API Configuration
- **Provider**: Moonshot AI (https://api.moonshot.cn/v1)
- **Models**: moonshot-v2 (LangChain), moonshot-v1-8k (direct API)
- **Authentication**: API key via environment variable `MOONSHOT_API_KEY`

## File Location Changes
- **Original test1.py** → **chatbot/api/langchain/moonshot_langchain.py**
- **Original test2.py** → **chatbot/api/openai/moonshot_openai.py**
- **Test scripts** → **chatbot/examples/basic/** and **chatbot/tests/**