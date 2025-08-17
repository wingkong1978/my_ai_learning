#!/usr/bin/env python3
"""
Simple examples runner for the demo-chatbot project.
"""
import os
import sys
import subprocess

def main():
    """Run all basic examples."""
    print("Running demo-chatbot examples...")
    
    # Import configuration which loads from .env
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from chatbot.config.settings import Config
    
    try:
        Config.validate()
        print("Configuration loaded successfully")
    except ValueError as e:
        print(f"Configuration error: {e}")
        return 1
    
    examples = [
        ("LangChain Basic", "python", ["chatbot/examples/basic/langchain_basic.py"]),
        ("OpenAI Basic", "python", ["chatbot/examples/basic/openai_basic.py"]),
    ]
    
    for name, cmd, args in examples:
        print(f"\n--- Running {name} ---")
        try:
            result = subprocess.run([cmd] + args, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{name} completed successfully")
            else:
                print(f"{name} failed with return code {result.returncode}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
        except Exception as e:
            print(f"{name} failed: {e}")
    
    print("\nAll examples completed!")
    return 0

if __name__ == "__main__":
    exit(main())