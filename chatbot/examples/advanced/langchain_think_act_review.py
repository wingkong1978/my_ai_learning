#!/usr/bin/env python3
"""
LangChain Think-Act-Review Demo
问答-思考-执行-回顾 演示程序

实现一个简单的AI助手，能够：
1. 问答 (Question-Answering) - 理解用户问题
2. 思考 (Thinking) - 分析问题并制定计划
3. 执行 (Action) - 执行具体的操作
4. 回顾 (Review) - 检查执行结果并反思
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Set
from pathlib import Path

# LangChain imports
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
    from langchain_core.runnables import RunnableSequence
    from langchain.memory import ConversationBufferMemory
    from langchain.schema import Document
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import TextLoader
except ImportError as e:
    print(f"缺少依赖包: {e}")
    print("请安装: pip install langchain langchain-openai langchain-community")
    exit(1)

# 配置环境
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-key-here")

class TemplateValidator:
    """模板变量验证器"""
    @staticmethod
    def validate_variables(template_vars: Set[str], input_vars: Dict[str, Any]) -> bool:
        """验证输入变量是否满足模板要求"""
        required_vars = set(template_vars)
        provided_vars = set(input_vars.keys())
        return required_vars.issubset(provided_vars)

    @staticmethod
    def get_missing_vars(template_vars: Set[str], input_vars: Dict[str, Any]) -> Set[str]:
        """获取缺失的变量列表"""
        required_vars = set(template_vars)
        provided_vars = set(input_vars.keys())
        return required_vars - provided_vars

class ThinkActReviewAgent:
    """问答-思考-执行-回顾 AI代理"""
    
    def __init__(self):
        self.name = "思考执行代理"
        self.llm = ChatOpenAI(
            model="qwen3-coder-plus",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # 内存系统
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # 定义提示模板
        self.setup_prompts()
        
        # 执行历史
        self.execution_history = []
        
        self.validator = TemplateValidator()
    
    def validate_prompt_inputs(self, prompt: PromptTemplate, inputs: Dict[str, Any]) -> None:
        """验证提示模板输入"""
        if not self.validator.validate_variables(set(prompt.input_variables), inputs):
            missing_vars = self.validator.get_missing_vars(set(prompt.input_variables), inputs)
            raise ValueError(f"模板缺少必需变量: {missing_vars}")
    
    def setup_prompts(self):
        """设置各种提示模板"""
        
        # 问答模板
        self.qa_prompt = PromptTemplate(
            input_variables=["question", "context"],
            template="""你是一个智能助手。请回答用户的问题。
            
用户问题: {question}
上下文信息: {context}

请提供清晰、准确的回答。""",
            validate_template=True  # 启用模板验证
        )
        
        # 思考模板 - 修复变量定义
        self.thinking_prompt = PromptTemplate(
            input_variables=["question", "context"],  # 移除了错误的 "analysis" 变量
            template="""你需要分析问题并制定执行计划。
            
用户问题: {question}
当前上下文: {context}

请分析这个问题，并制定一个详细的执行计划。输出格式：
{{"analysis": "问题分析", "plan": ["步骤1", "步骤2", "步骤3"], "expected_outcome": "预期结果", "tools_needed": ["需要的工具"]}}"""  # 使用双大括号转义
        )
        
        # 修改执行模板，统一变量名称
        self.action_prompt = PromptTemplate(
            input_variables=["plan", "current_step", "previous_results"],
            template="""根据计划执行当前步骤。
            
完整计划: {plan}
当前步骤: {current_step}
先前结果: {previous_results}

请执行当前步骤并提供结果。
输出格式：{{"step": "{current_step}", "action": "执行的操作", "result": "执行结果", "status": "success|error", "next_action": "下一步建议"}}"""  # 修复：使用双大括号，预填充current_step
        )
        
        # 回顾模板 - 修复JSON格式和变量定义
        self.review_prompt = PromptTemplate(
            input_variables=["question", "plan", "actions", "final_result"],
            template="""请回顾整个执行过程并提供反思。
        
原始问题: {question}
执行计划: {plan}
执行过程: {actions}
最终结果: {final_result}

请提供：
{{"effectiveness": "效果评估", "successes": ["成功之处"], "improvements": ["改进建议"], "next_time_suggestions": ["下次建议"]}}"""  # 使用双大括号转义
        )
    
    async def question_answer(self, question: str) -> Dict[str, Any]:
        """问答阶段：理解用户问题"""
        context = self.memory.load_memory_variables({})["history"]
        inputs = {"question": question, "context": context}
        
        try:
            self.validate_prompt_inputs(self.qa_prompt, inputs)
            qa_chain = self.qa_prompt | self.llm | StrOutputParser()
            answer = await qa_chain.ainvoke(inputs)
        except ValueError as e:
            print(f"[ERROR] 变量验证失败: {e}")
            return {
                "type": "qa",
                "question": question,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "type": "qa",
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }
    
    async def thinking_phase(self, question: str) -> Dict[str, Any]:
        """思考阶段：分析问题并制定计划"""
        context = self.memory.load_memory_variables({})["history"]
        inputs = {"question": question, "context": context}
        
        try:
            self.validate_prompt_inputs(self.thinking_prompt, inputs)
            thinking_chain = self.thinking_prompt | self.llm | JsonOutputParser()
            plan = await thinking_chain.ainvoke(inputs)
        except ValueError as e:
            print(f"[ERROR] 变量验证失败: {e}")
            return {
                "type": "thinking",
                "question": question,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "type": "thinking",
            "question": question,
            "analysis": plan["analysis"],
            "plan": plan["plan"],
            "expected_outcome": plan["expected_outcome"],
            "tools_needed": plan["tools_needed"],
            "timestamp": datetime.now().isoformat()
        }
    
    async def action_phase(self, plan: List[str], context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """执行阶段：按步骤执行计划"""
        actions = []
        previous_results = "无"
        
        for i, step in enumerate(plan, 1):
            print(f"执行步骤 {i}/{len(plan)}: {step}")
            
            # 构建输入变量
            inputs = {
                "plan": str(plan),
                "current_step": step,  # 确保step变量正确传递
                "previous_results": previous_results
            }
            
            try:
                # 添加输入验证
                self.validate_prompt_inputs(self.action_prompt, inputs)
                action_chain = self.action_prompt | self.llm | JsonOutputParser()
                result = await action_chain.ainvoke(inputs)
                
                # 验证返回结果包含所需字段
                required_fields = ["step", "action", "result", "status", "next_action"]
                if not all(field in result for field in required_fields):
                    raise ValueError(f"响应缺少必需字段，需要: {required_fields}")
                
                action = {
                    "step_number": i,
                    "step_description": step,
                    "action": result["action"],
                    "result": result["result"],
                    "status": result["status"],
                    "next_action": result["next_action"],
                    "timestamp": datetime.now().isoformat()
                }
                
                actions.append(action)
                previous_results = result["result"]
                
                # 如果执行失败，记录错误并继续
                if result["status"] == "error":
                    print(f"[WARN] Step {i} failed: {result['result']}")
                    if not context or not context.get("continue_on_error", False):
                        break
                
                await asyncio.sleep(0.5)  # 执行延迟
                
            except Exception as e:
                error_msg = f"执行步骤 {i} 时出错: {str(e)}"
                print(f"[ERROR] {error_msg}")
                action = {
                    "step_number": i,
                    "step_description": step,
                    "action": "执行失败",
                    "result": error_msg,
                    "status": "error",
                    "next_action": "检查错误并重试",
                    "timestamp": datetime.now().isoformat()
                }
                actions.append(action)
                if not context or not context.get("continue_on_error", False):
                    break
        
        return actions
    
    async def review_phase(self, question: str, plan: List[str], 
                          actions: List[Dict[str, Any]], 
                          final_result: str) -> Dict[str, Any]:
        """回顾阶段：反思整个执行过程"""
        inputs = {
            "question": question,
            "plan": str(plan),
            "actions": str(actions),
            "final_result": final_result
        }
        
        try:
            self.validate_prompt_inputs(self.review_prompt, inputs)
            review_chain = self.review_prompt | self.llm | JsonOutputParser()
            review = await review_chain.ainvoke(inputs)
        except ValueError as e:
            print(f"[ERROR] 变量验证失败: {e}")
            return {
                "type": "review",
                "question": question,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "type": "review",
            "question": question,
            "effectiveness": review["effectiveness"],
            "successes": review["successes"],
            "improvements": review["improvements"],
            "next_time_suggestions": review["next_time_suggestions"],
            "timestamp": datetime.now().isoformat()
        }
    
    async def process_request(self, question: str) -> Dict[str, Any]:
        """完整处理流程：问答-思考-执行-回顾"""
        print("=" * 60)
        print(f"开始处理: {question}")
        print("=" * 60)
        
        # 1. 问答阶段
        print("\n阶段1: 问答理解")
        qa_result = await self.question_answer(question)
        print(f"理解: {qa_result['answer'][:200]}...")
        
        # 2. 思考阶段
        print("\n阶段2: 思考规划")
        thinking_result = await self.thinking_phase(question)
        print(f"分析: {thinking_result['analysis']}")
        print(f"计划: {len(thinking_result['plan'])} 个步骤")
        
        # 3. 执行阶段
        print("\n阶段3: 执行操作")
        actions = await self.action_phase(thinking_result['plan'])
        
        final_result = actions[-1]['result'] if actions else "执行完成"
        
        # 4. 回顾阶段
        print("\n阶段4: 回顾反思")
        review_result = await self.review_phase(
            question, 
            thinking_result['plan'], 
            actions, 
            final_result
        )
        
        # 构建完整结果
        complete_result = {
            "question": question,
            "qa": qa_result,
            "thinking": thinking_result,
            "actions": actions,
            "review": review_result,
            "timestamp": datetime.now().isoformat()
        }
        
        # 保存到内存
        self.memory.save_context(
            {"input": question},
            {"output": json.dumps(complete_result, ensure_ascii=False, indent=2)}
        )
        
        # 保存到执行历史
        self.execution_history.append(complete_result)
        
        return complete_result
    
    def save_session(self, filename: str = None):
        """保存会话历史"""
        if filename is None:
            filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = Path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "session_info": {
                    "agent": self.name,
                    "timestamp": datetime.now().isoformat(),
                    "total_requests": len(self.execution_history)
                },
                "executions": self.execution_history
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 会话已保存到: {filepath}")

class DemoActions:
    """演示动作执行器"""
    
    @staticmethod
    async def simulate_file_operation(action_type: str, params: Dict[str, Any]) -> str:
        """模拟文件操作"""
        await asyncio.sleep(0.5)  # 模拟处理时间
        
        if action_type == "read_file":
            return f"成功读取文件: {params.get('filename', 'example.txt')}"
        elif action_type == "write_file":
            return f"成功写入文件: {params.get('filename', 'output.txt')}"
        elif action_type == "search_info":
            return f"搜索到相关信息: {params.get('query', 'Python')[:50]}..."
        elif action_type == "calculate":
            return f"计算结果: {params.get('expression', '2+2')} = 4"
        else:
            return f"完成操作: {action_type}"

async def main():
    """主函数 - 演示程序"""
    print("🚀 LangChain 问答-思考-执行-回顾 演示程序")
    print("=" * 50)
    
    # 检查 API 密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  请设置 OPENAI_API_KEY 环境变量")
        print("   例如: export OPENAI_API_KEY='your-key-here'")
        return
    
    agent = ThinkActReviewAgent()
    
    # 演示问题
    demo_questions = [
        "如何学习Python编程？",
        "解释一下机器学习的基本概念",
        "设计一个简单的Web应用架构"
    ]
    
    while True:
        print("\n" + "="*50)
        print("🎯 请选择操作:")
        print("1. 运行演示问题")
        print("2. 输入自定义问题")
        print("3. 查看历史")
        print("4. 保存会话")
        print("5. 退出")
        
        choice = input("\n选择 (1-5): ").strip()
        
        if choice == "1":
            # 运行演示问题
            for question in demo_questions:
                result = await agent.process_request(question)
                print(f"\n✅ 完成: {question}")
                
        elif choice == "2":
            # 自定义问题
            question = input("\n🤔 请输入您的问题: ").strip()
            if question:
                result = await agent.process_request(question)
                
        elif choice == "3":
            # 查看历史
            if agent.execution_history:
                print(f"\n📊 执行历史 ({len(agent.execution_history)} 条):")
                for i, exec in enumerate(agent.execution_history, 1):
                    print(f"{i}. {exec['question'][:50]}...")
            else:
                print("暂无历史记录")
                
        elif choice == "4":
            # 保存会话
            agent.save_session()
            
        elif choice == "5":
            print("👋 再见!")
            break
            
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    asyncio.run(main())