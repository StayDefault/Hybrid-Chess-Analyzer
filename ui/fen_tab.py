"""
FEN分析标签页
功能：输入FEN格式的棋盘位置，显示棋盘并分析最佳走法
"""

import gradio as gr
import os
from chess_core.engine import get_engine
from ui.components import render_board, create_analysis_card


def create_fen_tab():
    """
    创建FEN分析标签页
    """
    with gr.TabItem("📊 FEN分析模式"):
        gr.Markdown("""
        ### 输入FEN格式的棋盘位置进行分析
        
        **FEN格式说明：**
        ```
        棋盘位置 / 轮到谁 / 王车易位 / 吃过路兵 / 半回合数 / 回合数
        ```
        
        **示例：**
        - 初始棋盘：`rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`
        - 意大利开局：`r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 2 3`
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # FEN输入框
                fen_input = gr.Textbox(
                    label="FEN Position",
                    lines=3,
                    placeholder="例如: rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
                    value="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
                )
                
                # 分析按钮
                with gr.Row():
                    analyze_btn = gr.Button("🔍 分析位置", variant="primary", size="lg", scale=2)
                    clear_btn = gr.Button("🗑️ 清空", size="lg", scale=1)
                
                # 分析结果区域
                with gr.Group():
                    gr.Markdown("### 📈 分析结果")
                    analysis_output = gr.HTML(label="分析详情")
            
            with gr.Column(scale=1):
                # 棋盘显示
                board_output = gr.HTML(
                    label="棋盘显示",
                    value=render_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                )
        
        # 常用示例
        gr.Markdown("### 📋 常用示例")
        
        examples = [
            ["初始棋盘", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"],
            ["意大利开局", "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 2 3"],
            ["西班牙开局", "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQ1RK1 w kq - 0 5"],
            ["王单挑", "4k3/8/8/8/8/8/8/4K3 w - - 0 1"],
            ["易位测试", "r3k2r/pppp1ppp/8/8/8/8/PPPP1PPP/R3K2R w KQkq - 0 1"],
            ["西西里防御", "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"],
        ]
        
        # 创建示例按钮网格
        with gr.Row():
            for i in range(0, len(examples), 2):
                with gr.Column():
                    for desc, fen in examples[i:i+2]:
                        gr.Button(f"📌 {desc}", size="sm").click(
                            lambda f=fen: (f, render_board(f)),
                            None,
                            [fen_input, board_output]
                        )
        
        # 高级选项
        with gr.Accordion("⚙️ 高级选项", open=False):
            time_limit = gr.Slider(
                minimum=0.5,
                maximum=5.0,
                value=2.0,
                step=0.5,
                label="分析时间（秒）"
            )
            multipv = gr.Slider(
                minimum=1,
                maximum=5,
                value=3,
                step=1,
                label="显示最佳走法数量"
            )
        
        # 分析函数
        def analyze_fen(fen, time_sec, multipv_count):
            """分析FEN位置"""
            try:
                if not fen or fen.strip() == "":
                    return render_board("start"), "请输入FEN"
                
                # 获取引擎
                engine = get_engine()
                
                # 分析位置
                result = engine.analyze_position(fen, time_limit=time_sec, multipv=multipv_count)
                
                if result["success"]:
                    # 创建分析卡片
                    analysis_html = create_analysis_card(
                        result["best_move"],
                        result["evaluation"],
                        result.get("variations", [])
                    )
                    
                    # 添加多走法列表
                    if result.get("best_moves"):
                        analysis_html += "<br><h4>其他可选走法：</h4><ul>"
                        for move in result["best_moves"][1:]:
                            analysis_html += f"<li>{move['rank']}. {move['move']} ({move['evaluation']})</li>"
                        analysis_html += "</ul>"
                    
                    return render_board(fen), analysis_html
                else:
                    return render_board(fen), f"❌ 分析失败：{result.get('error', '未知错误')}"
                    
            except Exception as e:
                return render_board(fen), f"❌ 错误：{str(e)}"
        
        def clear_inputs():
            """清空输入"""
            default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
            return default_fen, render_board(default_fen), ""
        
        # 事件绑定
        fen_input.change(
            lambda f: render_board(f),
            inputs=fen_input,
            outputs=board_output
        )
        
        analyze_btn.click(
            analyze_fen,
            inputs=[fen_input, time_limit, multipv],
            outputs=[board_output, analysis_output]
        )
        
        clear_btn.click(
            clear_inputs,
            None,
            [fen_input, board_output, analysis_output]
        )
        
        # 帮助信息
        with gr.Accordion("❓ 使用帮助", open=False):
            gr.Markdown("""
            **操作步骤：**
            1. 在输入框中粘贴FEN字符串
            2. 点击"分析位置"按钮
            3. 查看分析结果
            
            **FEN格式说明：**
            - **第一部分**：棋盘位置（8行，/分隔）
              - r/n/b/q/k/b/n/r 黑方棋子
              - R/N/B/Q/K/B/N/R 白方棋子
              - 数字表示连续空格数
            - **第二部分**：轮到谁（w=白方，b=黑方）
            - **第三部分**：王车易位权限（KQkq）
            - **第四部分**：吃过路兵目标格
            - **第五部分**：半回合数（50回合规则）
            - **第六部分**：回合数
            
            **评估值说明：**
            - 正数：白方优势
            - 负数：黑方优势
            - 单位：兵（1.0 = 一个兵的优势）
            - 马在X步内将死：表示有杀棋
            """)
    
    return {
        "fen_input": fen_input,
        "board_output": board_output,
        "analysis_output": analysis_output
    }