"""
Stockfish引擎封装
提供棋局分析功能
"""

import chess
import chess.engine
import os
import time
from typing import Dict, Any, Optional


class StockfishEngine:
    """Stockfish引擎封装类"""
    
    def __init__(self, engine_path: str):
        """
        初始化引擎
        
        Args:
            engine_path: Stockfish可执行文件路径
        """
        self.engine_path = engine_path
        self.engine = None
        self._check_engine()
    
    def _check_engine(self):
        """检查引擎文件是否存在"""
        if not os.path.exists(self.engine_path):
            raise FileNotFoundError(
                f"Stockfish引擎不存在: {self.engine_path}\n"
                "请下载引擎并设置正确的路径。"
            )
    
    def _ensure_engine(self):
        """确保引擎已启动"""
        if self.engine is None:
            self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
    
    def analyze_position(
        self, 
        fen: str, 
        time_limit: float = 2.0,
        multipv: int = 3
    ) -> Dict[str, Any]:
        """
        分析棋盘位置
        
        Args:
            fen: FEN格式的棋盘状态
            time_limit: 分析时间限制（秒）
            multipv: 返回的最佳走法数量
        
        Returns:
            包含分析结果的字典
        """
        try:
            # 验证FEN
            board = chess.Board(fen)
            
            # 启动引擎
            self._ensure_engine()
            
            # 设置分析限制
            limit = chess.engine.Limit(time=time_limit)
            
            # 获取最佳走法
            result = self.engine.play(board, limit)
            
            # 获取详细分析
            info = self.engine.analyse(
                board, 
                limit,
                multipv=multipv,
                info=chess.engine.INFO_ALL
            )
            
            # 获取评估值
            score = info[0]["score"].white()
            if score.is_mate():
                mate_in = score.mate()
                eval_str = f"马在{abs(mate_in)}步内将死"
                eval_value = 100.0 if mate_in > 0 else -100.0
            else:
                eval_value = score.score() / 100.0
                eval_str = f"{eval_value:+.2f}"
            
            # 获取后续变化
            variations = []
            if "pv" in info[0]:
                pv_moves = []
                for move in info[0]["pv"][:8]:
                    try:
                        pv_moves.append(board.san(move))
                        board.push(move)
                    except:
                        break
                variations.append(" → ".join(pv_moves))
            
            # 获取多个最佳走法
            best_moves = []
            for i, analysis in enumerate(info[:multipv]):
                move = analysis["pv"][0] if "pv" in analysis else None
                if move:
                    move_san = chess.Board(fen).san(move)
                    score = analysis["score"].white()
                    if score.is_mate():
                        move_eval = f"马在{abs(score.mate())}步"
                    else:
                        move_eval = f"{score.score()/100:+.2f}"
                    best_moves.append({
                        "rank": i + 1,
                        "move": move_san,
                        "evaluation": move_eval
                    })
            
            return {
                "success": True,
                "fen": fen,
                "best_move": chess.Board(fen).san(result.move),
                "evaluation": eval_str,
                "eval_value": eval_value,
                "variations": variations,
                "best_moves": best_moves,
                "depth": info[0].get("depth", 0),
                "nodes": info[0].get("nodes", 0),
                "time": info[0].get("time", 0)
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": f"FEN格式错误: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"分析失败: {str(e)}"
            }
    
    def quit(self):
        """关闭引擎"""
        if self.engine:
            self.engine.quit()
            self.engine = None
    
    def __enter__(self):
        self._ensure_engine()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()


# 全局单例
_engine_instance = None

def get_engine(engine_path: str = None) -> StockfishEngine:
    """获取引擎单例"""
    global _engine_instance
    if _engine_instance is None:
        if engine_path is None:
            engine_path = os.getenv("STOCKFISH_PATH")
        _engine_instance = StockfishEngine(engine_path)
    return _engine_instance