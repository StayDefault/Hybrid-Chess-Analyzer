# Project Architecture Overview

## 1. High-Level Architecture
Hybrid Chess Analyzer is a web-based chess analysis tool that combines traditional chess engine (Stockfish) capabilities with modern AI (Google Gemini) to provide intelligent, conversational chess coaching. The system allows users to analyze positions via FEN input or interact naturally through chat.

## 2. Project Structure
Hybrid_Chess_Analyzer/
│
├── app.py                          # Main application entry point
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── chess_core/                      # Chess engine core module
│   ├── __init__.py
│   ├── engine.py                    # Stockfish engine wrapper
│   └── utils.py                     # Chess utility functions
│
├── sessions/                         # Session management module
│   ├── __init__.py
│   ├── manager.py                    # Session manager
│   └── models.py                     # Session data models
│
├── llm/                               # AI integration module
│   ├── __init__.py
│   ├── gemini_client.py               # Google Gemini client
│   ├── tools.py                        # Function calling definitions
│   └── prompts.py                      # Prompt templates
│
├── ui/                                 # UI components
│   ├── __init__.py
│   ├── components.py                    # Reusable UI components
│   ├── fen_tab.py                        # FEN analysis tab
│   └── chat_tab.py                       # Chat mode tab
│
└── engines/                             # External engines
    └── stockfish/
        └── stockfish-windows-x86-64-avx2.exe

## 3. Core Components
### Frontend (Gradio)
-   Framework: Gradio 4.8.0
-   Components:
   -   Chat interface with message history

Interactive chess board visualization

FEN input with validation

Analysis results display

Session state management

Key Files: ui/fen_tab.py, ui/chat_tab.py, ui/components.py

Backend
Framework: Python 3.9 with Gradio server

Architecture: Modular, clean architecture with separation of concerns

Core Modules:

app.py: Main orchestrator, tab creation

chess_core/: Chess engine abstraction

sessions/: State management

llm/: AI integration

Database
Type: In-memory only (no persistent database)

Session Storage: Python dictionary with timeout-based cleanup

Future Consideration: Redis for distributed sessions

ORM
None: Not required for current scope

Uses python-chess objects directly

Authentication
Current: No authentication (local development)

Future: API key validation for production deployment

AI Integration
Provider: Google Gemini 1.5 (Pro and Flash models)

SDK: google-genai 0.1.0

Features:

Natural language understanding

Function calling simulation via JSON

Multiple tool call handling

Conversational responses
## 4. Data Flow
   - 关键业务流程的数据走向（时序/流程图）
   - 请求流 + 异步任务流 + AI 流（如有）
## 5. Design Principles
   - SOLID、DRY、依赖注入、Clean Architecture
## 6. Environment & Configuration
## 7. Deployment & Infrastructure
## 8. Testing Strategy
## 9. Performance Considerations
## 10. Security Practices
## 11. Future Improvements
## 12. Revision History
