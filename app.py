"""
Hybrid Chess Analyzer - 主程序入口
整合所有模块，启动Gradio界面
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
        ### 国际象棋AI分析系统 - Stockfish + OpenAI GPT
        
        欢迎使用混合式国际象棋分析系统！本系统提供两种分析模式：
        - **FEN分析模式**：输入FEN格式的棋盘位置，获取引擎分析
        - **AI对话模式**：通过自然语言对话方式下棋和分析
        """)
        
        # 创建标签页
        with gr.Tabs():
            create_fen_tab()      # FEN分析标签页
            create_chat_tab()     # 对话模式标签页
        
        # 页脚
        gr.Markdown("---")
        gr.Markdown("""
        <div style="text-align: center; color: #64748b; padding: 20px;">
            Powered by Stockfish 16 + OpenAI GPT · 
            <a href="https://github.com/your-repo" target="_blank">GitHub</a>
        </div>
        """)
    
    return demo


if __name__ == "__main__":
    print("=" * 50)
    print("♟️ Hybrid Chess Analyzer 启动中...")
    print("=" * 50)
    print("\n📋 检查配置:")
    print(f"   - OpenAI API Key: {'✅ 已设置' if os.getenv('OPENAI_API_KEY') else '❌ 未设置'}")
    print(f"   - Stockfish路径: {os.getenv('STOCKFISH_PATH', '未设置')}")
    print("\n🌐 访问地址: http://localhost:7860")
    print("=" * 50)
    
    demo = create_app()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )