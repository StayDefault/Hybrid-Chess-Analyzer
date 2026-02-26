# Roadmap

## Phase 1: MVP
> Goal: User inputs FEN, gets move suggestions.

- Set up minimal frontend with Gradio
- Integrate python-chess + Stockfish
- User inputs FEN, returns best move + engine evaluation
- No LLM at all — just get the engine call working

**Deliverable**: A tool that understands FEN and recommends moves. Not a chatbot, but usable.

---

## Phase 2: Natural Language Interaction
> Goal: User speaks human language, system extracts FEN and intent automatically.

- Integrate Gemini API (function calling mode)
- User input: “How can White win? Position: r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3”
- LLM calls `analyze_chess_position`
- Backend runs Stockfish analysis, returns result to LLM
- LLM formats response in natural language

**Deliverable**: A real Chess Chatbot.


---

## Phase 3: FEN-free, Pure Dialogue
> Goal: User says “I played e4, opponent e5, I Nf3, opponent Nc6 — how’s the position?”

- Maintain conversation state — keep a `board` object in session
- Each time user makes a move, LLM calls `make_move(fen, move_san)` to update the board
- Return latest FEN + analysis

---

## Phase 4: Full Game Play (Incomplete)
> Goal: Human vs. Computer — user says “I want to play Nf3”, system makes the move and responds.

- Maintain a full `chess.Board` session
- Human inputs natural language move → LLM extracts SAN → `board.push_san(move)` → legality check → Stockfish responds → return
- Add move explanations: “Why did I play this? To control the center, prepare castling…”

---
