#!/usr/bin/env python3
"""
Interactive demo for demo-chatbot project.
Provides a simple command-line interface for testing the chatbot.
"""
import os
import sys

def main():
    """Main interactive demo function."""
    print("Demo Chatbot - Interactive Mode")
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
    from chatbot.api.openai.moonshot_openai import MoonshotOpenAIClient
    
    print("\nAvailable clients:")
    print("1. LangChain (Moonshot)")
    print("2. OpenAI Compatible (Moonshot)")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nSelect client (1-3): ").strip()
            
            if choice == '3' or choice.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            elif choice == '1':
                client = MoonshotLangChainClient()
                client_name = "LangChain"
            elif choice == '2':
                client = MoonshotOpenAIClient()
                client_name = "OpenAI"
            else:
                print("Invalid choice. Please select 1-3.")
                continue
            
            print(f"\nUsing {client_name} client")
            print("Type 'quit' or 'exit' to return to main menu")
            print("Type 'switch' to change client")
            print("-" * 40)
            
            while True:
                try:
                    user_input = input(f"\n[{client_name}] You: ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        print("Returning to main menu...")
                        break
                    elif user_input.lower() == 'switch':
                        print("Returning to client selection...")
                        break
                    elif not user_input:
                        continue
                    
                    messages = [
                        {"role": "system", "content": "You are a helpful AI assistant."},
                        {"role": "user", "content": user_input}
                    ]
                    
                    print(f"[{client_name}] Thinking...")
                    response = client.chat_completion(messages)
                    print(f"[{client_name}] Assistant: {response}")
                    
                except KeyboardInterrupt:
                    print("\n\nSession interrupted by user")
                    return 0
                except Exception as e:
                    print(f"Error: {e}")
                    
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            return 0
        except Exception as e:
            print(f"Error: {e}")
            
    return 0

if __name__ == "__main__":
    exit(main())