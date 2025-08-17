# LangChain 问答-思考-执行-回顾 演示程序

一个基于LangChain的智能AI代理，实现了完整的"问答-思考-执行-回顾"工作流程。

## 🎯 功能特色

### 四阶段工作流
- **问答 (Question-Answering)** - 理解用户问题
- **思考 (Thinking)** - 分析问题并制定计划  
- **执行 (Action)** - 按步骤执行操作
- **回顾 (Review)** - 检查执行结果并反思

### 核心特性
- ✅ 智能问题分析
- ✅ 动态执行计划生成
- ✅ 步骤化操作执行
- ✅ 结果评估与反思
- ✅ 会话记忆与保存
- ✅ 跨平台支持

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r langchain_requirements.txt
```

### 2. 设置API密钥
```bash
# Linux/macOS
export OPENAI_API_KEY="your-openai-key-here"

# Windows
set OPENAI_API_KEY=your-openai-key-here
```

### 3. 运行演示
```bash
python langchain_think_act_review.py
```

## 📋 使用示例

### 交互模式
```
🚀 LangChain 问答-思考-执行-回顾 演示程序
==================================================

🎯 请选择操作:
1. 运行演示问题
2. 输入自定义问题
3. 查看历史
4. 保存会话
5. 退出

选择 (1-5): 1

运行演示问题...
```

### 示例输出
```
============================================================
🤖 开始处理: 如何学习Python编程？
============================================================

📋 阶段1: 问答理解
💬 理解: Python是一种易学易用的编程语言...

🧠 阶段2: 思考规划
📊 分析: 这是一个关于学习路径的问题...
📝 计划: 4 个步骤

⚡ 阶段3: 执行操作
执行步骤 1/4: 分析学习者背景...
执行步骤 2/4: 制定学习计划...

🔍 阶段4: 回顾反思
📊 效果评估: 成功提供了完整的学习路径...
```

## 🔧 核心功能

### 1. 问答阶段
- 理解用户意图
- 提供基础回答
- 建立对话上下文

### 2. 思考阶段
- 深度分析问题
- 生成执行计划
- 确定所需工具

### 3. 执行阶段
- 按步骤执行
- 实时反馈进度
- 错误处理机制

### 4. 回顾阶段
- 评估执行效果
- 总结经验教训
- 提供改进建议

## 🎮 使用模式

### 模式1：演示模式
运行预设的演示问题，快速了解功能。

### 模式2：交互模式
输入自定义问题，体验完整工作流。

### 模式3：会话模式
- 保存会话历史
- 查看执行记录
- 持续对话

## 📊 输出格式

### 执行结果结构
```json
{
  "question": "用户问题",
  "qa": {
    "type": "qa",
    "question": "问题",
    "answer": "回答",
    "timestamp": "2024-01-01T12:00:00"
  },
  "thinking": {
    "type": "thinking",
    "analysis": "问题分析",
    "plan": ["步骤1", "步骤2"],
    "expected_outcome": "预期结果",
    "tools_needed": ["工具列表"]
  },
  "actions": [
    {
      "step_number": 1,
      "step_description": "步骤描述",
      "action": "执行操作",
      "result": "执行结果",
      "status": "success"
    }
  ],
  "review": {
    "effectiveness": "效果评估",
    "successes": ["成功之处"],
    "improvements": ["改进建议"]
  }
}
```

## 🛠️ 扩展功能

### 自定义动作
你可以扩展 `DemoActions` 类来添加实际的操作：

```python
class CustomActions:
    @staticmethod
    async def search_web(query: str) -> str:
        # 实际的网络搜索实现
        return f"搜索结果: {query}"
    
    @staticmethod
    async def calculate(expression: str) -> str:
        # 实际的计算实现
        return str(eval(expression))
```

### 集成工具
- **文件操作** - 读写系统文件
- **网络搜索** - 获取最新信息
- **数据计算** - 执行数学运算
- **API调用** - 与外部服务交互

## 📁 文件结构

```
demo_chatbot/
├── langchain_think_act_review.py  # 主程序
├── langchain_requirements.txt     # 依赖列表
├── session_*.json                # 会话保存文件
├── LANGCHAIN_DEMO_README.md      # 本文档
└── scripts/                      # 其他演示程序
```

## 🎨 高级用法

### 自定义提示模板
```python
# 修改提示模板
agent.qa_prompt = PromptTemplate(
    input_variables=["question"],
    template="作为专家，请详细回答：{question}"
)
```

### 会话管理
```python
# 保存会话
agent.save_session("my_session.json")

# 加载会话历史
with open("my_session.json") as f:
    history = json.load(f)
```

## 🔍 故障排除

### 常见问题
1. **API密钥错误** - 检查 `OPENAI_API_KEY` 环境变量
2. **网络连接** - 确保能访问 OpenAI API
3. **依赖缺失** - 重新安装 `langchain_requirements.txt`

### 调试模式
```bash
# 设置调试环境变量
export LANGCHAIN_DEBUG=true
python langchain_think_act_review.py
```

## 🌟 示例问题

### 技术类
- "如何优化Python代码性能？"
- "解释一下机器学习中的过拟合"
- "设计一个微服务架构"

### 生活类
- "如何制定健身计划？"
- "学习一门新语言的最佳方法？"

### 商业类
- "如何启动一个创业项目？"
- "制定市场营销策略"

## 🤝 贡献指南

欢迎提交改进建议：
1. 添加新的动作处理器
2. 优化提示模板
3. 增强错误处理
4. 添加新功能

## 📄 许可证
MIT License - 自由使用、修改和分发