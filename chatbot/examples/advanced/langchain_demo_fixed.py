#!/usr/bin/env python3
"""
LangChain Think-Act-Review Demo - Fixed Version
Fixed prompt template issues and encoding problems
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

class FixedThinkActReviewAgent:
    """Fixed AI agent with think-act-review workflow"""
    
    def __init__(self):
        self.name = "Fixed Agent"
        
        # Check for API key
        api_key = os.getenv("OPENAI_API_KEY", "your-key-here")
        if api_key == "your-key-here":
            print("WARNING: Please set OPENAI_API_KEY environment variable")
            print("Example: export OPENAI_API_KEY='your-openai-key'")
            return
        
        try:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                openai_api_key=api_key
            )
            
            self.memory = ConversationBufferMemory(return_messages=True)
            self.setup_prompts()
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            exit(1)
    
    def setup_prompts(self):
        """Setup prompt templates with proper variable formatting"""
        
        self.thinking_prompt = PromptTemplate(
            input_variables=["question", "context"],
            template="""Analyze this question and create an execution plan:

Question: {question}
Context: {context}

Return JSON with these exact keys: analysis, plan, expected_outcome, tools_needed"""
        )
        
        self.action_prompt = PromptTemplate(
            input_variables=["plan", "current_step", "previous_results"],
            template="""Execute this step based on the plan:

Plan: {plan}
Current Step: {current_step}
Previous Results: {previous_results}

Return JSON with these exact keys: step, action, result, status, next_action"""
        )
        
        self.review_prompt = PromptTemplate(
            input_variables=["question", "plan", "actions", "final_result"],
            template="""Review the entire execution process:

Question: {question}
Plan: {plan}
Actions: {actions}
Final Result: {final_result}

Return JSON with these exact keys: effectiveness, successes, improvements, next_time_suggestions"""
        )
    
    async def process_question(self, question: str) -> Dict[str, Any]:
        """Process a question through think-act-review workflow"""
        
        print(f"\nProcessing: {question}")
        print("=" * 50)
        
        try:
            # 1. Thinking phase
            print("\n1. Thinking Phase")
            thinking_chain = self.thinking_prompt | self.llm | JsonOutputParser()
            thinking = await thinking_chain.ainvoke({
                "question": question,
                "context": str(self.memory.load_memory_variables({}))
            })
            
            print(f"Analysis: {thinking.get('analysis', 'No analysis provided')}")
            print(f"Plan: {len(thinking.get('plan', []))} steps")
            
            # 2. Action phase
            print("\n2. Action Phase")
            actions = []
            
            plan_steps = thinking.get('plan', ["General processing"])
            previous_results = "None"
            
            for i, step in enumerate(plan_steps, 1):
                print(f"Step {i}: {step}")
                
                action_chain = self.action_prompt | self.llm | JsonOutputParser()
                action_result = await action_chain.ainvoke({
                    "plan": str(plan_steps),
                    "current_step": step,
                    "previous_results": previous_results
                })
                
                # Ensure all required keys are present
                action_data = {
                    "step_number": i,
                    "step_description": step,
                    "action": action_result.get("action", "No action specified"),
                    "result": action_result.get("result", "No result provided"),
                    "status": action_result.get("status", "unknown"),
                    "next_action": action_result.get("next_action", "Continue")
                }
                
                actions.append(action_data)
                previous_results = action_data["result"]
                
                # Small delay to show processing
                await asyncio.sleep(0.1)
            
            # 3. Review phase
            print("\n3. Review Phase")
            review_chain = self.review_prompt | self.llm | JsonOutputParser()
            review = await review_chain.ainvoke({
                "question": question,
                "plan": str(plan_steps),
                "actions": str(actions),
                "final_result": actions[-1]["result"] if actions else "No final result"
            })
            
            result = {
                "question": question,
                "thinking": thinking,
                "actions": actions,
                "review": review,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
            
            return result
            
        except Exception as e:
            return {
                "question": question,
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.now().isoformat()
            }

async def main():
    """Main demo function"""
    print("LangChain Think-Act-Review Demo - Fixed Version")
    print("=" * 50)
    
    agent = FixedThinkActReviewAgent()
    
    # Demo questions
    demo_questions = [
        "What is Python programming?",
        "How to learn machine learning?",
        "Explain web development basics"
    ]
    
    if not hasattr(agent, 'llm'):
        print("Agent initialization failed. Please check your API key.")
        return
    
    while True:
        print("\nOptions:")
        print("1. Run demo questions")
        print("2. Enter custom question")
        print("3. Exit")
        
        try:
            choice = input("\nSelect (1-3): ").strip()
            
            if choice == "1":
                for question in demo_questions:
                    print(f"\nProcessing: {question}")
                    result = await agent.process_question(question)
                    if result.get("status") == "completed":
                        print(f"✓ Completed: {question}")
                    else:
                        print(f"✗ Failed: {result.get('error', 'Unknown error')}")
                        
            elif choice == "2":
                question = input("Enter your question: ").strip()
                if question:
                    print(f"Processing: {question}")
                    result = await agent.process_question(question)
                    if result.get("status") == "completed":
                        print(f"✓ Completed successfully")
                        # Print summary
                        print(f"Analysis: {result['thinking'].get('analysis', 'N/A')[:100]}...")
                        print(f"Plan steps: {len(result['thinking'].get('plan', []))}")
                    else:
                        print(f"✗ Failed: {result.get('error', 'Unknown error')}")
                        
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())