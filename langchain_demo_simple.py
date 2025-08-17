#!/usr/bin/env python3
"""
LangChain Simple Think-Act-Review Demo
A simple AI agent implementing question-answering, thinking, action, and review workflow
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, List

# LangChain imports
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
    from langchain.memory import ConversationBufferMemory
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Please install: pip install langchain langchain-openai")
    exit(1)

class SimpleThinkActReviewAgent:
    """Simple AI agent with think-act-review workflow"""
    
    def __init__(self):
        self.name = "Simple Agent"
        
        # Check for API key
        api_key = os.getenv("OPENAI_API_KEY", "your-key-here")
        if api_key == "your-key-here":
            print("WARNING: Please set OPENAI_API_KEY environment variable")
            print("Example: export OPENAI_API_KEY='your-openai-key'")
        
        self.llm = ChatOpenAI(
            model="qwen3-coder-plus",
            temperature=0.7,
            openai_api_key=api_key
        )
        
        self.memory = ConversationBufferMemory(return_messages=True)
        self.setup_prompts()
    
    def setup_prompts(self):
        """Setup prompt templates"""
        
        self.thinking_prompt = PromptTemplate(
            input_variables=["question"],
            template="""Analyze this question and create an execution plan:

Question: {question}

Please provide:
1. Analysis of the question
2. Step-by-step execution plan
3. Expected outcome

Return JSON format:
{{
    "analysis": "your analysis",
    "plan": ["step1", "step2", "step3"],
    "expected_outcome": "what you expect"
}}"""
        )
        
        self.action_prompt = PromptTemplate(
            input_variables=["step", "context"],
            template="""Execute this step:
            
Step: {step}
Context: {context}

Return JSON format:
{{
    "action": "what was done",
    "result": "the result",
    "status": "success"
}}"""
        )
    
    async def process_question(self, question: str) -> Dict[str, Any]:
        """Process a question through think-act-review workflow"""
        
        print(f"\nProcessing: {question}")
        print("=" * 50)
        
        # 1. Thinking phase
        print("\nPhase 1: Thinking")
        thinking_chain = self.thinking_prompt | self.llm | JsonOutputParser()
        thinking = await thinking_chain.ainvoke({"question": question})
        
        print(f"Analysis: {thinking['analysis']}")
        print(f"Plan: {len(thinking['plan'])} steps")
        
        # 2. Action phase
        print("\nPhase 2: Action")
        actions = []
        
        for i, step in enumerate(thinking['plan'], 1):
            print(f"Step {i}: {step}")
            
            action_chain = self.action_prompt | self.llm | JsonOutputParser()
            action_result = await action_chain.ainvoke({
                "step": step,
                "context": str(actions)
            })
            
            actions.append({
                "step": i,
                "description": step,
                "action": action_result["action"],
                "result": action_result["result"],
                "status": action_result["status"]
            })
        
        # 3. Review phase
        print("\nPhase 3: Review")
        print("Completed successfully!")
        
        return {
            "question": question,
            "thinking": thinking,
            "actions": actions,
            "timestamp": datetime.now().isoformat()
        }

async def main():
    """Main demo function"""
    print("LangChain Think-Act-Review Demo")
    print("=" * 40)
    
    agent = SimpleThinkActReviewAgent()
    
    # Demo questions
    demo_questions = [
        "How to learn Python programming?",
        "What is machine learning?",
        "How to build a simple web application?"
    ]
    
    while True:
        print("\nOptions:")
        print("1. Run demo questions")
        print("2. Enter custom question")
        print("3. Exit")
        
        choice = input("\nSelect (1-3): ").strip()
        
        if choice == "1":
            for question in demo_questions:
                result = await agent.process_question(question)
                print(f"\nCompleted: {question}")
                
        elif choice == "2":
            question = input("Enter your question: ").strip()
            if question:
                result = await agent.process_question(question)
                
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())