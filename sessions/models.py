"""
会话数据模型
"""

import chess
from typing import List, Dict, Any, Optional


class ChessSession:
    """国际象棋会话类，管理单个对话的棋盘状态"""
    
    def __init__(self, session_id: str = "default"):
        """
        初始化会话
        
        Args:
            session_id: 会话ID
        """
        self.session_id = session_id
        self.board = chess.Board()
        self.history: List[str] = []
        self.last_analysis: Optional[Dict[str, Any]] = None
        self.created_at = None  # 可以添加时间戳
        self.updated_at = None
    
    def make_move(self, move_san: str) -> Dict[str, Any]:
        """
        执行走法
        
        Args:
            move_san: 标准代数记谱法走法
        
        Returns:
            执行结果
        """
        try:
            # 解析走法
            move = self.board.parse_san(move_san)
            
            # 检查合法性
            if move not in self.board.legal_moves:
                return {
                    "success": False,
                    "error": f"非法走法: {move_san}",
                    "fen": self.board.fen(),
                    "turn": "白方" if self.board.turn == chess.WHITE else "黑方"
                }
            
            # 执行走法
            self.board.push(move)
            self.history.append(move_san)
            
            return {
                "success": True,
                "fen": self.board.fen(),
                "move": move_san,
                "turn": "白方" if self.board.turn == chess.WHITE else "黑方",
                "move_number": len(self.history)
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": f"无效走法格式: {move_san} - {str(e)}",
                "fen": self.board.fen()
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取当前棋盘状态
        
        Returns:
            状态信息
        """
        # 检查特殊状态
        if self.board.is_checkmate():
            winner = "黑方" if self.board.turn == chess.WHITE else "白方"
            status = f"将死！{winner}获胜"
            game_over = True
        elif self.board.is_stalemate():
            status = "逼和"
            game_over = True
        elif self.board.is_insufficient_material():
            status = "子力不足，和棋"
            game_over = True
        elif self.board.is_seventyfive_moves():
            status = "75步规则和棋"
            game_over = True
        elif self.board.is_fivefold_repetition():
            status = "五次重复和棋"
            game_over = True
        elif self.board.is_check():
            status = f"{'白方' if self.board.turn == chess.WHITE else '黑方'}被将军"
            game_over = False
        else:
            status = "正常对局"
            game_over = False
        
        # 计算双方子力
        from chess_core.utils import get_piece_value
        white_value, black_value = get_piece_value(self.board)
        
        return {
            "fen": self.board.fen(),
            "turn": "白方" if self.board.turn == chess.WHITE else "黑方",
            "turn_code": "w" if self.board.turn == chess.WHITE else "b",
            "status": status,
            "game_over": game_over,
            "history": " → ".join(self.history) if self.history else "无",
            "move_count": len(self.history),
            "fullmove_number": self.board.fullmove_number,
            "white_piece_value": white_value,
            "black_piece_value": black_value,
            "material_balance": white_value - black_value,
            "legal_moves": len(list(self.board.legal_moves))
        }
    
    def reset(self) -> Dict[str, Any]:
        """
        重置棋盘到初始状态
        
        Returns:
            重置结果
        """
        self.board = chess.Board()
        self.history = []
        self.last_analysis = None
        
        return {
            "success": True,
            "message": "棋盘已重置到初始位置",
            "fen": self.board.fen()
        }
    
    def get_move_history(self) -> List[Dict[str, str]]:
        """
        获取格式化的走法历史
        
        Returns:
            走法历史列表，每两步一组
        """
        moves = []
        for i in range(0, len(self.history), 2):
            move_number = i // 2 + 1
            white_move = self.history[i] if i < len(self.history) else ""
            black_move = self.history[i + 1] if i + 1 < len(self.history) else ""
            moves.append({
                "number": move_number,
                "white": white_move,
                "black": black_move
            })
        return moves
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "session_id": self.session_id,
            "fen": self.board.fen(),
            "history": self.history,
            "status": self.get_status()
        }