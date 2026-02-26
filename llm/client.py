"""
OpenAI客户端封装
"""

from openai import OpenAI
import os
from typing import List, Dict, Any, Optional


class LLMClient:
    """OpenAI客户端封装类"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            api_key: OpenAI API密钥
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY 未设置")
        
        self.client = OpenAI(api_key=self.api_key)
        self.default_model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.cheap_model = os.getenv("OPENAI_MODEL_CHEAP", "gpt-3.5-turbo")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Any:
        """
        发送聊天完成请求
        
        Args:
            messages: 消息列表
            tools: 工具定义
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
        
        Returns:
            API响应
        """
        model = model or self.default_model
        
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        
        try:
            return self.client.chat.completions.create(**kwargs)
        except Exception as e:
            print(f"OpenAI API调用失败: {e}")
            raise
    
    def parse_function_call(self, response) -> Optional[Dict]:
        """
        解析函数调用
        
        Args:
            response: API响应
        
        Returns:
            函数调用参数，如果没有则返回None
        """
        message = response.choices[0].message
        
        if message.tool_calls and len(message.tool_calls) > 0:
            tool_call = message.tool_calls[0]
            import json
            return {
                "name": tool_call.function.name,
                "arguments": json.loads(tool_call.function.arguments)
            }
        
        return None


# 全局客户端单例
_llm_client = None

def get_llm_client() -> LLMClient:
    """获取LLM客户端单例"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client

llm_client = get_llm_client()