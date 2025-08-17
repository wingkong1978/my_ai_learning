# Demo Scripts Organization

This directory contains all the demo scripts and test utilities for the chatbot project.

## 📁 Script Structure

```
scripts/
├── run_demo.py           # Master launcher - run all demos
├── demo_agent.py         # Interactive AI agent with file operations
├── mcp_server.py         # MCP (Model Context Protocol) server
├── test_mcp.py           # Test script for MCP server
├── test_agent.py         # Test script for demo agent
├── run_agent.bat         # Windows launcher for demo agent
├── run_mcp.bat           # Windows launcher for MCP server
└── DEMO_SCRIPTS.md       # This documentation
```

## 🚀 Quick Start

### Option 1: Master Launcher (Recommended)
```bash
# Run the master launcher with menu
python run_demo.py
```

### Option 2: Individual Scripts
```bash
# Start MCP server
python mcp_server.py

# Start interactive agent
python demo_agent.py

# Run tests
python test_mcp.py
python test_agent.py
```

### Option 3: Windows Batch Files
```bash
# On Windows, use batch files
run_mcp.bat
run_agent.bat
```

## 📋 Available Scripts

### Core Scripts

| Script | Description | Usage |
|--------|-------------|--------|
| `run_demo.py` | Master launcher with interactive menu | `python run_demo.py` |
| `demo_agent.py` | Interactive AI agent with file tools | `python demo_agent.py` |
| `mcp_server.py` | MCP server for external integrations | `python mcp_server.py` |

### Test Scripts

| Script | Description | Usage |
|--------|-------------|--------|
| `test_mcp.py` | Test MCP server functionality | `python test_mcp.py` |
| `test_agent.py` | Test demo agent functionality | `python test_agent.py` |

### Launchers

| Script | Description | Usage |
|--------|-------------|--------|
| `run_agent.bat` | Windows launcher for agent | Double-click or `run_agent.bat` |
| `run_mcp.bat` | Windows launcher for MCP server | Double-click or `run_mcp.bat` |

## 🎯 Demo Agent Features

The `demo_agent.py` provides:
- **Interactive CLI** - Real-time chat interface
- **File Operations** - Read/write/list files and directories
- **System Information** - Platform and environment details
- **Error Handling** - Robust feedback and error messages

**Available Commands:**
- `help` - Show all commands
- `read <file>` - Read file contents
- `write <file> <content>` - Write to files
- `ls [directory]` - List directory contents
- `info` - Get system information
- `exit` - Quit the agent

## 🔧 MCP Server Features

The `mcp_server.py` provides:
- **Model Context Protocol** implementation
- **File System Tools** - Read/write/list operations
- **System Information** - Environment details
- **JSON Schema** validation
- **Async Processing** - Modern async patterns

**Available Tools:**
- `read_file` - Read file contents
- `write_file` - Write content to files
- `list_directory` - List directory contents
- `get_system_info` - System information

## 🧪 Testing

All scripts include comprehensive tests:

```bash
# Test everything
python test_agent.py
python test_mcp.py

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

## 🛠️ Development

### Adding New Scripts

1. Place new scripts in this directory
2. Update `run_demo.py` to include new options
3. Add batch file if needed for Windows
4. Update this documentation

### Path Handling

All scripts use relative paths to work from any directory:

```python
# Get project root
project_root = Path(__file__).parent.parent

# Import from src
sys.path.insert(0, str(project_root / "src"))
```

## 📖 Usage Examples

### Running Everything
```bash
cd scripts
python run_demo.py
```

### Testing Individual Components
```bash
# Test MCP server
python test_mcp.py

# Test agent
python test_agent.py

# Interactive agent
python demo_agent.py
```

### From Root Directory
```bash
# Run specific script
python scripts/test_mcp.py
python scripts/demo_agent.py
```

## 🔄 Integration

These scripts are designed to work with:
- **Original test1.py/test2.py** - Moonshot AI integrations
- **MCP Server** - For external tool access
- **Claude Desktop** - As MCP server
- **Other AI frameworks** - As tool providers