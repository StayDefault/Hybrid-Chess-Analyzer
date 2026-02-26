"""
Chess Core 工具函数
"""

import chess
from typing import Optional, Tuple


def validate_fen(fen: str) -> Tuple[bool, Optional[str]]:
    """
    验证FEN字符串是否合法
    
    Args:
        fen: FEN字符串
    
    Returns:
        (是否合法, 错误信息)
    """
    try:
        chess.Board(fen)
        return True, None
    except ValueError as e:
        return False, str(e)


def fen_to_board(fen: str) -> Optional[chess.Board]:
    """
    FEN转棋盘对象
    
    Args:
        fen: FEN字符串
    
    Returns:
        棋盘对象，失败返回None
    """
    try:
        return chess.Board(fen)
    except ValueError:
        return None


def get_game_phase(board: chess.Board) -> str:
    """
    判断对局阶段
    
    Args:
        board: 棋盘对象
    
    Returns:
        开局/中局/残局
    """
    piece_count = len(board.piece_map())
    
    if piece_count > 28:
        return "开局"
    elif piece_count > 12:
        return "中局"
    else:
        return "残局"


def get_piece_value(board: chess.Board) -> Tuple[int, int]:
    """
    计算双方子力价值
    
    Args:
        board: 棋盘对象
    
    Returns:
        (白方子力价值, 黑方子力价值)
    """
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    
    white_value = 0
    black_value = 0
    
    for square, piece in board.piece_map().items():
        value = piece_values.get(piece.piece_type, 0)
        if piece.color == chess.WHITE:
            white_value += value
        else:
            black_value += value
    
    return white_value, black_value


def simplify_fen(fen: str) -> str:
    """
    简化FEN（只保留棋盘位置和轮到谁）
    
    Args:
        fen: 完整FEN
    
    Returns:
        简化FEN
    """
    parts = fen.split()
    if len(parts) >= 2:
        return f"{parts[0]} {parts[1]}"
    return fen