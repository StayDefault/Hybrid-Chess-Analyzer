"""
UI Module
Gradio界面模块
"""

from .components import render_board
from .fen_tab import create_fen_tab
from .chat_tab import create_chat_tab

__all__ = ['render_board', 'create_fen_tab', 'create_chat_tab']