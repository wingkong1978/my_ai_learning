# Demo Chatbot - LangChain + LangGraph + MCP + Agent Integration

A comprehensive demonstration project showcasing the integration of modern AI agent technologies including LangChain, LangGraph, MCP (Model Context Protocol), and conversational agents with Moonshot AI's language models.

## 🚀 Features

- **Multi-Modal Integration**: Combines LangChain, LangGraph, and MCP for advanced AI agent capabilities
- **Moonshot AI Integration**: Uses Moonshot AI's powerful language models via both LangChain and direct API
- **Conversational Memory**: Persistent conversation memory with thread-based isolation
- **Tool Integration**: Built-in tools for file operations, calculations, directory listing, and web search
- **Windows-Optimized**: Complete Windows batch scripts for easy setup and usage
- **CLI Interface**: Rich command-line interface with colorful output and interactive modes
- **MCP Server**: Model Context Protocol server for external tool integration
- **Production Ready**: Proper packaging, configuration management, and logging

## 📋 Prerequisites

- **Python 3.8+** (3.8-3.12 supported)
- **Windows 10/11** (optimized for Windows with batch scripts)
- **Moonshot AI API Key** (get from [Moonshot AI](https://platform.moonshot.cn/))

## 🔧 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd demo_chatbot

# Windows: Use the automated setup script
setup.bat
```

### 2. Configure API Key

Create a `.env` file in the project root:

```env
MOONSHOT_API_KEY=your_moonshot_api_key_here
# Optional configurations
DEFAULT_MODEL=kimi-latest
TEMPERATURE=0.7
MAX_TOKENS=1000
```

### 3. Run Demos

```bash
# Check environment setup
demo-check.bat

# Run comprehensive demo
demo-demo.bat

# Start interactive chat
demo-interactive.bat
```

## 🎯 Usage

### Command Line Interface

After setup, use the CLI commands:

```bash
# Activate virtual environment first
venv\Scripts\activate

# Check setup
demo-chatbot check

# Install dependencies
demo-chatbot install

# Run demo
demo-chatbot demo

# Interactive chat mode
demo-chatbot interactive

# Start MCP server
demo-chatbot mcp-server

# Run examples
demo-chatbot examples

# Chat with specific thread ID
demo-chatbot chat --thread-id my-session
```

### Direct Python Usage

```python
import asyncio
from demo_chatbot.agents.langgraph_agent import LangGraphAgent

async def main():
    agent = LangGraphAgent()
    
    # Simple query
    response = await agent.run("What can you do?")
    print(response)
    
    # File operations
    await agent.run("Create a file called hello.txt with 'Hello World'")
    content = await agent.run("Read the hello.txt file")
    print(content)

asyncio.run(main())
```

## 🏗️ Architecture

### Core Components

1. **LangGraphAgent** (`src/demo_chatbot/agents/langgraph_agent.py`)
   - Advanced agent with conversation memory
   - Tool integration and workflow management
   - State management with LangGraph

2. **MCP Server** (`src/demo_chatbot/servers/mcp_server.py`)
   - Model Context Protocol implementation
   - External tool integration
   - Standardized AI tool interface

3. **CLI Interface** (`src/demo_chatbot/cli.py`)
   - Rich command-line interface
   - Interactive chat modes
   - Comprehensive demos and examples

4. **Configuration** (`src/demo_chatbot/config/settings.py`)
   - Environment-based configuration
   - Validation and settings management
   - Proxy and logging support

### Available Tools

The agent includes these built-in tools:

- **File Operations**: Read, write, and manage files
- **Directory Listing**: Browse file system contents
- **Calculator**: Evaluate mathematical expressions
- **Web Search**: Mock web search functionality
- **System Info**: Get system and environment information

## 📁 Project Structure

```
demo_chatbot/
├── src/demo_chatbot/           # Main package
│   ├── agents/                 # LangGraph agents
│   │   └── langgraph_agent.py  # Main agent implementation
│   ├── servers/                # MCP servers
│   │   └── mcp_server.py       # MCP server implementation
│   ├── config/                 # Configuration
│   │   └── settings.py         # Settings management
│   ├── utils/                  # Utilities
│   │   └── logger.py           # Logging setup
│   └── cli.py                  # Command-line interface
├── tests/                      # Test suite
├── examples/                   # Usage examples
├── *.bat                       # Windows batch scripts
├── requirements.txt            # Dependencies
├── pyproject.toml             # Package configuration
└── README.md                  # This file
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Run specific test categories
python -m pytest tests/test_agents.py
python -m pytest tests/test_servers.py
python -m pytest tests/test_config.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MOONSHOT_API_KEY` | Required API key for Moonshot AI | - |
| `DEFAULT_MODEL` | Default AI model | `kimi-latest` |
| `TEMPERATURE` | Response creativity (0-1) | `0.7` |
| `MAX_TOKENS` | Maximum response length | `1000` |
| `WORKING_DIRECTORY` | Default working directory | `.` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `HTTP_PROXY` | HTTP proxy for API calls | - |
| `HTTPS_PROXY` | HTTPS proxy for API calls | - |

### Advanced Configuration

Create a `.env` file with custom settings:

```env
# API Configuration
MOONSHOT_API_KEY=your_key_here
DEFAULT_MODEL=kimi-latest
TEMPERATURE=0.8
MAX_TOKENS=2000

# MCP Server
MCP_SERVER_NAME=demo-chatbot-mcp
MCP_HOST=localhost
MCP_PORT=8080

# File System
WORKING_DIRECTORY=./data
MAX_FILE_SIZE=10485760
ALLOWED_FILE_EXTENSIONS=.txt,.py,.md,.json

# Proxy (if needed)
HTTP_PROXY=http://127.0.0.1:9328
HTTPS_PROXY=http://127.0.0.1:9328

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=./logs/chatbot.log
```

## 🚀 Advanced Usage

### Custom Tools

Extend the agent with custom tools:

```python
from langchain_core.tools import tool
from demo_chatbot.agents.langgraph_agent import LangGraphAgent

@tool
def custom_tool(input_data: str) -> str:
    """Your custom tool description"""
    return f"Processed: {input_data}"

# Add to agent
agent = LangGraphAgent()
agent.tools.append(custom_tool)
```

### Thread-Based Conversations

```python
# Different conversation threads
await agent.run("Hello!", thread_id="user1")
await agent.run("Remember my name is Alice", thread_id="user1")

# Separate conversation
await agent.run("Hello!", thread_id="user2")
await agent.run("What's my name?", thread_id="user2")  # Won't remember Alice
```

### Streaming Responses

```python
# Stream responses for real-time output
async for chunk in agent.stream("Tell me a long story"):
    print(chunk, end="", flush=True)
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run code formatting
black src/
isort src/

# Type checking
mypy src/

# Linting
flake8 src/
```

### Project Scripts

| Script | Purpose |
|--------|---------|
| `setup.bat` | Initial project setup |
| `demo-check.bat` | Environment validation |
| `demo-demo.bat` | Run comprehensive demo |
| `demo-interactive.bat` | Start interactive chat |
| `main.py` | Unified entry point with CLI |

## 📊 Examples

The project includes comprehensive examples covering:

1. **Basic Conversations**: Simple Q&A and chat
2. **File Operations**: Create, read, update, and delete files
3. **Calculations**: Mathematical computations and expressions
4. **System Operations**: Directory listing and system info
5. **Advanced Features**: Thread memory and tool usage

Run examples with:
```bash
demo-chatbot examples
```

## 🔍 Troubleshooting

### Common Issues

1. **API Key Issues**
   ```bash
   # Check if API key is set
   demo-chatbot check
   ```

2. **Virtual Environment**
   ```bash
   # Recreate virtual environment
   rmdir /s venv
   setup.bat
   ```

3. **Dependencies**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

4. **Proxy Issues**
   ```bash
   # Set proxy in .env file
   HTTP_PROXY=http://your-proxy:port
   HTTPS_PROXY=http://your-proxy:port
   ```

### Debug Mode

Enable debug logging:
```bash
# Set log level
set LOG_LEVEL=DEBUG

# Run with debug output
demo-chatbot interactive
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Moonshot AI](https://www.moonshot.cn/) for providing the AI models
- [LangChain](https://langchain.dev/) for the framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) for workflow management
- [MCP](https://modelcontextprotocol.io/) for standardized tool integration

## 📞 Support

For support and questions:
- Check the [Issues](https://github.com/example/demo-chatbot/issues) page
- Review the [Documentation](docs/)
- Join our [Discord](https://discord.gg/example)

---

**Made with ❤️ for the AI community**