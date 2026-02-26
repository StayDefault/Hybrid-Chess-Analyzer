"""
UI可复用组件
包含棋盘渲染、状态显示等通用UI组件
"""

import gradio as gr
import chess


# =====================================
# 棋盘渲染函数
# =====================================

def render_board(fen):
    """
    生成可交互的棋盘HTML
    
    Args:
        fen: FEN格式的棋盘状态字符串
        
    Returns:
        HTML代码
    """
    # 处理特殊情况
    if not fen or fen == "start" or fen.strip() == "":
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    return f"""
    <div style="display: flex; justify-content: center; margin: 10px 0;">
        <div id="board" style="width: 400px; height: 400px;"></div>
    </div>

    <link rel="stylesheet" 
          href="https://cdnjs.cloudflare.com/ajax/libs/chessboard.js/1.0.0/chessboard-1.0.0.min.css">
    
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chessboard.js/1.0.0/chessboard-1.0.0.min.js"></script>

    <script>
        // 等待DOM和依赖完全加载
        function initBoard() {{
            if (typeof $ !== 'undefined' && typeof Chessboard !== 'undefined') {{
                // 确保容器存在
                if ($('#board').length) {{
                    try {{
                        var board = Chessboard('board', {{
                            position: '{fen}',
                            draggable: false,
                            pieceTheme: 'https://cdnjs.cloudflare.com/ajax/libs/chessboard.js/1.0.0/img/chesspieces/wikipedia/{{piece}}.png',
                            showErrors: true,
                            sparePieces: false
                        }});
                        
                        // 窗口大小变化时重新计算
                        $(window).on('resize', function() {{
                            if (board && typeof board.resize === 'function') {{
                                board.resize();
                            }}
                        }});
                        
                        console.log('棋盘初始化成功');
                    }} catch (e) {{
                        console.error('棋盘初始化失败:', e);
                        $('#board').html('<p style="color: red;">棋盘初始化失败</p>');
                    }}
                }}
            }} else {{
                console.log('等待依赖加载...');
                setTimeout(initBoard, 100);
            }}
        }}
        
        // 启动初始化
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', initBoard);
        }} else {{
            initBoard();
        }}
    </script>
    
    <style>
        .board-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
        }}
        #board {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border-radius: 4px;
            overflow: hidden;
        }}
    </style>
    """


# =====================================
# 状态卡片组件
# =====================================

def create_status_card(title, value, color="blue"):
    """
    创建状态显示卡片
    
    Args:
        title: 卡片标题
        value: 显示的值
        color: 主题颜色 (blue, green, red, purple)
    
    Returns:
        HTML代码
    """
    color_map = {
        "blue": "#3b82f6",
        "green": "#10b981",
        "red": "#ef4444",
        "purple": "#8b5cf6",
        "yellow": "#f59e0b"
    }
    
    bg_color = color_map.get(color, color_map["blue"])
    
    return f"""
    <div style="
        background: white;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid {bg_color};
        margin: 8px 0;
    ">
        <div style="color: #64748b; font-size: 14px; margin-bottom: 8px;">
            {title}
        </div>
        <div style="color: #1e293b; font-size: 24px; font-weight: bold;">
            {value}
        </div>
    </div>
    """


# =====================================
# 分析结果显示组件
# =====================================

def create_analysis_card(best_move, evaluation, variations=None):
    """
    创建分析结果显示卡片
    
    Args:
        best_move: 最佳走法
        evaluation: 评估值
        variations: 后续变化列表
    
    Returns:
        HTML代码
    """
    # 解析评估值
    try:
        eval_float = float(evaluation)
        if eval_float > 0:
            advantage = "白方优势"
            color = "blue"
        elif eval_float < 0:
            advantage = "黑方优势"
            color = "red"
        else:
            advantage = "均势"
            color = "purple"
    except:
        advantage = "未知"
        color = "gray"
        eval_float = 0
    
    # 构建HTML
    html = f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 16px 0;
    ">
        <div style="font-size: 18px; opacity: 0.9; margin-bottom: 12px;">
            🔍 分析结果
        </div>
        
        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 150px;">
                <div style="font-size: 14px; opacity: 0.8;">最佳走法</div>
                <div style="font-size: 32px; font-weight: bold;">{best_move}</div>
            </div>
            
            <div style="flex: 1; min-width: 150px;">
                <div style="font-size: 14px; opacity: 0.8;">评估值</div>
                <div style="font-size: 32px; font-weight: bold;">{evaluation}</div>
                <div style="font-size: 14px; opacity: 0.9;">{advantage}</div>
            </div>
        </div>
    """
    
    # 添加后续变化
    if variations:
        html += f"""
        <div style="
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid rgba(255,255,255,0.2);
        ">
            <div style="font-size: 14px; opacity: 0.8; margin-bottom: 8px;">
                后续变化:
            </div>
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 6px;
                padding: 10px;
                font-family: monospace;
            ">
                {variations[0] if variations else '无'}
            </div>
        </div>
        """
    
    html += "</div>"
    return html


# =====================================
# 走法历史显示组件
# =====================================

def create_move_history(moves_list):
    """
    创建走法历史显示
    
    Args:
        moves_list: 走法列表
    
    Returns:
        HTML代码
    """
    if not moves_list:
        return "<p style='color: #64748b;'>暂无走法历史</p>"
    
    html = '<div style="font-family: monospace;">'
    
    # 每两个走法一行（白方+黑方）
    for i in range(0, len(moves_list), 2):
        move_number = i // 2 + 1
        white_move = moves_list[i] if i < len(moves_list) else ""
        black_move = moves_list[i + 1] if i + 1 < len(moves_list) else ""
        
        html += f"""
        <div style="
            display: flex;
            padding: 6px 12px;
            {'background: #f8fafc;' if move_number % 2 == 0 else ''}
            border-radius: 4px;
        ">
            <span style="width: 40px; color: #64748b;">{move_number}.</span>
            <span style="width: 60px; font-weight: bold;">{white_move}</span>
            <span style="width: 60px;">{black_move}</span>
        </div>
        """
    
    html += '</div>'
    return html


# =====================================
# 棋盘缩略图组件
# =====================================

def create_board_thumbnail(fen, size=60):
    """
    创建棋盘缩略图（用于列表显示）
    
    Args:
        fen: FEN字符串
        size: 缩略图大小
    
    Returns:
        HTML代码
    """
    # 简单起见，返回文字描述
    # 实际应用中可以用canvas或svg生成小棋盘
    board = chess.Board(fen)
    turn = "白" if board.turn == chess.WHITE else "黑"
    
    return f"""
    <div style="
        display: inline-block;
        width: {size}px;
        height: {size}px;
        background: #f1f5f9;
        border-radius: 4px;
        padding: 4px;
        text-align: center;
        font-size: 12px;
        border: 1px solid #cbd5e1;
    ">
        <div>{turn}方走</div>
        <div style="font-size: 10px; color: #64748b;">{board.fullmove_number}</div>
    </div>
    """


# =====================================
# 消息气泡组件
# =====================================

def create_message_bubble(message, is_user=True):
    """
    创建聊天消息气泡
    
    Args:
        message: 消息内容
        is_user: 是否是用户消息
    
    Returns:
        HTML代码
    """
    if is_user:
        return f"""
        <div style="
            display: flex;
            justify-content: flex-end;
            margin: 12px 0;
        ">
            <div style="
                background: #3b82f6;
                color: white;
                padding: 12px 16px;
                border-radius: 18px 18px 4px 18px;
                max-width: 70%;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                {message}
            </div>
        </div>
        """
    else:
        return f"""
        <div style="
            display: flex;
            justify-content: flex-start;
            margin: 12px 0;
        ">
            <div style="
                background: #f1f5f9;
                color: #1e293b;
                padding: 12px 16px;
                border-radius: 18px 18px 18px 4px;
                max-width: 70%;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                {message}
            </div>
        </div>
        """


# =====================================
# 加载动画组件
# =====================================

def create_loading_spinner():
    """创建加载动画"""
    return """
    <div style="display: flex; justify-content: center; padding: 20px;">
        <div style="
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3b82f6;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        "></div>
    </div>
    
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """


# =====================================
# 评估值进度条组件
# =====================================

def create_evaluation_bar(evaluation, max_value=5.0):
    """
    创建评估值进度条
    
    Args:
        evaluation: 评估值（浮点数）
        max_value: 最大显示值
    
    Returns:
        HTML代码
    """
    try:
        eval_float = float(evaluation)
    except:
        eval_float = 0
    
    # 限制范围
    eval_float = max(-max_value, min(max_value, eval_float))
    
    # 计算百分比
    percentage = (eval_float + max_value) / (2 * max_value) * 100
    
    # 确定颜色
    if eval_float > 0.5:
        color = "#3b82f6"  # 蓝
    elif eval_float < -0.5:
        color = "#ef4444"  # 红
    else:
        color = "#8b5cf6"  # 紫
    
    return f"""
    <div style="margin: 16px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: #ef4444;">黑方优势</span>
            <span style="color: #3b82f6;">白方优势</span>
        </div>
        <div style="
            width: 100%;
            height: 20px;
            background: linear-gradient(90deg, #ef4444 0%, #f1f5f9 50%, #3b82f6 100%);
            border-radius: 10px;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                width: 4px;
                height: 100%;
                background: #1e293b;
                left: {percentage}%;
                transform: translateX(-50%);
                box-shadow: 0 0 4px rgba(0,0,0,0.3);
            "></div>
        </div>
        <div style="text-align: center; margin-top: 4px; font-weight: bold;">
            当前评估: {evaluation}
        </div>
    </div>
    """


# =====================================
# 工具提示组件
# =====================================

def create_tooltip(text, tooltip):
    """
    创建带工具提示的文本
    
    Args:
        text: 显示文本
        tooltip: 提示内容
    
    Returns:
        HTML代码
    """
    return f"""
    <span style="
        position: relative;
        border-bottom: 1px dashed #64748b;
        cursor: help;
    " onmouseover="this.querySelector('.tooltip').style.display='block'" 
       onmouseout="this.querySelector('.tooltip').style.display='none'">
        {text}
        <span class="tooltip" style="
            display: none;
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: #1e293b;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            white-space: nowrap;
            z-index: 1000;
        ">{tooltip}</span>
    </span>
    """


# =====================================
# 快捷按钮组组件
# =====================================

def create_button_group(buttons):
    """
    创建按钮组
    
    Args:
        buttons: 按钮列表，每个元素为 (label, value, color)
    
    Returns:
        HTML代码
    """
    html = '<div style="display: flex; gap: 8px; flex-wrap: wrap;">'
    
    for label, value, color in buttons:
        color_map = {
            "blue": "#3b82f6",
            "green": "#10b981",
            "red": "#ef4444",
            "gray": "#64748b"
        }
        bg_color = color_map.get(color, color_map["blue"])
        
        html += f"""
        <button onclick="console.log('{value}')" style="
            background: {bg_color};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: opacity 0.2s;
        " onmouseover="this.style.opacity='0.9'" 
           onmouseout="this.style.opacity='1'">
            {label}
        </button>
        """
    
    html += '</div>'
    return html


# =====================================
# 主函数测试
# =====================================

if __name__ == "__main__":
    # 测试组件
    import gradio as gr
    
    with gr.Blocks() as test_demo:
        gr.Markdown("# UI组件测试")
        
        with gr.Tab("棋盘渲染"):
            fen_input = gr.Textbox(
                label="FEN",
                value="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
            )
            board_output = gr.HTML(value=render_board(fen_input.value))
            fen_input.change(
                lambda f: render_board(f),
                fen_input,
                board_output
            )
        
        with gr.Tab("状态卡片"):
            gr.HTML(create_status_card("轮到", "白方", "blue"))
            gr.HTML(create_status_card("评估", "+0.5", "green"))
            gr.HTML(create_status_card("状态", "被将军", "red"))
        
        with gr.Tab("分析卡片"):
            gr.HTML(create_analysis_card("e4", "+0.35", ["e4 → e5 → Nf3"]))
        
        with gr.Tab("走法历史"):
            moves = ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6"]
            gr.HTML(create_move_history(moves))
        
        with gr.Tab("评估进度条"):
            eval_slider = gr.Slider(-5, 5, 0.5, label="评估值")
            eval_bar = gr.HTML(create_evaluation_bar(0.5))
            eval_slider.change(
                lambda v: create_evaluation_bar(v),
                eval_slider,
                eval_bar
            )
        
        with gr.Tab("消息气泡"):
            gr.HTML(create_message_bubble("我走e4", is_user=True))
            gr.HTML(create_message_bubble("好的，白方e4。轮到黑方。", is_user=False))
        
        with gr.Tab("加载动画"):
            gr.HTML(create_loading_spinner())
    
    test_demo.launch()