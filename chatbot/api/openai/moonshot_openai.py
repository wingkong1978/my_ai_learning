import os
from typing import List, Dict, Any, Optional
from openai import OpenAI

class MoonshotOpenAIClient:
    """OpenAI-compatible client for Moonshot AI API."""
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.moonshot.cn/v1"):
        """
        Initialize Moonshot OpenAI client.
        
        Args:
            api_key: Moonshot API key. If None, uses MOONSHOT_API_KEY env var.
            base_url: Base URL for the API.
        """
        self.api_key = api_key or os.getenv("MOONSHOT_API_KEY")
        if not self.api_key:
            raise ValueError("MOONSHOT_API_KEY is required")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=base_url,
        )
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "moonshot-v1-8k",
        temperature: float = 0.8,
        max_tokens: int = 100,
        **kwargs
    ) -> str:
        """
        Send chat completion request.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            model: Model name to use for chat completions.
            temperature: Sampling temperature.
            max_tokens: Maximum number of tokens to generate.
            **kwargs: Additional parameters for the chat model.
        
        Returns:
            The response content as a string.
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    # Example usage
    client = MoonshotOpenAIClient()
    messages = [
        {"role": "system", "content": "You are a creative AI."},
        {"role": "user", "content": "请给我的花店起个名,多输出几个结果，直接输出名字，不要输出多余的语句"},
    ]
    response = client.chat_completion(messages)
    print(response)