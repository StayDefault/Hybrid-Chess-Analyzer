"""
提示词模板
"""

import chess
from typing import Dict, Any


def get_system_prompt(fen: str, turn: str, history: str = "") -> str:
    """
    获取系统提示词
    
    Args:
        fen: 当前FEN
        turn: 当前轮到谁
        history: 走法历史
    
    Returns:
        系统提示词
    """
    return f"""
你是一个专业的国际象棋AI教练。你的任务是帮助用户下棋、分析局势、解答疑问。

当前对局信息：
- 棋盘FEN: {fen}
- 轮到：{turn}
- 走法历史：{history if history else "无"}

你可以：
1. 执行用户描述的走法（调用 make_move）
2. 分析当前局势（调用 analyze_position）
3. 重置棋盘（调用 reset_board）
4. 查看走法历史（调用 get_move_history）
5. 解释局势（调用 explain_position）

回复要求：
- 语气友好专业，像真正的教练
- 解释清楚每个走法的意图
- 分析局势时要通俗易懂
- 如果用户描述不清，可以追问
- 保持对话自然流畅
"""


def get_analysis_prompt(
    original_message: str,
    status: Dict[str, Any],
    results: list
) -> str:
    """
    获取分析提示词
    
    Args:
        original_message: 原始用户消息
        status: 当前状态
        results: 操作结果
    
    Returns:
        分析提示词
    """
    # 构建结果描述
    results_desc = []
    for r in results:
        if "best_move" in r:
            results_desc.append(
                f"- 分析结果：最佳走法 {r['best_move']}，评估 {r['evaluation']}"
            )
        elif "move" in r and r.get("success"):
            results_desc.append(f"- 执行走法：{r['move']}")
        elif "message" in r:
            results_desc.append(f"- 系统消息：{r['message']}")
    
    return f"""
用户消息：{original_message}

当前棋盘状态：
- 轮到：{status['turn']}
- 状态：{status['status']}
- 走法历史：{status['history']}
- 子力对比：白方 {status['white_piece_value']} - {status['black_piece_value']} 黑方
- 合法走法数：{status['legal_moves']}

操作结果：
{chr(10).join(results_desc) if results_desc else "无操作"}

请以AI教练的身份回复用户：
1. 首先确认执行的操作（如果有）
2. 解释当前局势的关键点
3. 如果棋盘有特殊状态（将军、将死等），重点说明
4. 给出下一步的建议
5. 询问用户是否需要进一步分析

回复要自然、专业、有针对性。
"""


def get_move_explanation(move_san: str, board_before: chess.Board) -> str:
    """
    获取走法解释
    
    Args:
        move_san: 走法
        board_before: 走法前的棋盘
    
    Returns:
        走法解释
    """
    explanations = {
        "e4": "占领中心，控制d5和f5格",
        "d4": "占领中心，控制e5和c5格",
        "Nf3": "出动王翼马，控制g1和e5格",
        "Nc3": "出动后翼马，控制b5和d5格",
        "O-O": "王车易位，把王转移到安全位置",
        "O-O-O": "长易位，同时出动后翼车",
    }
    
    return explanations.get(move_san, f"执行 {move_san}")