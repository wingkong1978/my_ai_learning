# Demo Chatbot Web Interface

## 简介

这是一个基于Web的AI聊天机器人界面，整合了LangChain、LangGraph和MCP技术，提供智能对话、文件操作、数学计算和网络搜索等功能。

## 功能特性

### 🌐 Web界面特性
- **现代化UI设计**：响应式设计，支持桌面和移动设备
- **实时聊天**：基于REST API的实时消息传递
- **对话记忆**：支持基于线程的对话历史管理
- **错误处理**：完善的错误处理和用户友好的错误提示

### 🤖 AI功能
- **智能对话**：基于Moonshot AI的自然语言处理
- **文件操作**：读取、写入、列表文件和目录
- **数学计算**：支持复杂的数学表达式计算
- **网络搜索**：集成网络搜索功能
- **工具链**：支持多工具组合和工作流

### 🔧 技术特性
- **FastAPI**：高性能异步Web框架
- **WebSocket支持**：为未来实时功能预留
- **API文档**：自动生成的OpenAPI文档
- **会话管理**：支持多会话并发

## 快速开始

### 1. 启动Web服务器

#### 方法一：使用批处理脚本（推荐）
```bash
# 生产模式
run_web.bat

# 开发模式（支持热重载）
run_web_dev.bat
```

#### 方法二：使用CLI命令
```bash
# 激活虚拟环境
venv\Scripts\activate

# 启动Web服务器
demo-chatbot web --host 127.0.0.1 --port 8000

# 开发模式（热重载）
demo-chatbot web --host 127.0.0.1 --port 8000 --reload
```

### 2. 访问Web界面

启动成功后，在浏览器中访问：
- **主界面**：http://127.0.0.1:8000
- **API文档**：http://127.0.0.1:8000/api/docs
- **备用文档**：http://127.0.0.1:8000/api/redoc

## API接口

### REST API端点

#### 聊天接口
- `POST /api/chat` - 发送聊天消息
- `GET /api/chat/history/{thread_id}` - 获取对话历史
- `DELETE /api/chat/history/{thread_id}` - 清除对话历史
- `GET /api/chat/sessions` - 列出所有会话

#### 系统接口
- `GET /api/health` - 健康检查
- `GET /` - 主页面（HTML界面）

#### WebSocket
- `WS /ws/{thread_id}` - WebSocket连接（预留）

### 请求示例

```bash
# 发送聊天消息
curl -X POST "http://127.0.0.1:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "你好，请介绍一下你自己", "thread_id": "test_session"}'

# 健康检查
curl "http://127.0.0.1:8000/api/health"

# 获取对话历史
curl "http://127.0.0.1:8000/api/chat/history/test_session"
```

## 使用指南

### 基本聊天
1. 在消息输入框中输入您的问题
2. 点击"发送"按钮或按Enter键
3. AI会处理您的请求并返回响应

### 高级功能

#### 文件操作
```
创建一个名为 'test.txt' 的文件，内容是 'Hello World'
读取 test.txt 文件的内容
列出当前目录的所有文件
```

#### 数学计算
```
计算 (25 * 4 + 10) / 2
计算圆的面积，半径为5
求解二次方程 x^2 + 2x - 8 = 0
```

#### 网络搜索
```
搜索最新的人工智能发展趋势
查找Python最佳实践
```

## 配置说明

### 环境变量
在`.env`文件中配置以下参数：

```env
# 必需配置
MOONSHOT_API_KEY=your_api_key_here

# 可选配置
DEFAULT_MODEL=kimi-latest
TEMPERATURE=0.7
MAX_TOKENS=1000
DEBUG=false

# Web服务器配置
WEB_HOST=127.0.0.1
WEB_PORT=8000
```

### 服务器配置
- **主机地址**：默认 127.0.0.1（本地访问）
- **端口**：默认 8000
- **CORS**：已启用跨域支持
- **文档**：自动生成OpenAPI文档

## 故障排除

### 常见问题

#### 1. 服务器无法启动
```
错误：MOONSHOT_API_KEY is required
解决：检查.env文件中的API密钥配置
```

#### 2. 依赖项缺失
```
错误：ImportError: No module named 'fastapi'
解决：运行 pip install -e . 安装依赖项
```

#### 3. 端口被占用
```
错误：Address already in use
解决：使用不同端口或停止占用端口的进程
```

### 调试模式
启用调试模式获取详细日志：
```bash
demo-chatbot web --reload --debug
```

### 查看日志
服务器日志会显示在控制台中，包括：
- 请求处理日志
- 错误信息
- 性能监控信息

## 开发指南

### 项目结构
```
src/demo_chatbot/
├── web_server.py      # Web服务器主文件
├── cli.py            # CLI命令（包含web命令）
├── agents/           # AI代理
├── config/           # 配置管理
└── utils/            # 工具类

根目录/
├── run_web.bat       # 生产启动脚本
├── run_web_dev.bat   # 开发启动脚本
└── README_WEB.md     # 本文档
```

### 扩展功能
1. **添加新API端点**：在`web_server.py`中添加新路由
2. **自定义前端**：修改HTML模板或创建独立前端
3. **集成新工具**：在LangGraph代理中添加新工具

### 部署建议
- **生产环境**：使用Nginx反向代理
- **HTTPS**：配置SSL证书
- **负载均衡**：多实例部署
- **监控**：集成日志监控系统

## 许可证

MIT License - 详见项目根目录的LICENSE文件

## 支持

如有问题或建议，请：
1. 查看API文档：http://127.0.0.1:8000/api/docs
2. 检查服务器日志
3. 运行健康检查：`demo-chatbot check`

---

**享受与AI的智能对话体验！** 🚀