#!/usr/bin/env python3
"""
Simple demo for the demo-chatbot project.
This demonstrates the basic functionality without complex dependencies.
"""

import os
import sys

def main():
    """Main demo function."""
    print("Starting demo-chatbot demonstration...")
    
    # Import configuration which loads from .env
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from chatbot.config.settings import Config
    
    try:
        Config.validate()
        api_key = Config.MOONSHOT_API_KEY
        print("Configuration loaded successfully from .env file")
    except ValueError as e:
        print(f"Configuration error: {e}")
        return 1
    
    try:
        # Import our chatbot modules
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from chatbot.api.langchain.moonshot_langchain import MoonshotLangChainClient
        from chatbot.api.openai.moonshot_openai import MoonshotOpenAIClient
        
        print("Successfully imported chatbot modules")
        
        # Test LangChain client
        print("\nTesting LangChain integration...")
        langchain_client = MoonshotLangChainClient(api_key=api_key)
        response1 = langchain_client.chat_completion([
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you briefly introduce yourself and tell me what you can do?"}
        ])
        print(f"LangChain Response: {response1}")
        
        # Test OpenAI client
        print("\nTesting OpenAI-compatible integration...")
        openai_client = MoonshotOpenAIClient(api_key=api_key)
        response2 = openai_client.chat_completion([
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you briefly introduce yourself and tell me what you can do?"}
        ])
        print(f"OpenAI Response: {response2}")
        
        print("\nDemo completed successfully!")
        print("The demo-chatbot is working correctly!")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please install dependencies: pip install langchain langchain-community openai")
        return 1
    except Exception as e:
        print(f"Demo failed: {e}")
        import traceback
        print(traceback.format_exc())
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())