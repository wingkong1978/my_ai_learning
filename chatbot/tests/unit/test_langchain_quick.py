#!/usr/bin/env python3
"""
Quick test for LangChain demo
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

async def quick_test():
    """Quick test of LangChain functionality"""
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("API key not set. Using demo mode.")
        return
    
    try:
        from langchain_openai import ChatOpenAI
        
        # Test basic LLM connection
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=api_key
        )
        
        # Test prompt
        from langchain_core.prompts import PromptTemplate
        test_prompt = PromptTemplate(
            input_variables=["question"],
            template="Answer this: {question}"
        )
        
        chain = test_prompt | llm
        response = await chain.ainvoke({"question": "Hello"})
        
        print("LangChain setup successful!")
        print(f"Response: {response.content[:50]}...")
        
    except Exception as e:
        print(f"Setup test failed: {e}")

if __name__ == "__main__":
    asyncio.run(quick_test())