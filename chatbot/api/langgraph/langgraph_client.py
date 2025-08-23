"""
LangGraph client integration for the demo chatbot.
Provides unified interface for LangGraph workflows.
"""

import os
from typing import List, Dict, Any, Optional, AsyncGenerator
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_community.chat_models.moonshot import MoonshotChat

from ..langchain.moonshot_langchain import MoonshotLangChainClient
from ..openai.moonshot_openai import MoonshotOpenAIClient


class ChatState(dict):
    """State structure for chat workflow"""
    def __init__(self, **kwargs):
        super().__init__()
        self["messages"] = kwargs.get("messages", [])
        self["context"] = kwargs.get("context", {})
        self["tools"] = kwargs.get("tools", [])
        self["current_step"] = kwargs.get("current_step", "start")


class LangGraphChatClient:
    """
    Unified LangGraph client that integrates both LangChain and OpenAI clients
    """
    
    def __init__(self, api_key: str = None, model: str = "kimi-latest"):
        """
        Initialize LangGraph chat client
        
        Args:
            api_key: Moonshot API key. If None, uses MOONSHOT_API_KEY env var.
            model: Model name to use for chat completions.
        """
        self.api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        if not self.api_key:
            raise ValueError("MOONSHOT_API_KEY is required")
        
        self.model = model
        self.langchain_client = MoonshotLangChainClient(api_key=api_key, model=model)
        self.openai_client = MoonshotOpenAIClient(api_key=api_key)
        self.chat_model = self._setup_chat_model()
        self.tools = self._setup_tools()
        self.graph = self._create_chat_graph()
    
    def _setup_chat_model(self):
        """Setup the Moonshot chat model"""
        return MoonshotChat(
            model=self.model,
            temperature=0.7,
            max_tokens=1000,
            api_key=self.api_key
        )
    
    def _setup_tools(self):
        """Setup available tools for the agent"""
        
        @tool
        def use_langchain(messages: List[Dict[str, str]], **kwargs) -> str:
            """Use LangChain client for chat completion"""
            return self.langchain_client.chat_completion(messages, **kwargs)
        
        @tool
        def use_openai(messages: List[Dict[str, str]], model: str = "moonshot-v1-8k", **kwargs) -> str:
            """Use OpenAI client for chat completion"""
            return self.openai_client.chat_completion(messages, model=model, **kwargs)
        
        @tool
        def switch_model(model_name: str) -> str:
            """Switch between different models"""
            self.model = model_name
            self.chat_model = self._setup_chat_model()
            return f"Switched to model: {model_name}"
        
        return [use_langchain, use_openai, switch_model]
    
    def _create_chat_graph(self):
        """Create the chat workflow graph"""
        workflow = StateGraph(ChatState)
        
        # Add nodes
        workflow.add_node("chat", self._chat_node)
        workflow.add_node("tools", ToolNode(self.tools))
        
        # Add conditional edges
        def should_use_tools(state):
            last_message = state["messages"][-1] if state["messages"] else None
            if isinstance(last_message, AIMessage) and last_message.tool_calls:
                return "tools"
            return END
        
        workflow.add_edge("chat", "tools")
        workflow.add_edge("tools", END)
        workflow.set_entry_point("chat")
        
        # Add memory for conversation context
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    
    def _chat_node(self, state: ChatState):
        """Process chat messages"""
        messages = state["messages"]
        
        # Add system message if needed
        if not messages or not any(isinstance(m, SystemMessage) for m in messages):
            system_msg = SystemMessage(
                content="""You are a helpful AI assistant with access to multiple AI clients.
                You can use LangChain or OpenAI clients based on the user's needs.
                Be helpful and provide clear, concise responses."""
            )
            messages = [system_msg] + messages
        
        # Use Moonshot chat model
        llm_with_tools = self.chat_model.bind_tools(self.tools)
        response = llm_with_tools.invoke(messages)
        
        # Update state
        state["messages"] = messages + [response]
        state["current_step"] = "chat_processed"
        
        return state
    
    async def chat(self, user_input: str, thread_id: str = "default") -> str:
        """
        Send a chat message and get response
        
        Args:
            user_input: The user's message
            thread_id: Thread ID for conversation memory
            
        Returns:
            The agent's response
        """
        initial_state = ChatState(
            messages=[HumanMessage(content=user_input)],
            current_step="start"
        )
        
        config = {"configurable": {"thread_id": thread_id}}
        result = self.graph.invoke(initial_state, config)
        
        # Get the last message
        last_message = result["messages"][-1]
        return last_message.content if isinstance(last_message, AIMessage) else str(last_message)
    
    async def stream_chat(self, user_input: str, thread_id: str = "default") -> AsyncGenerator[str, None]:
        """
        Stream chat responses
        
        Args:
            user_input: The user's message
            thread_id: Thread ID for conversation memory
            
        Yields:
            Response chunks as they are generated
        """
        initial_state = ChatState(
            messages=[HumanMessage(content=user_input)],
            current_step="start"
        )
        
        config = {"configurable": {"thread_id": thread_id}}
        
        async for chunk in self.graph.astream(initial_state, config):
            if "chat" in chunk:
                yield chunk["chat"]
            elif "tools" in chunk:
                yield chunk["tools"]
    
    def get_conversation_history(self, thread_id: str = "default") -> List[Dict[str, str]]:
        """Get conversation history for a thread"""
        # This would require implementing state retrieval
        # For now, return empty list as placeholder
        return []


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        client = LangGraphChatClient()
        
        # Test basic chat
        response = await client.chat("Hello! Can you help me?")
        print(f"Response: {response}")
        
        # Test with different models
        response = await client.chat("Use the OpenAI client to answer this question: What is Python?")
        print(f"OpenAI Response: {response}")
    
    asyncio.run(main())