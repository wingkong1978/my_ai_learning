"""
FastAPI Web Server for Demo Chatbot

Provides:
- RESTful API endpoints for chat functionality
- WebSocket support for real-time communication
- Static file serving for frontend
- Integration with LangGraph agent
- Session management
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from demo_chatbot.agents.langgraph_agent import LangGraphAgent, AgentConfig
from demo_chatbot.config.settings import get_settings
from demo_chatbot.utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    thread_id: str
    timestamp: datetime
    message_id: str

class ChatHistory(BaseModel):
    thread_id: str
    messages: List[Dict[str, Any]]

class HealthCheck(BaseModel):
    status: str
    version: str
    timestamp: datetime
    agent_status: str

# Initialize FastAPI app
app = FastAPI(
    title="Demo Chatbot Web Server",
    description="Web interface for LangChain + LangGraph + MCP Agent",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
agent_instance: Optional[LangGraphAgent] = None
active_connections: Dict[str, WebSocket] = {}
chat_sessions: Dict[str, List[Dict]] = {}

def get_agent() -> LangGraphAgent:
    """Get or create agent instance."""
    global agent_instance
    
    if agent_instance is None:
        try:
            settings = get_settings()
            config = AgentConfig(
                model_name=settings.default_model,
                temperature=settings.temperature,
                max_tokens=settings.max_tokens,
                max_file_size=settings.max_file_size,
                allowed_extensions=settings.allowed_file_extensions
            )
            agent_instance = LangGraphAgent(config)
            logger.info("Agent instance created successfully")
        except Exception as e:
            logger.error(f"Failed to create agent: {e}")
            raise HTTPException(status_code=500, detail=f"Agent initialization failed: {e}")
    
    return agent_instance

def get_or_create_thread_id(thread_id: Optional[str] = None) -> str:
    """Get existing thread ID or create a new one."""
    if not thread_id:
        thread_id = f"web_session_{uuid.uuid4().hex[:8]}"
    
    if thread_id not in chat_sessions:
        chat_sessions[thread_id] = []
    
    return thread_id

# API Routes

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main chat interface."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Demo Chatbot</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                margin: 0; 
                padding: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px; 
                background: white;
                min-height: 100vh;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }
            .header {
                text-align: center;
                padding: 20px 0;
                border-bottom: 2px solid #f0f0f0;
                margin-bottom: 20px;
            }
            .header h1 {
                color: #333;
                margin: 0;
                font-size: 2em;
            }
            .header p {
                color: #666;
                margin: 10px 0 0 0;
            }
            .chat-container { 
                height: 500px; 
                border: 2px solid #e0e0e0; 
                border-radius: 10px; 
                padding: 20px; 
                overflow-y: auto; 
                margin-bottom: 20px;
                background: #fafafa;
            }
            .message { 
                margin-bottom: 15px; 
                padding: 12px 16px;
                border-radius: 18px;
                max-width: 70%;
                word-wrap: break-word;
            }
            .user-message { 
                background: #007bff; 
                color: white; 
                margin-left: auto;
                text-align: right;
            }
            .bot-message { 
                background: #e9ecef; 
                color: #333; 
                margin-right: auto;
            }
            .input-container { 
                display: flex; 
                gap: 10px; 
            }
            .message-input { 
                flex: 1; 
                padding: 12px 16px; 
                border: 2px solid #e0e0e0; 
                border-radius: 25px; 
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }
            .message-input:focus {
                border-color: #007bff;
            }
            .send-button { 
                padding: 12px 24px; 
                background: #007bff; 
                color: white; 
                border: none; 
                border-radius: 25px; 
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s;
            }
            .send-button:hover {
                background: #0056b3;
            }
            .send-button:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            .status {
                text-align: center;
                margin: 10px 0;
                font-size: 14px;
                color: #666;
            }
            .typing {
                font-style: italic;
                color: #999;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Demo Chatbot</h1>
                <p>基于 LangChain + LangGraph + MCP 的智能聊天机器人</p>
            </div>
            <div class="status" id="status">准备就绪</div>
            <div class="chat-container" id="chatContainer">
                <div class="message bot-message">
                    你好！我是一个智能聊天机器人，可以帮助你进行文件操作、数学计算、网络搜索等任务。有什么我可以帮助你的吗？
                </div>
            </div>
            <div class="input-container">
                <input type="text" id="messageInput" class="message-input" 
                       placeholder="输入你的消息..." maxlength="1000">
                <button id="sendButton" class="send-button">发送</button>
            </div>
        </div>

        <script>
            const chatContainer = document.getElementById('chatContainer');
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            const status = document.getElementById('status');
            
            let threadId = 'web_session_' + Math.random().toString(36).substr(2, 9);
            let isWaiting = false;

            function addMessage(message, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
                messageDiv.textContent = message;
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            function setStatus(text) {
                status.textContent = text;
            }

            function setWaiting(waiting) {
                isWaiting = waiting;
                sendButton.disabled = waiting;
                messageInput.disabled = waiting;
                if (waiting) {
                    setStatus('AI 正在思考...');
                } else {
                    setStatus('准备就绪');
                }
            }

            async function sendMessage() {
                const message = messageInput.value.trim();
                if (!message || isWaiting) return;

                addMessage(message, true);
                messageInput.value = '';
                setWaiting(true);

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: message,
                            thread_id: threadId
                        })
                    });

                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }

                    const data = await response.json();
                    addMessage(data.response, false);
                    threadId = data.thread_id;
                    
                } catch (error) {
                    addMessage('抱歉，发生了错误：' + error.message, false);
                    console.error('Error:', error);
                } finally {
                    setWaiting(false);
                }
            }

            sendButton.addEventListener('click', sendMessage);
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            // 加载时的欢迎信息
            setStatus('准备就绪 - 会话ID: ' + threadId);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    try:
        agent = get_agent()
        agent_status = "healthy"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        agent_status = f"error: {str(e)}"
    
    return HealthCheck(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.now(),
        agent_status=agent_status
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage, agent: LangGraphAgent = Depends(get_agent)):
    """Chat endpoint for REST API."""
    try:
        thread_id = get_or_create_thread_id(chat_message.thread_id)
        
        # Log the user message
        user_msg = {
            "role": "user",
            "content": chat_message.message,
            "timestamp": datetime.now().isoformat(),
            "message_id": str(uuid.uuid4())
        }
        chat_sessions[thread_id].append(user_msg)
        
        # Get agent response
        logger.info(f"Processing chat message for thread {thread_id}")
        response = await agent.run(chat_message.message, thread_id=thread_id)
        
        # Log the bot response
        bot_msg = {
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat(),
            "message_id": str(uuid.uuid4())
        }
        chat_sessions[thread_id].append(bot_msg)
        
        return ChatResponse(
            response=response,
            thread_id=thread_id,
            timestamp=datetime.now(),
            message_id=bot_msg["message_id"]
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/history/{thread_id}", response_model=ChatHistory)
async def get_chat_history(thread_id: str):
    """Get chat history for a specific thread."""
    if thread_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    return ChatHistory(
        thread_id=thread_id,
        messages=chat_sessions[thread_id]
    )

@app.delete("/api/chat/history/{thread_id}")
async def clear_chat_history(thread_id: str):
    """Clear chat history for a specific thread."""
    if thread_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    chat_sessions[thread_id] = []
    return {"message": f"Chat history cleared for thread {thread_id}"}

@app.get("/api/chat/sessions")
async def list_chat_sessions():
    """List all active chat sessions."""
    sessions = []
    for thread_id, messages in chat_sessions.items():
        if messages:
            last_message = messages[-1]
            sessions.append({
                "thread_id": thread_id,
                "message_count": len(messages),
                "last_activity": last_message["timestamp"],
                "last_message_preview": last_message["content"][:100] + "..." if len(last_message["content"]) > 100 else last_message["content"]
            })
    
    return {"sessions": sessions}

# WebSocket endpoint
@app.websocket("/ws/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    active_connections[thread_id] = websocket
    
    try:
        # Ensure thread exists
        get_or_create_thread_id(thread_id)
        
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "system",
            "message": "WebSocket连接已建立",
            "thread_id": thread_id
        }))
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "chat":
                user_message = message_data.get("message", "")
                
                try:
                    # Get agent instance
                    agent = get_agent()
                    
                    # Send typing indicator
                    await websocket.send_text(json.dumps({
                        "type": "typing",
                        "message": "AI正在思考..."
                    }))
                    
                    # Process message with agent
                    response = await agent.run(user_message, thread_id=thread_id)
                    
                    # Send response back
                    await websocket.send_text(json.dumps({
                        "type": "response",
                        "message": response,
                        "thread_id": thread_id,
                        "timestamp": datetime.now().isoformat()
                    }))
                    
                except Exception as e:
                    logger.error(f"WebSocket chat error: {e}")
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": f"处理消息时发生错误: {str(e)}"
                    }))
                    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for thread {thread_id}")
        if thread_id in active_connections:
            del active_connections[thread_id]
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if thread_id in active_connections:
            del active_connections[thread_id]

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    return app

def run_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = False):
    """Run the web server."""
    settings = get_settings()
    
    try:
        # Validate settings
        settings.validate_api_key()
        logger.info("API key validation successful")
        
        # Pre-initialize agent
        get_agent()
        logger.info("Agent pre-initialization successful")
        
        logger.info(f"Starting web server on http://{host}:{port}")
        logger.info(f"API documentation available at http://{host}:{port}/api/docs")
        
        uvicorn.run(
            "demo_chatbot.web_server:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
        
    except Exception as e:
        logger.error(f"Failed to start web server: {e}")
        raise

if __name__ == "__main__":
    run_server(reload=True)