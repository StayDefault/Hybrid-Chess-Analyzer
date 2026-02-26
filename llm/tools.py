"""
Function Calling 工具定义
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "make_move",
            "description": "执行一个国际象棋走法，更新棋盘状态",
            "parameters": {
                "type": "object",
                "properties": {
                    "move": {
                        "type": "string",
                        "description": "标准代数记谱法的走法，例如：'e4', 'Nf3', 'O-O', 'exd5'"
                    },
                    "side": {
                        "type": "string",
                        "enum": ["white", "black"],
                        "description": "走棋的一方，默认为当前轮到的一方"
                    }
                },
                "required": ["move"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_position",
            "description": "分析当前棋盘位置，返回最佳走法和评估",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "用户的具体问题，如'谁优势？'、'下一步怎么走？'"
                    },
                    "depth": {
                        "type": "integer",
                        "description": "分析深度，默认为中等"
                    }
                },
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reset_board",
            "description": "重置棋盘到初始状态",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_move_history",
            "description": "获取当前对局的走法历史",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "explain_position",
            "description": "用通俗语言解释当前局势",
            "parameters": {
                "type": "object",
                "properties": {
                    "aspect": {
                        "type": "string",
                        "enum": ["general", "material", "position", "tactics"],
                        "description": "要解释的方面"
                    }
                }
            }
        }
    }
]