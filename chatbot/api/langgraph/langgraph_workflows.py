"""
LangGraph workflow implementations for different use cases
"""

import os
from typing import List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_community.chat_models.moonshot import MoonshotChat

from ..langchain.moonshot_langchain import MoonshotLangChainClient
from ..openai.moonshot_openai import MoonshotOpenAIClient


class ChatWorkflow:
    """Simple chat workflow without tools"""
    
    def __init__(self, api_key: str = None, model: str = "kimi-latest"):
        self.api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        if not self.api_key:
            raise ValueError("MOONSHOT_API_KEY is required")
        
        self.model = MoonshotChat(
            model=model,
            temperature=0.7,
            max_tokens=1000,
            api_key=self.api_key
        )
        self.graph = self._create_graph()
    
    def _create_graph(self):
        """Create simple chat graph"""
        def chat_node(state):
            messages = state.get("messages", [])
            if not messages:
                return state
            
            response = self.model.invoke(messages)
            return {"messages": messages + [response]}
        
        workflow = StateGraph(dict)
        workflow.add_node("chat", chat_node)
        workflow.set_entry_point("chat")
        workflow.add_edge("chat", END)
        
        return workflow.compile()
    
    async def run(self, messages: List[Dict[str, str]], thread_id: str = "default") -> str:
        """Run chat workflow"""
        formatted_messages = []
        for msg in messages:
            if msg["role"] == "system":
                formatted_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
        
        state = {"messages": formatted_messages}
        result = self.graph.invoke(state)
        
        last_message = result["messages"][-1]
        return last_message.content


class ToolWorkflow:
    """Workflow with tools for file operations, calculations, etc."""
    
    def __init__(self, api_key: str = None, model: str = "kimi-latest"):
        self.api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        if not self.api_key:
            raise ValueError("MOONSHOT_API_KEY is required")
        
        self.model = MoonshotChat(
            model=model,
            temperature=0.7,
            max_tokens=1000,
            api_key=self.api_key
        )
        self.tools = self._setup_tools()
        self.graph = self._create_graph()
    
    def _setup_tools(self):
        """Setup tools for file operations and calculations"""
        
        @tool
        def read_file(file_path: str) -> str:
            """Read content from a file"""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file: {str(e)}"
        
        @tool
        def write_file(file_path: str, content: str) -> str:
            """Write content to a file"""
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Successfully wrote to {file_path}"
            except Exception as e:
                return f"Error writing file: {str(e)}"
        
        @tool
        def list_files(directory: str = ".") -> Dict[str, List[str]]:
            """List files and directories"""
            try:
                items = os.listdir(directory)
                files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
                dirs = [item for item in items if os.path.isdir(os.path.join(directory, item))]
                return {"files": files, "directories": dirs}
            except Exception as e:
                return {"error": str(e)}
        
        @tool
        def calculate(expression: str) -> str:
            """Evaluate mathematical expression"""
            try:
                # Simple safety check
                allowed_chars = set('0123456789+-*/.() ')
                if not all(c in allowed_chars for c in expression):
                    return "Error: Invalid characters in expression"
                
                result = eval(expression)
                return str(result)
            except Exception as e:
                return f"Error calculating: {str(e)}"
        
        @tool
        def get_system_info() -> Dict[str, str]:
            """Get system information"""
            import platform
            return {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "working_directory": os.getcwd()
            }
        
        return [read_file, write_file, list_files, calculate, get_system_info]
    
    def _create_graph(self):
        """Create graph with tools"""
        workflow = StateGraph(dict)
        
        def agent_node(state):
            messages = state.get("messages", [])
            if not messages:
                return state
            
            # Add system message
            system_msg = SystemMessage(
                content="You are a helpful AI assistant with access to various tools. "
                       "Use tools when appropriate to help users with their tasks."
            )
            
            if not any(isinstance(m, SystemMessage) for m in messages):
                messages = [system_msg] + messages
            
            llm_with_tools = self.model.bind_tools(self.tools)
            response = llm_with_tools.invoke(messages)
            return {"messages": messages + [response]}
        
        workflow.add_node("agent", agent_node)
        workflow.add_node("tools", ToolNode(self.tools))
        
        def should_use_tools(state):
            last_message = state["messages"][-1]
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                return "tools"
            return END
        
        workflow.add_edge("agent", "tools")
        workflow.add_edge("tools", "agent")
        workflow.set_entry_point("agent")
        
        # Add memory
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    
    async def run(self, user_input: str, thread_id: str = "default") -> str:
        """Run tool workflow"""
        messages = [HumanMessage(content=user_input)]
        state = {"messages": messages}
        
        config = {"configurable": {"thread_id": thread_id}}
        result = self.graph.invoke(state, config)
        
        last_message = result["messages"][-1]
        return last_message.content


class AdvancedWorkflow:
    """Advanced workflow combining multiple AI clients"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        if not self.api_key:
            raise ValueError("MOONSHOT_API_KEY is required")
        
        self.langchain_client = MoonshotLangChainClient(api_key=api_key)
        self.openai_client = MoonshotOpenAIClient(api_key=api_key)
        self.model = MoonshotChat(
            model="kimi-latest",
            temperature=0.7,
            max_tokens=1000,
            api_key=self.api_key
        )
        self.tools = self._setup_advanced_tools()
        self.graph = self._create_advanced_graph()
    
    def _setup_advanced_tools(self):
        """Setup advanced tools combining multiple clients"""
        
        @tool
        def compare_responses(query: str) -> Dict[str, str]:
            """Compare responses from LangChain and OpenAI clients"""
            messages = [{"role": "user", "content": query}]
            
            langchain_response = self.langchain_client.chat_completion(messages)
            openai_response = self.openai_client.chat_completion(messages)
            
            return {
                "langchain": langchain_response,
                "openai": openai_response,
                "query": query
            }
        
        @tool
        def switch_client_strategy(strategy: str) -> str:
            """Switch between different client strategies"""
            strategies = {
                "langchain": "Using LangChain client",
                "openai": "Using OpenAI client", 
                "hybrid": "Using hybrid approach"
            }
            return strategies.get(strategy, "Unknown strategy")
        
        return [compare_responses, switch_client_strategy]
    
    def _create_advanced_graph(self):
        """Create advanced workflow graph"""
        workflow = StateGraph(dict)
        
        def router_node(state):
            """Route to appropriate client based on query"""
            messages = state.get("messages", [])
            if not messages:
                return state
            
            last_message = messages[-1]
            if isinstance(last_message, HumanMessage):
                content = last_message.content.lower()
                
                if "compare" in content or "both" in content:
                    return {"route": "compare"}
                elif "langchain" in content:
                    return {"route": "langchain"}
                elif "openai" in content:
                    return {"route": "openai"}
                else:
                    return {"route": "default"}
            
            return state
        
        def process_node(state):
            """Process based on route"""
            route = state.get("route", "default")
            messages = state.get("messages", [])
            
            if route == "compare":
                # Use comparison tool
                tool = self._setup_advanced_tools()[0]  # compare_responses
                last_message = messages[-1]
                if isinstance(last_message, HumanMessage):
                    result = tool.invoke({"query": last_message.content})
                    response = AIMessage(content=str(result))
            else:
                # Use default chat
                response = self.model.invoke(messages)
            
            return {"messages": messages + [response]}
        
        workflow.add_node("router", router_node)
        workflow.add_node("process", process_node)
        workflow.add_edge("router", "process")
        workflow.add_edge("process", END)
        workflow.set_entry_point("router")
        
        return workflow.compile()
    
    async def run(self, user_input: str, thread_id: str = "default") -> str:
        """Run advanced workflow"""
        messages = [HumanMessage(content=user_input)]
        state = {"messages": messages}
        
        result = self.graph.invoke(state)
        last_message = result["messages"][-1]
        return last_message.content


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Test basic chat workflow
        chat_workflow = ChatWorkflow()
        response = await chat_workflow.run([
            {"role": "user", "content": "Hello! What can you do?"}
        ])
        print(f"Chat Response: {response}")
        
        # Test tool workflow
        tool_workflow = ToolWorkflow()
        response = await tool_workflow.run("List files in the current directory")
        print(f"Tool Response: {response}")
    
    asyncio.run(main())