"""
对话模式标签页
功能：通过自然语言对话方式下棋和分析
"""

import gradio as gr
import json
import os
import chess
from sessions.manager import session_manager
from llm.client import llm_client
from llm.tools import tools
from llm.prompts import get_analysis_prompt
from ui.components import render_board
from chess_core.engine import get_engine


def process_chat_message(message, session_id="default"):
    """
    处理用户的自然语言输入
    返回机器人回复
    """
    if not message or message.strip() == "":
        return "请输入消息..."
    
    # 获取会话
    session = session_manager.get_session(session_id)
    current_fen = session.board.fen()
    current_turn = "白方" if session.board.turn == chess.WHITE else "黑方"
    
    try:
        # 调用OpenAI解析用户意图
        response = llm_client.chat_completion(
            messages=[
                {"role": "system", "content": f"""
                你是一个国际象棋助手。当前棋盘FEN: {current_fen}
                轮到：{current_turn}
                走法历史：{session.get_status()['history']}
                
                你的任务：
                1. 如果用户描述了一个走法（如"我走e4"），调用 make_move
                2. 如果用户问关于局势的问题（如"谁优势"），调用 analyze_position
                3. 如果用户想重新开始，调用 reset_board
                4. 如果用户描述多个走法，依次调用 make_move
                
                用友好的语气回复，解释你做了什么。
                """},
                {"role": "user", "content": message}
            ],
            tools=tools
        )
        
        response_message = response.choices[0].message
        
        # 处理函数调用
        if response_message.tool_calls:
            results = []
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                
                # 执行对应的函数
                if function_name == "make_move":
                    result = session.make_move(function_args["move"])
                    results.append(result)
                    
                elif function_name == "analyze_position":
                    # 调用引擎分析
                    engine = get_engine()
                    engine_result = engine.analyze_position(session.board.fen())
                    session.last_analysis = engine_result
                    results.append(engine_result)
                    
                elif function_name == "reset_board":
                    result = session.reset()
                    results.append({"message": result["message"]})
                    
                elif function_name == "get_move_history":
                    history = session.get_move_history()
                    results.append({"history": history})
                    
                elif function_name == "explain_position":
                    results.append({"message": "正在分析局势..."})
            
            # 生成自然语言回复
            return generate_chat_response(message, session, results)
        else:
            # 没有函数调用，可能是普通对话
            return handle_general_chat(message, session)
            
    except Exception as e:
        return f"处理出错: {str(e)}。请重试。"


def generate_chat_response(original_message, session, results):
    """生成自然语言回复"""
    status = session.get_status()
    
    # 构建回复提示词
    prompt = get_analysis_prompt(original_message, status, results)
    
    try:
        response = llm_client.chat_completion(
            messages=[
                {"role": "system", "content": "你是国际象棋助手，语气友好专业。"},
                {"role": "user", "content": prompt}
            ],
            model=os.getenv("OPENAI_MODEL_CHEAP", "gpt-3.5-turbo"),
            temperature=0.5,
            max_tokens=300
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        # 降级回复
        if results and "best_move" in results[0]:
            r = results[0]
            return f"分析完成！推荐走法：{r['best_move']}，评估：{r['evaluation']}。当前{status['status']}，轮到{status['turn']}。"
        elif results and "move" in results[0] and results[0].get("success"):
            return f"已记录 {results[0]['move']}。当前{status['status']}，轮到{status['turn']}。"
        else:
            return f"当前轮到{status['turn']}，{status['status']}。你想怎么走？"


def handle_general_chat(message, session):
    """处理普通对话（没有函数调用）"""
    status = session.get_status()
    
    prompt = f"""
    用户说：{message}
    
    当前棋盘状态：
    - 轮到：{status['turn']}
    - 状态：{status['status']}
    - 走法历史：{status['history']}
    
    请以国际象棋助手的身份友好回复。可以：
    - 如果用户问问题，回答国际象棋相关知识
    - 如果用户没指定动作，询问是想走棋还是分析
    - 保持对话自然
    """
    
    try:
        response = llm_client.chat_completion(
            messages=[
                {"role": "system", "content": "你是国际象棋助手。"},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"当前轮到{status['turn']}，请告诉我你的走法。"


def create_chat_tab():
    """
    创建对话模式标签页
    """
    with gr.TabItem("💬 AI对话模式"):
        gr.Markdown("""
        ### 🎯 像聊天一样下棋！
        
        **完全不用输入FEN**，直接描述你的走法：
        - **走棋**："我走e4"、"对手e5"、"我Nf3，对手Nc6"
        - **分析**："现在谁优势？"、"分析当前局面"
        - **重置**："我想重新开始一局"
        """)
        
        # 会话状态
        session_id = gr.State("default")
        
        with gr.Row():
            # 左侧：棋盘和信息
            with gr.Column(scale=1):
                # 棋盘显示
                chat_board = gr.HTML(
                    label="当前棋盘",
                    value=render_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                )
                
                # 棋盘状态信息
                with gr.Group():
                    gr.Markdown("### 📊 当前状态")
                    
                    with gr.Row():
                        chat_turn = gr.Textbox(
                            label="轮到",
                            interactive=False,
                            value="白方",
                            scale=1
                        )
                        chat_status = gr.Textbox(
                            label="状态",
                            interactive=False,
                            value="正常对局",
                            scale=2
                        )
                    
                    chat_fen = gr.Textbox(
                        label="FEN",
                        interactive=False,
                        lines=2,
                        value="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
                    )
                    
                    chat_history_moves = gr.Textbox(
                        label="走法历史",
                        interactive=False,
                        lines=2,
                        value="无"
                    )
                    
                    with gr.Row():
                        material_balance = gr.Textbox(
                            label="子力对比",
                            interactive=False,
                            value="白方 39 - 39 黑方"
                        )
                        legal_moves = gr.Textbox(
                            label="合法走法",
                            interactive=False,
                            value="20"
                        )
            
            # 右侧：对话区域
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    label="对话记录",
                    height=450,
                    bubble_full_width=False
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        label="你的消息",
                        placeholder="例如：我走e4 / 谁优势？ / 重新开始",
                        lines=2,
                        scale=8
                    )
                    send_btn = gr.Button(
                        "发送",
                        variant="primary",
                        scale=1,
                        min_width=80
                    )
                
                with gr.Row():
                    clear_btn = gr.Button("🗑️ 清空对话", size="sm")
                    reset_btn = gr.Button("🔄 重置棋盘", size="sm", variant="secondary")
                    analyze_btn = gr.Button("📊 分析当前", size="sm", variant="secondary")
        
        # 快捷输入示例
        gr.Markdown("### 📝 快捷输入")
        
        examples = [
            ["开局e4", "我走e4"],
            ["对手回应", "对手e5"],
            ["出动马", "我Nf3"],
            ["对手出马", "对手Nc6"],
            ["谁优势", "现在谁优势？"],
            ["分析", "分析当前局面"],
            ["重置", "我想重新开始"],
            ["走法历史", "刚才怎么走的？"]
        ]
        
        # 创建快捷按钮
        with gr.Row():
            for i in range(0, len(examples), 4):
                with gr.Column():
                    for desc, example in examples[i:i+4]:
                        gr.Button(f"📌 {desc}", size="sm").click(
                            lambda e=example: e,
                            None,
                            msg
                        )
        
        # 函数定义
        def update_chat_display(session_id):
            """更新棋盘显示和信息"""
            session = session_manager.get_session(session_id)
            status = session.get_status()
            return (
                render_board(status["fen"]),
                status["turn"],
                status["status"],
                status["fen"],
                status["history"],
                f"白方 {status['white_piece_value']} - {status['black_piece_value']} 黑方",
                str(status["legal_moves"])
            )
        
        def chat_respond(message, history, session_id):
            """处理用户消息并更新界面"""
            if not message or message.strip() == "":
                return "", history, session_id
            
            # 获取机器人回复
            bot_message = process_chat_message(message, session_id)
            
            # 更新对话历史
            history.append((message, bot_message))
            
            # 更新显示
            board_html, turn, status, fen, moves, material, legal = update_chat_display(session_id)
            
            return "", history, session_id, board_html, turn, status, fen, moves, material, legal
        
        def reset_chat(session_id):
            """重置棋盘"""
            session = session_manager.get_session(session_id)
            session.reset()
            return update_chat_display(session_id)
        
        def analyze_current(session_id):
            """分析当前局面"""
            session = session_manager.get_session(session_id)
            bot_message = process_chat_message("分析当前局面", session_id)
            
            # 获取当前对话历史
            current_history = chatbot.value or []
            current_history.append(("分析当前局面", bot_message))
            
            # 更新显示
            board_html, turn, status, fen, moves, material, legal = update_chat_display(session_id)
            
            return current_history, board_html, turn, status, fen, moves, material, legal
        
        # 事件绑定
        msg.submit(
            chat_respond,
            [msg, chatbot, session_id],
            [msg, chatbot, session_id, chat_board, chat_turn, chat_status, 
             chat_fen, chat_history_moves, material_balance, legal_moves]
        )
        
        send_btn.click(
            chat_respond,
            [msg, chatbot, session_id],
            [msg, chatbot, session_id, chat_board, chat_turn, chat_status, 
             chat_fen, chat_history_moves, material_balance, legal_moves]
        )
        
        reset_btn.click(
            reset_chat,
            [session_id],
            [chat_board, chat_turn, chat_status, chat_fen, 
             chat_history_moves, material_balance, legal_moves]
        ).then(
            lambda: ("系统：棋盘已重置", None),
            None,
            [msg, chatbot],
            queue=False
        )
        
        analyze_btn.click(
            analyze_current,
            [session_id],
            [chatbot, chat_board, chat_turn, chat_status, chat_fen, 
             chat_history_moves, material_balance, legal_moves]
        )
        
        clear_btn.click(
            lambda: None,
            None,
            chatbot,
            queue=False
        )
        
        # 初始加载
        demo.load(
            update_chat_display,
            [session_id],
            [chat_board, chat_turn, chat_status, chat_fen, 
             chat_history_moves, material_balance, legal_moves]
        )
        
        # 帮助信息
        with gr.Accordion("❓ 使用说明", open=False):
            gr.Markdown("""
            ### 如何使用AI对话模式
            
            **基本操作：**
            1. 在输入框描述你的走法，比如"我走e4"
            2. AI会自动更新棋盘并回复
            3. 继续描述对手的走法："对手e5"
            4. 随时可以问："谁优势？"或"分析一下"
            
            **支持的指令：**
            - **走棋**："我走[走法]"，"对手[走法]"
            - **分析**："谁优势？"，"分析局面"，"怎么走？"
            - **重置**："重新开始"，"新的一局"
            
            **走法格式：**
            - 兵：e4, d5, exd5（吃子）
            - 马：Nf3, Nc6
            - 象：Bb5, Bg4
            - 车：Re1
            - 后：Qe2
            - 王：O-O（短易位），O-O-O（长易位）
            
            **技巧：**
            - 可以一次描述多个走法，如"我走e4，对手e5，我Nf3"
            - 不确定走法名称时，可以用自然语言描述
            """)
    
    return {
        "session_id": session_id,
        "chatbot": chatbot,
        "msg": msg,
        "chat_board": chat_board,
        "chat_turn": chat_turn,
        "chat_status": chat_status,
        "chat_fen": chat_fen,
        "chat_history_moves": chat_history_moves
    }