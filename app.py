"""
Hybrid Chess Analyzer - 主程序入口（Gemini版）
"""

import os
import gradio as gr
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入UI模块
from ui.fen_tab import create_fen_tab
from ui.chat_tab import create_chat_tab


def create_app():
    """
    创建Gradio应用
    """
    with gr.Blocks(
        title="Hybrid Chess Analyzer",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: auto !important;
        }
        footer {
            display: none !important;
        }
        """
    ) as demo:
        
        # 标题
        gr.Markdown("""
        # ♟️ Hybrid Chess Analyzer
        ### 国际象棋AI分析系统 - Stockfish + Google Gemini
        
        欢迎使用混合式国际象棋分析系统！本系统提供两种分析模式：
        - **FEN分析模式**：输入FEN格式的棋盘位置，获取引擎分析
        - **AI对话模式**：通过自然语言对话方式下棋和分析
        """)
        
        # 显示配置信息
        with gr.Row():
            with gr.Column():
                api_status = "✅ 已设置" if os.getenv("GEMINI_API_KEY") else "❌ 未设置"
                gr.Markdown(f"**Gemini API**: {api_status}")
            
            with gr.Column():
                engine_path = os.getenv("STOCKFISH_PATH", "./engines/stockfish/stockfish-windows-x86-64-avx2.exe")
                engine_exists = os.path.exists(engine_path)
                engine_status = "✅ 存在" if engine_exists else "❌ 不存在"
                gr.Markdown(f"**Stockfish引擎**: {engine_status}")
        
        # 创建标签页
        with gr.Tabs():
            create_fen_tab()      # FEN分析标签页
            create_chat_tab()     # 对话模式标签页
        
        # 页脚
        gr.Markdown("---")
        gr.Markdown("""
        <div style="text-align: center; color: #64748b; padding: 20px;">
            Powered by Stockfish 16 + Google Gemini · 
            <a href=" " target="_blank">GitHub</a >
        </div>
        """)
    
    return demo


if __name__ == "__main__":
    print("=" * 50)
    print("♟️ Hybrid Chess Analyzer (Gemini版) 启动中...")
    print("=" * 50)
    
    print("\n📋 检查配置:")
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"   - Gemini API Key: ✅ 已设置 ({masked_key})")
    else:
        print(f"   - Gemini API Key: ❌ 未设置")
    
    engine_path = os.getenv("STOCKFISH_PATH", "./engines/stockfish/stockfish-windows-x86-64-avx2.exe")
    if os.path.exists(engine_path):
        print(f"   - Stockfish路径: ✅ {engine_path}")
    else:
        print(f"   - Stockfish路径: ❌ {engine_path}")
    
    print("\n🌐 访问地址: http://127.0.0.1:7860")
    print("=" * 50)
    
    demo = create_app()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=True
    )