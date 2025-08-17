# LangChain Demo 使用指南

## 快速修复了编码和提示模板问题！

### 安装和设置

1. **安装依赖**:
```bash
pip install -r langchain_requirements.txt
```

2. **设置API密钥**:
```bash
# Linux/macOS
export OPENAI_API_KEY="your-openai-key-here"

# Windows
set OPENAI_API_KEY=your-openai-key-here
```

### 运行演示

#### 选项1：简化版本（推荐）
```bash
python langchain_demo_fixed.py
```

#### 选项2：快速测试
```bash
python test_langchain_quick.py
```

#### 选项3：原始版本
```bash
python langchain_think_act_review.py
```

### 已修复的问题

✅ **提示模板变量错误** - 修复了JSON格式和变量匹配
✅ **编码问题** - 移除了Unicode字符
✅ **API密钥验证** - 更好的错误处理
✅ **依赖更新** - 添加了必要的langchain-core

### 使用示例

运行后会看到：
```
LangChain Think-Act-Review Demo - Fixed Version
==============================================

Options:
1. Run demo questions
2. Enter custom question
3. Exit

Select (1-3): 1

Processing: What is Python programming?
==================================================

1. Thinking Phase
Analysis: Python is a high-level programming language...
Plan: 3 steps

2. Action Phase
Step 1: Define Python basics
Step 2: Explain key features
Step 3: Provide learning resources

3. Review Phase
Completed successfully!
```

### 故障排除

如果遇到问题：
1. 确保OPENAI_API_KEY已设置
2. 重新安装依赖：`pip install -r langchain_requirements.txt`
3. 检查网络连接
4. 使用简化版本：`python langchain_demo_fixed.py`