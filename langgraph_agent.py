"""
LangGraph Agent Implementation
Creates a sophisticated agent with tools and workflow management
"""

import os
import asyncio
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.chat_models.moonshot import MoonshotChat
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AgentState(TypedDict):
    """State structure for the LangGraph agent"""
    messages: List[Any]
    tools: List[str]
    current_step: str
    context: Dict[str, Any]

class LangGraphAgent:
    def __init__(self):
        self.llm = self._setup_llm()
        self.tools = self._setup_tools()
        self.graph = self._create_graph()
    
    def _setup_llm(self):
        """Setup the language model"""
        api_key = os.getenv("MOONSHOT_API_KEY")
        if not api_key:
            raise ValueError("MOONSHOT_API_KEY environment variable is required")
        
        return MoonshotChat(
            model="kimi-latest",
            temperature=0.7,
            max_tokens=1000,
            api_key=api_key
        )
    
    def _setup_tools(self):
        """Setup available tools for the agent"""
        
        @tool
        def file_reader(file_path: str) -> str:
            """Read contents of a file"""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file: {str(e)}"
        
        @tool
        def file_writer(file_path: str, content: str) -> str:
            """Write content to a file"""
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Successfully wrote to {file_path}"
            except Exception as e:
                return f"Error writing file: {str(e)}"
        
        @tool
        def list_directory(directory_path: str = ".") -> Dict[str, List[str]]:
            """List contents of a directory"""
            try:
                items = os.listdir(directory_path)
                files = [item for item in items if os.path.isfile(os.path.join(directory_path, item))]
                dirs = [item for item in items if os.path.isdir(os.path.join(directory_path, item))]
                return {"files": files, "directories": dirs}
            except Exception as e:
                return {"error": str(e)}
        
        @tool
        def calculator(expression: str) -> str:
            """Evaluate a mathematical expression"""
            try:
                # Basic safety check
                allowed_chars = set('0123456789+-*/.() ')
                if not all(c in allowed_chars for c in expression):
                    return "Error: Invalid characters in expression"
                
                result = eval(expression)
                return str(result)
            except Exception as e:
                return f"Error calculating: {str(e)}"
        
        @tool
        def web_search(query: str) -> str:
            """Perform a web search (mock implementation)"""
            # Mock search results
            return f"Search results for '{query}':\n1. Example result 1\n2. Example result 2\n3. Example result 3"
        
        return [file_reader, file_writer, list_directory, calculator, web_search]
    
    def _create_graph(self):
        """Create the LangGraph workflow"""
        # Create the workflow
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("tools", ToolNode(self.tools))
        
        # Add edges
        workflow.add_edge("agent", "tools")
        workflow.add_edge("tools", END)
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add memory
        memory = MemorySaver()
        
        return workflow.compile(checkpointer=memory)
    
    def _agent_node(self, state: AgentState):
        """The agent node that processes messages and decides on tool usage"""
        messages = state["messages"]
        
        # Add system message if none exists
        if not messages or not any(isinstance(m, SystemMessage) for m in messages):
            system_msg = SystemMessage(
                content="""You are a helpful AI assistant with access to various tools. 
                Use the appropriate tools when needed to help users with their tasks.
                Always provide clear and concise responses."""
            )
            messages = [system_msg] + messages
        
        # Get LLM with tools
        llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Process the messages
        response = llm_with_tools.invoke(messages)
        
        # Update state
        state["messages"] = messages + [response]
        state["current_step"] = "agent_processed"
        
        return state
    
    async def run(self, user_input: str, thread_id: str = "default"):
        """Run the agent with user input"""
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "tools": [],
            "current_step": "initial",
            "context": {}
        }
        
        config = {"configurable": {"thread_id": thread_id}}
        
        result = self.graph.invoke(initial_state, config)
        
        # Get the last message
        last_message = result["messages"][-1]
        
        if isinstance(last_message, AIMessage):
            return last_message.content
        else:
            return str(last_message)
    
    def stream(self, user_input: str, thread_id: str = "default"):
        """Stream the agent's response"""
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "tools": [],
            "current_step": "initial",
            "context": {}
        }
        
        config = {"configurable": {"thread_id": thread_id}}
        
        for chunk in self.graph.stream(initial_state, config):
            if "agent" in chunk:
                yield chunk["agent"]
            elif "tools" in chunk:
                yield chunk["tools"]

# Example usage
if __name__ == "__main__":
    async def main():
        agent = LangGraphAgent()
        
        # Test the agent
        responses = [
            "Hello! Can you help me create a new Python file?",
            "List the files in the current directory",
            "Calculate 15 * 23 + 7",
            "Search for Python programming tutorials"
        ]
        
        for query in responses:
            print(f"\nUser: {query}")
            result = await agent.run(query)
            print(f"Agent: {result}")
    
    asyncio.run(main())