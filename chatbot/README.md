# Demo Chatbot - Refactored Structure

A comprehensive demo chatbot showcasing integration with Moonshot AI's API through multiple approaches: LangChain, OpenAI-compatible endpoints, and direct API calls.

## Project Structure

```
chatbot/
├── api/                    # API integration modules
│   ├── __init__.py
│   ├── langchain/         # LangChain integration
│   │   ├── __init__.py
│   │   └── moonshot_langchain.py
│   ├── openai/            # OpenAI-compatible client
│   │   ├── __init__.py
│   │   └── moonshot_openai.py
│   └── direct/            # Direct API calls
│       └── __init__.py
├── config/                # Configuration management
│   ├── __init__.py
│   └── settings.py
├── examples/              # Usage examples
│   ├── __init__.py
│   ├── basic/            # Basic usage examples
│   │   ├── langchain_basic.py
│   │   └── openai_basic.py
│   └── advanced/         # Advanced usage examples
│       ├── langchain_demo_simple.py
│       ├── langchain_demo_fixed.py
│       └── langchain_think_act_review.py
├── models/               # Data models and schemas
│   └── __init__.py
├── tests/                # Test suites
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_langchain_quick.py
│   │   └── test_mcp_client.py
│   └── integration/
├── utils/                # Utility functions
│   └── __init__.py
└── scripts/              # Utility scripts
```

## Quick Start

### Environment Setup

1. Set your Moonshot API key:
```bash
export MOONSHOT_API_KEY="your_api_key_here"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage Examples

#### LangChain Integration
```python
from chatbot.api.langchain.moonshot_langchain import MoonshotLangChainClient

client = MoonshotLangChainClient()
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"}
]
response = client.chat_completion(messages)
print(response)
```

#### OpenAI-Compatible Client
```python
from chatbot.api.openai.moonshot_openai import MoonshotOpenAIClient

client = MoonshotOpenAIClient()
messages = [
    {"role": "system", "content": "You are a creative AI."},
    {"role": "user", "content": "Tell me a story"}
]
response = client.chat_completion(messages)
print(response)
```

### Running Tests

```bash
# Run all tests
python -m pytest chatbot/tests/

# Run specific test files
python chatbot/tests/unit/test_langchain_quick.py
python chatbot/tests/unit/test_mcp_client.py
```

### Running Examples

```bash
# Basic examples
python chatbot/examples/basic/langchain_basic.py
python chatbot/examples/basic/openai_basic.py

# Advanced examples
python chatbot/examples/advanced/langchain_demo_simple.py
python chatbot/examples/advanced/langchain_demo_fixed.py
```

## API Reference

### MoonshotLangChainClient
- `__init__(api_key=None, model="kimi-latest")`
- `chat_completion(messages, **kwargs)`

### MoonshotOpenAIClient
- `__init__(api_key=None, base_url="https://api.moonshot.cn/v1")`
- `chat_completion(messages, model="moonshot-v1-8k", temperature=0.8, max_tokens=100, **kwargs)`

## Configuration

Configuration is managed through environment variables:
- `MOONSHOT_API_KEY`: Your Moonshot API key
- `MOONSHOT_BASE_URL`: API base URL (default: https://api.moonshot.cn/v1)

## Development

The project supports different environments:
- Development (default): Debug mode enabled
- Production: Optimized for production use

Set environment:
```bash
export CHATBOT_ENV="development"  # or "production"
```