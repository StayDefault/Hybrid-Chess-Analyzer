# test_gemini.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("测试Gemini安装...")

# 检查API密钥
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY 未设置")
    exit(1)

print(f"✅ API密钥已找到: {api_key[:8]}...")

# 配置Gemini
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print(f"✅ Gemini响应: {response.text}")
except Exception as e:
    print(f"❌ Gemini调用失败: {e}")

print("测试完成")