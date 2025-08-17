# Demo Agent with MCP Integration

A working demo agent that demonstrates AI capabilities with file system integration using MCP-like tools.

## Features

- **Interactive CLI**: Real-time chat with the agent
- **File Operations**: Read, write, and list files/directories
- **System Information**: Get platform and environment details
- **Error Handling**: Robust error handling and user feedback
- **Async/Await**: Modern async Python patterns

## Quick Start

### 1. Test the Agent
```bash
# Run tests to verify everything works
python test_agent.py
```

### 2. Run Interactive Mode
```bash
# Start interactive agent session
python demo_agent.py

# Or use the batch file (Windows)
run_agent.bat
```

## Available Commands

When running the interactive agent, you can use these commands:

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show available commands | `help` |
| `read <file>` | Read a file | `read README.md` |
| `write <file> <content>` | Write to a file | `write hello.txt Hello World` |
| `ls [directory]` | List directory contents | `ls src` |
| `ls` | List current directory | `ls` |
| `info` | Get system information | `info` |
| `exit` | Exit the agent | `exit` |

## Example Usage

### Interactive Session
```
=== DemoAgent Demo Agent ===
Type 'help' for available commands or 'exit' to quit
------------------------------

Agent> help
Available commands:
- help: Show this help message
- read <file_path>: Read a file
- write <file_path> <content>: Write to a file
- ls [directory]: List directory contents
- info: Get system information
- exit: Exit the agent

Agent> info
{
  "success": true,
  "system": {
    "platform": "Windows",
    "platform_version": "10.0.22631",
    "python_version": "3.13.6",
    "cwd": "C:\\source\\RND\\demo_chatbot",
    "agent_name": "DemoAgent"
  }
}

Agent> write test.txt Hello from Demo Agent!
{
  "success": true,
  "message": "File written successfully",
  "file_path": "C:\\source\\RND\\demo_chatbot\\test.txt",
  "file_size": 25
}

Agent> read test.txt
{
  "success": true,
  "content": "Hello from Demo Agent!",
  "file_size": 25,
  "file_path": "C:\\source\\RND\\demo_chatbot\\test.txt"
}

Agent> ls .
{
  "success": true,
  "directory": "C:\\source\\RND\\demo_chatbot",
  "files": [...],
  "directories": [...],
  "total_items": 43
}
```

## Architecture

### Core Components

1. **DemoAgent Class** - Main agent implementation
2. **Tool Methods** - File system operations
3. **Command Processor** - Natural language command parsing
4. **Interactive Interface** - CLI for user interaction

### File Structure

```
demo_chatbot/
├── demo_agent.py          # Main agent implementation
├── test_agent.py          # Test script
├── run_agent.bat          # Windows launcher
├── AGENT_README.md        # This documentation
└── src/
    └── demo_chatbot/
        └── servers/       # MCP server implementations
```

## Development

### Adding New Tools

To add new tools to the agent:

1. Add the method to the `DemoAgent` class:
```python
async def new_tool(self, param1: str, param2: int = 0) -> Dict[str, Any]:
    """Description of the new tool"""
    try:
        # Implementation
        return {"success": True, "result": "..."}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

2. Add to the tools dictionary:
```python
self.tools = {
    ...existing tools...
    'new_tool': self.new_tool
}
```

3. Add command processing:
```python
elif command.startswith("new "):
    # Parse and call new_tool
```

### Integration with MCP

The agent uses the same tool interface as the MCP server, making it easy to:
- Share code between agent and MCP server
- Test tools independently
- Migrate from agent to full MCP server

## Testing

The agent includes comprehensive tests:

```bash
# Run all tests
python test_agent.py

# Test specific functionality
python -c "
import asyncio
from demo_agent import DemoAgent

async def test():
    agent = DemoAgent()
    result = await agent.get_system_info()
    print(result)

asyncio.run(test())
"
```

## Configuration

No configuration required! The agent works out of the box with sensible defaults.

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure you have write permissions in the current directory
2. **File Not Found**: Check that file paths are correct and files exist
3. **Encoding Issues**: Use appropriate encoding when reading/writing files

### Debug Mode

Enable debug output by setting environment variable:
```bash
set DEBUG=1
python demo_agent.py
```

## Next Steps

- Integrate with actual AI/LLM for natural language processing
- Add more sophisticated command parsing
- Implement persistent memory
- Add web search capabilities
- Create GUI interface