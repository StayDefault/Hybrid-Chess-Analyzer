# Hybrid Chess Analyzer

一个混合式国际象棋分析系统，结合Stockfish引擎和OpenAI GPT，提供智能化的棋局分析。

## ✨ 功能特点

### 📊 FEN分析模式
- 输入FEN格式的棋盘位置
- 实时可视化棋盘显示
- 获取最佳走法和评估值
- 支持常用开局示例

### 💬 AI对话模式
- 自然语言对话式下棋
- 自动跟踪棋盘状态
- 智能分析局势
- 支持多种棋局指令

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt

### 2. 配置环境变量
复制 .env.example 为 .env 并填写配置：

```text
OPENAI_API_KEY=your-api-key
STOCKFISH_PATH=./engines/stockfish/stockfish-windows-x86-64-avx2.exe

### 3. 下载Stockfish引擎
从 Stockfish官网 下载对应系统的引擎文件，
放入 engines/stockfish/ 目录。

### 4. 运行程序
bash
python app.py
访问 http://localhost:7860

## 📖 使用指南
### FEN分析模式
在输入框粘贴FEN字符串

点击"分析位置"按钮

查看最佳走法和评估值

### AI对话模式
支持的自然语言指令：

走棋：我走e4、对手e5

分析：谁优势？、分析局面

重置：重新开始

## 🏗️ 项目结构
```text
Hybrid_Chess_Analyzer/
├── app.py                 # 主程序入口
├── chess_core/            # 核心引擎模块
├── sessions/              # 会话管理模块
├── llm/                   # AI对话模块
├── ui/                    # 界面模块
└── engines/               # 引擎文件


## 📝 许可证
MIT License

``` text

---

## **chess_core/ 模块**

### **chess_core/__init__.py**
```python
"""
Chess Core Module
提供国际象棋引擎核心功能
"""

from .engine import StockfishEngine
from .utils import validate_fen, fen_to_board, get_game_phase

__all__ = ['StockfishEngine', 'validate_fen', 'fen_to_board', 'get_game_phase']