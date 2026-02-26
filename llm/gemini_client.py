"""
Google Gemini客户端封装 - 使用新的 google.genai SDK
"""

import os
import json
from typing import List, Dict, Any, Optional
from google import genai  # 新的导入方式
from google.genai import types  # 类型定义


class GeminiClient:
    """Google Gemini客户端封装类（使用新SDK）"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            api_key: Google Gemini API密钥
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY 未设置")
        
        # 使用新的客户端初始化方式
        self.client = genai.Client(api_key=self.api_key)
        
        # 设置模型
        self.default_model = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        self.cheap_model = os.getenv("GEMINI_MODEL_CHEAP", "gemini-1.5-flash")
    
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
            messages: 消息列表 [{"role": "system/user", "content": "..."}]
            tools: 工具定义
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
        
        Returns:
            兼容OpenAI格式的响应
        """
        model_name = model or self.default_model
        
        # 转换消息格式
        system_prompt = ""
        user_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                user_messages.append(msg["content"])
        
        # 构建完整提示
        full_prompt = f"{system_prompt}\n\n{' '.join(user_messages)}"
        
        # 如果有tools，添加到提示中
        if tools:
            full_prompt += f"\n\n可用工具：{json.dumps(tools, ensure_ascii=False, indent=2)}"
            full_prompt += "\n请以JSON格式返回工具调用：{\"tool\": \"工具名\", \"parameters\": {...}}"
        
        # 配置生成参数
        config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens or 2048,
        }
        
        # 调用新SDK
        response = self.client.models.generate_content(
            model=model_name,
            contents=full_prompt,
            config=config
        )
        
        # 转换为兼容格式
        return self._convert_response(response, tools)
    
    def _convert_response(self, gemini_response, tools=None):
        """
        将Gemini响应转换为兼容格式
        """
        class MockResponse:
            def __init__(self, content, tool_calls=None):
                self.choices = [MockChoice(content, tool_calls)]
        
        class MockChoice:
            def __init__(self, content, tool_calls=None):
                self.message = MockMessage(content, tool_calls)
        
        class MockMessage:
            def __init__(self, content, tool_calls=None):
                self.content = content
                self.tool_calls = tool_calls
        
        class MockToolCall:
            def __init__(self, name, arguments):
                self.function = MockFunction(name, arguments)
        
        class MockFunction:
            def __init__(self, name, arguments):
                self.name = name
                self.arguments = arguments
        
        content = gemini_response.text
        
        # 尝试解析JSON格式的工具调用
        tool_calls = None
        if tools and "{" in content and "}" in content:
            try:
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    tool_data = json.loads(json_match.group())
                    if "tool" in tool_data and "parameters" in tool_data:
                        tool_calls = [MockToolCall(
                            tool_data["tool"],
                            json.dumps(tool_data["parameters"])
                        )]
                        content = content.replace(json_match.group(), "").strip()
            except:
                pass
        
        return MockResponse(content, tool_calls)
    
    def parse_function_call(self, response) -> Optional[Dict]:
        """
        解析函数调用
        """
        if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            return {
                "name": tool_call.function.name,
                "arguments": json.loads(tool_call.function.arguments)
            }
        return None


# 全局客户端单例
_gemini_client = None

def get_gemini_client() -> GeminiClient:
    """获取Gemini客户端单例"""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client

gemini_client = get_gemini_client()