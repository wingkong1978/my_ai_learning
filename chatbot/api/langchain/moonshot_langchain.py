# import getpass
# import os

# os.environ["OPENAI_API_KEY"] = "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"
# os.environ["OPENAI_API_KEY"] = "sk-HecyDPgFCKdgjIK5qkdbFQXrAWJbETWcKtlFcnZoJCxoNQuL"
# os.environ["OPENAI_API_BASE"] = "https://api.moonshot.cn/v1"
# os.environ['http_proxy']="http://127.0.0.1:9328"
# os.environ['https_proxy']="http://127.0.0.1:9328"

# from langchain_openai import ChatOpenj

# model = ChatOpenAI(model="kimi-k2-0711-previewgpt-p4")

# <!--IMPORTS:[{"imported": "HumanMessage", "source": "langchain_core.messages", "docs": "https://python.langchain.com/api_reference/core/messages/langchain_core.messages.human.HumanMessage.html", "title": "Build a Simple LLM Application with LCEL"}, {"imported": "SystemMessage", "source": "langchain_core.messages", "docs": "https://python.langchain.com/api_reference/core/messages/langchain_core.messages.system.SystemMessage.html", "title": "Build a Simple LLM Application with LCEL"}]-->
# from langchain_core.messages import HumanMessage, SystemMessage

# messages = [
#     SystemMessage(content="Translate the following from English into Italian"),
#     HumanMessage(content="hi!"),
# ]

# model.invoke(messages)
import os
from typing import List, Dict, Any
from langchain_community.chat_models.moonshot import MoonshotChat
from langchain.schema import HumanMessage, SystemMessage, AIMessage

class MoonshotLangChainClient:
    """LangChain client for Moonshot AI API."""
    
    def __init__(self, api_key: str = None, model: str = "kimi-latest"):
        """
        Initialize Moonshot LangChain client.
        
        Args:
            api_key: Moonshot API key. If None, uses MOONSHOT_API_KEY env var.
            model: Model name to use for chat completions.
        """
        self.api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        if not self.api_key:
            raise ValueError("MOONSHOT_API_KEY is required")
        
        os.environ["MOONSHOT_API_KEY"] = self.api_key
        self.model = model
        self.chat = MoonshotChat(
            model=model,
            temperature=0.8,
            max_tokens=100,
        )
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Send chat completion request.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            **kwargs: Additional parameters for the chat model.
        
        Returns:
            The response content as a string.
        """
        formatted_messages = []
        for msg in messages:
            if msg["role"] == "system":
                formatted_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
        
        response = self.chat.invoke(formatted_messages, **kwargs)
        return response.content

if __name__ == "__main__":
    # Example usage
    client = MoonshotLangChainClient()
    messages = [
        {"role": "system", "content": "Translate the following from English into Italian"},
        {"role": "user", "content": "hi!"},
    ]
    response = client.chat_completion(messages)
    print(response)