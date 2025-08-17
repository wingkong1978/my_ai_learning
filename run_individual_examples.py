#!/usr/bin/env python3
"""
Individual example runner for demo-chatbot.
"""
import os
import sys
import subprocess

def run_example(example_name):
    """Run a specific example."""
    examples = {
        'langchain_basic': 'chatbot/examples/basic/langchain_basic.py',
        'openai_basic': 'chatbot/examples/basic/openai_basic.py',
        'langchain_demo_simple': 'chatbot/examples/advanced/langchain_demo_simple.py',
        'langchain_demo_fixed': 'chatbot/examples/advanced/langchain_demo_fixed.py',
    }
    
    if example_name not in examples:
        print(f"Available examples: {', '.join(examples.keys())}")
        return 1
    
    print(f"Running {example_name}...")
    result = subprocess.run([sys.executable, examples[example_name]], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"{example_name} completed successfully")
        return 0
    else:
        print(f"{example_name} failed: {result.stderr}")
        return 1

def main():
    """Main function."""
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
    
    # Run all basic examples
    examples = [
        'langchain_basic',
        'openai_basic'
    ]
    
    success_count = 0
    for example in examples:
        if run_example(example) == 0:
            success_count += 1
        print()
    
    print(f"Completed {success_count}/{len(examples)} examples successfully")
    return 0 if success_count == len(examples) else 1

if __name__ == "__main__":
    exit(main())