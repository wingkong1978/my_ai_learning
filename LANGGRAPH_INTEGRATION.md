# LangGraph Integration Guide

This document provides comprehensive guidance for using LangGraph with the demo chatbot project.

## Overview

The LangGraph integration provides advanced AI agent capabilities including:
- **Conversational Memory**: Maintain context across multiple interactions
- **Tool Integration**: Execute file operations, calculations, and system commands
- **Multi-Client Support**: Seamlessly switch between LangChain and OpenAI clients
- **Workflow Management**: Structured conversation flow with state management

## Architecture

```
chatbot/
├── api/
│   └── langgraph/
│       ├── __init__.py
│       ├── langgraph_client.py      # Main LangGraph client
│       └── langgraph_workflows.py   # Workflow implementations
├── examples/
│   └── langgraph_examples.py        # Usage examples
└── tests/
    └── test_langgraph_integration.py # Test suite
```

## Quick Start

### 1. Install Dependencies

```bash
pip install langgraph langchain-core langchain-community
```

### 2. Set API Key

Create or update your `.env` file:
```
MOONSHOT_API_KEY=your_actual_api_key_here
```

### 3. Basic Usage

```python
import asyncio
from chatbot.api.langgraph.langgraph_client import LangGraphChatClient

async def demo():
    client = LangGraphChatClient()
    response = await client.chat("Hello! What can you do?")
    print(response)

asyncio.run(demo())
```

## Available Workflows

### 1. ChatWorkflow (Simple Chat)

Basic chat without tools:

```python
from chatbot.api.langgraph.langgraph_workflows import ChatWorkflow

async def simple_chat():
    workflow = ChatWorkflow()
    messages = [{"role": "user", "content": "Hello!"}]
    response = await workflow.run(messages)
    print(response)
```

### 2. ToolWorkflow (With Tools)

Chat with file operations and calculations:

```python
from chatbot.api.langgraph.langgraph_workflows import ToolWorkflow

async def tool_demo():
    workflow = ToolWorkflow()
    
    # File operations
    await workflow.run("Create a file called test.txt with content 'Hello World'")
    
    # Calculations
    result = await workflow.run("Calculate 15 * 23 + 7")
    print(result)
```

### 3. AdvancedWorkflow (Multi-Client)

Compare responses from different clients:

```python
from chatbot.api.langgraph.langgraph_workflows import AdvancedWorkflow

async def compare_clients():
    workflow = AdvancedWorkflow()
    response = await workflow.run("Compare LangChain and OpenAI responses for Python")
    print(response)
```

## Features

### Conversation Memory

Maintain context across conversations using thread IDs:

```python
client = LangGraphChatClient()

# Thread 1: Personal conversation
await client.chat("My name is Alice", thread_id="personal")
await client.chat("What is my name?", thread_id="personal")  # Remembers Alice

# Thread 2: Work conversation  
await client.chat("My project is AI", thread_id="work")
await client.chat("Tell me about my project", thread_id="work")  # Remembers AI
```

### Available Tools

The ToolWorkflow provides these tools:

- **read_file**: Read file contents
- **write_file**: Write content to files
- **list_files**: List directory contents
- **calculate**: Evaluate mathematical expressions
- **get_system_info**: Get system information

### Streaming Support

Get real-time responses:

```python
async def streaming_demo():
    client = LangGraphChatClient()
    
    async for chunk in client.stream_chat("Tell me a story"):
        print(chunk, end="")
```

## Examples

### Run All Examples

```bash
python chatbot/examples/langgraph_examples.py
```

### Individual Examples

```bash
# Basic chat
python -c "from chatbot.examples.langgraph_examples import LangGraphExamples; import asyncio; asyncio.run(LangGraphExamples().basic_chat_example())"

# Tool usage
python -c "from chatbot.examples.langgraph_examples import LangGraphExamples; import asyncio; asyncio.run(LangGraphExamples().tool_usage_example())"

# Multi-client comparison
python -c "from chatbot.examples.langgraph_examples import LangGraphExamples; import asyncio; asyncio.run(LangGraphExamples().multi_client_example())"
```

## CLI Usage

The project includes command-line interfaces:

### Basic CLI
```bash
# Check environment
python -m demo_chatbot.cli check

# Run demo
python -m demo_chatbot.cli demo

# Interactive chat
python -m demo_chatbot.cli interactive

# Chat with memory
python -m demo_chatbot.cli chat --thread-id my_conversation
```

### Main Script
```bash
# Run all checks
python main.py --check

# Install dependencies
python main.py --install

# Run demo
python main.py --demo

# Interactive mode
python main.py --interactive
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest chatbot/tests/test_langgraph_integration.py -v

# Run with coverage
pytest chatbot/tests/test_langgraph_integration.py --cov=chatbot.api.langgraph -v
```

## Configuration

### Environment Variables

- `MOONSHOT_API_KEY`: Your Moonshot AI API key (required)
- `MOONSHOT_BASE_URL`: API endpoint (default: https://api.moonshot.cn/v1)

### Model Configuration

```python
# Custom model and parameters
client = LangGraphChatClient(
    api_key="your-key",
    model="kimi-latest",
)

workflow = ToolWorkflow(
    api_key="your-key",
    model="moonshot-v1-8k"
)
```

## Integration with Existing Code

### Using with LangChain Client

```python
from chatbot.api.langchain.moonshot_langchain import MoonshotLangChainClient
from chatbot.api.langgraph.langgraph_client import LangGraphChatClient

# Existing LangChain usage
langchain_client = MoonshotLangChainClient()

# Enhanced with LangGraph
langgraph_client = LangGraphChatClient()
```

### Using with OpenAI Client

```python
from chatbot.api.openai.moonshot_openai import MoonshotOpenAIClient
from chatbot.api.langgraph.langgraph_client import LangGraphChatClient

# Existing OpenAI usage
openai_client = MoonshotOpenAIClient()

# Enhanced with LangGraph
langgraph_client = LangGraphChatClient()
```

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```
   ValueError: MOONSHOT_API_KEY is required
   ```
   Solution: Set the environment variable or pass api_key parameter

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'langgraph'
   ```
   Solution: Install dependencies
   ```bash
   pip install langgraph langchain-core langchain-community
   ```

3. **Network Issues**
   ```
   ConnectionError: Failed to connect to API
   ```
   Solution: Check internet connection and API key validity

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## API Reference

### LangGraphChatClient

Main client class for LangGraph integration.

#### Methods

- `async chat(user_input, thread_id="default")`: Send chat message
- `async stream_chat(user_input, thread_id="default")`: Stream chat response
- `get_conversation_history(thread_id="default")`: Get conversation history

### ChatWorkflow

Simple chat workflow without tools.

#### Methods

- `async run(messages, thread_id="default")`: Run chat workflow

### ToolWorkflow

Chat workflow with tools for file operations and calculations.

#### Methods

- `async run(user_input, thread_id="default")`: Run tool workflow

### AdvancedWorkflow

Advanced workflow with multi-client support.

#### Methods

- `async run(user_input, thread_id="default")`: Run advanced workflow

## Contributing

To add new workflows or tools:

1. Create new workflow class in `langgraph_workflows.py`
2. Add corresponding tests in `test_langgraph_integration.py`
3. Add usage examples in `langgraph_examples.py`
4. Update this documentation

## Next Steps

- Explore more complex workflows
- Add custom tools
- Implement persistent memory storage
- Add web search and API integration tools
- Create custom agent behaviors