"""
Demo Chatbot - A comprehensive demo of LangChain + LangGraph + MCP + Agent integration
"""

__version__ = "0.1.0"
__author__ = "Developer"
__email__ = "dev@example.com"

from .agents.langgraph_agent import LangGraphAgent
from .servers.mcp_server import MCPServer

__all__ = ["LangGraphAgent", "MCPServer"]