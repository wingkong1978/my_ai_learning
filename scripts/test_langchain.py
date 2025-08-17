#!/usr/bin/env python3
"""
测试 LangChain Think-Act-Review Demo
快速测试 LangChain 功能
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_think_act_review import ThinkActReviewAgent

async def test_langchain_demo():
    """测试 LangChain 演示功能"""
    print("测试 LangChain Think-Act-Review Demo")
    print("=" * 50)
    
    # 检查 API 密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY 环境变量")
        print("例如: export OPENAI_API_KEY='your-key-here'")
        return False
    
    try:
        agent = ThinkActReviewAgent()
        
        # 测试简单问题
        test_question = "Python是什么？"
        
        print(f"测试问题: {test_question}")
        print("正在处理...")
        
        result = await agent.process_request(test_question)
        
        print("\n测试完成！")
        print(f"问题: {result['question']}")
        print(f"回答: {result['qa']['answer'][:100]}...")
        print(f"分析: {result['thinking']['analysis'][:100]}...")
        print(f"步骤数: {len(result['thinking']['plan'])}")
        print(f"执行结果: {result['actions'][-1]['result'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_langchain_demo())
    if success:
        print("\nLangChain 演示测试通过！")
        print("现在可以运行: python langchain_think_act_review.py")
    else:
        print("\n请检查环境配置后重试")