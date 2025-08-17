# MCP Server Demo

This is a working demo of the Model Context Protocol (MCP) server that provides file system and system information tools to AI assistants.

## Quick Start

### 1. Run the MCP Server
```bash
# Run the simple MCP server
python mcp_server_simple.py

# Or use the batch file (Windows)
run_mcp.bat
```

### 2. Test the Server
```bash
# Test server functionality
python mcp_test.py
```

## Available Tools

The MCP server provides the following tools:

### 1. `read_file`
Read contents of a file
- **Parameters:**
  - `file_path` (required): Path to the file to read
  - `encoding` (optional): File encoding (default: utf-8)

### 2. `write_file`
Write content to a file
- **Parameters:**
  - `file_path` (required): Path to the file to write
  - `content` (required): Content to write
  - `encoding` (optional): File encoding (default: utf-8)

### 3. `list_directory`
List contents of a directory
- **Parameters:**
  - `directory_path` (optional): Directory path to list (default: ".")

### 4. `get_system_info`
Get basic system information
- **Parameters:** None

## Usage with Claude Desktop

To use this MCP server with Claude Desktop, add the following to your Claude Desktop configuration:

### Windows
```json
{
  "mcpServers": {
    "demo-chatbot-mcp": {
      "command": "python",
      "args": ["C:\\path\\to\\mcp_server_simple.py"]
    }
  }
}
```

### macOS/Linux
```json
{
  "mcpServers": {
    "demo-chatbot-mcp": {
      "command": "python3",
      "args": ["/path/to/mcp_server_simple.py"]
    }
  }
}
```

## Dependencies

All required dependencies are listed in `requirements.txt`:
- `mcp>=1.0.0`
- `pydantic>=2.0.0`

## Files Structure

- `mcp_server_simple.py`: Main MCP server implementation
- `mcp_test.py`: Test script for MCP functionality
- `run_mcp.bat`: Windows batch file to start the server
- `src/demo_chatbot/servers/mcp_server.py`: Alternative MCP server implementation

## Testing

Run the test script to verify all tools are working:
```bash
python mcp_test.py
```

This will test:
- File read/write operations
- Directory listing
- System information retrieval

## Development

The server uses the modern MCP Python SDK with:
- Async/await pattern
- Type hints
- Proper error handling
- JSON Schema validation