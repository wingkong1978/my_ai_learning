#!/usr/bin/env python3
"""
Simple interactive demo for demo-chatbot project.
"""
import os
import sys

def main():
    """Simple interactive demo."""
    print("Demo Chatbot - Simple Interactive Mode")
    print("=" * 40)
    
    # Add current directory to Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Import configuration
    from chatbot.config.settings import Config
    
    try:
        Config.validate()
        print("Configuration loaded successfully")
    except ValueError as e:
        print(f"Configuration error: {e}")
        return 1
    
    # Import chatbot modules
    from chatbot.api.langchain.moonshot_langchain import MoonshotLangChainClient
    
    client = MoonshotLangChainClient()
    print("Ready for chat! Type 'quit' to exit")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
            
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ]
            
            response = client.chat_completion(messages)
            print(f"Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    return 0

if __name__ == "__main__":
    main()