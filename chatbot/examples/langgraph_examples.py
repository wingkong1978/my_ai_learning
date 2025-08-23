"""
LangGraph usage examples for the demo chatbot
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from chatbot.api.langgraph.langgraph_client import LangGraphChatClient
from chatbot.api.langgraph.langgraph_workflows import ChatWorkflow, ToolWorkflow, AdvancedWorkflow


class LangGraphExamples:
    """Collection of LangGraph usage examples"""
    
    def __init__(self):
        self.api_key = os.getenv("MOONSHOT_API_KEY")
        if not self.api_key:
            print("❌ Please set MOONSHOT_API_KEY in your .env file")
            return
    
    async def basic_chat_example(self):
        """Basic chat without tools"""
        print("\n🎯 Basic Chat Example")
        print("=" * 50)
        
        client = LangGraphChatClient(api_key=self.api_key)
        
        questions = [
            "What is LangGraph?",
            "Explain the benefits of using LangGraph for AI applications",
            "How does LangGraph differ from regular chat APIs?"
        ]
        
        for question in questions:
            print(f"\n❓ Question: {question}")
            response = await client.chat(question)
            print(f"💡 Answer: {response}")
    
    async def tool_usage_example(self):
        """Example using tools for file operations"""
        print("\n🛠️ Tool Usage Example")
        print("=" * 50)
        
        workflow = ToolWorkflow(api_key=self.api_key)
        
        commands = [
            "List all files in the current directory",
            "Create a test file called 'langgraph_demo.txt' with content 'Hello from LangGraph!'",
            "Read the content of the langgraph_demo.txt file",
            "Calculate 15 * 23 + 7",
            "Get system information"
        ]
        
        for command in commands:
            print(f"\n📝 Command: {command}")
            response = await workflow.run(command)
            print(f"✅ Result: {response}")
    
    async def multi_client_example(self):
        """Example using multiple AI clients"""
        print("\n🔄 Multi-Client Example")
        print("=" * 50)
        
        workflow = AdvancedWorkflow(api_key=self.api_key)
        
        queries = [
            "Compare responses from LangChain and OpenAI clients for: What is Python?",
            "Use LangChain client to explain async programming",
            "Use OpenAI client to explain Python decorators"
        ]
        
        for query in queries:
            print(f"\n🤖 Query: {query}")
            response = await workflow.run(query)
            print(f"📊 Response: {response}")
    
    async def conversation_memory_example(self):
        """Example showing conversation memory"""
        print("\n🧠 Conversation Memory Example")
        print("=" * 50)
        
        client = LangGraphChatClient(api_key=self.api_key)
        thread_id = "memory_demo"
        
        conversation = [
            "My name is Alice and I love programming",
            "What is my name?",
            "What do I love?",
            "Can you remember this conversation?"
        ]
        
        for message in conversation:
            print(f"\n👤 You: {message}")
            response = await client.chat(message, thread_id=thread_id)
            print(f"🤖 Bot: {response}")
    
    async def streaming_example(self):
        """Example of streaming responses"""
        print("\n🌊 Streaming Example")
        print("=" * 50)
        
        client = LangGraphChatClient(api_key=self.api_key)
        
        question = "Tell me a short story about AI and humans working together"
        print(f"\n❓ Question: {question}")
        print("🤖 Response: ", end="")
        
        try:
            async for chunk in client.stream_chat(question):
                if isinstance(chunk, dict) and "messages" in chunk:
                    last_message = chunk["messages"][-1]
                    if hasattr(last_message, 'content'):
                        print(last_message.content, end="")
                else:
                    print(chunk, end="")
        except Exception as e:
            print(f"Error: {e}")
    
    async def workflow_comparison_example(self):
        """Compare different workflow types"""
        print("\n⚖️ Workflow Comparison")
        print("=" * 50)
        
        chat_workflow = ChatWorkflow(api_key=self.api_key)
        tool_workflow = ToolWorkflow(api_key=self.api_key)
        
        query = "What is the capital of France?"
        
        print(f"\n📝 Query: {query}")
        
        # Chat workflow
        print("\n💬 Chat Workflow:")
        messages = [{"role": "user", "content": query}]
        response = await chat_workflow.run(messages)
        print(f"Response: {response}")
        
        # Tool workflow
        print("\n🛠️ Tool Workflow:")
        response = await tool_workflow.run(query)
        print(f"Response: {response}")
    
    async def run_all_examples(self):
        """Run all examples"""
        print("🚀 Starting LangGraph Examples")
        print("=" * 60)
        
        try:
            await self.basic_chat_example()
            await self.tool_usage_example()
            await self.multi_client_example()
            await self.conversation_memory_example()
            await self.streaming_example()
            await self.workflow_comparison_example()
            
            print("\n🎉 All examples completed successfully!")
            
        except Exception as e:
            print(f"❌ Error running examples: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """Main function to run examples"""
    examples = LangGraphExamples()
    await examples.run_all_examples()


if __name__ == "__main__":
    asyncio.run(main())