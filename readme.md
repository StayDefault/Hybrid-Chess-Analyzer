# ♟️ Hybrid Chess Analyzer

A hybrid chess analysis system that combines the power of **Stockfish** with **Google Gemini** to provide intelligent position evaluation, natural-language interaction, and an intuitive visual interface.

---

## 📌 Overview

Hybrid Chess Analyzer is designed for players, developers, and chess enthusiasts who want:

- 🔍 Accurate engine analysis  
- 💬 Natural language chess interaction  
- 📊 Visual board feedback  
- 🧠 AI-assisted understanding of positions  

The system merges classical engine strength with modern LLM reasoning to create a smarter chess analysis experience.

---

## ✨ Features

### 📊 FEN Analysis Mode

- Paste any FEN position
- Real-time visual chessboard
- Best move suggestions from Stockfish
- Position evaluation (centipawn / mate)
- Built-in opening examples

---

### 💬 AI Chat Mode

- Play chess via natural language
- Automatic board tracking
- Ask positional questions
- Flexible chess commands
- Context-aware analysis

Example interactions:
I play e4,
Opponent plays c5,
Who is better?
Analyze the position
Restart the game


---

## 🚀 Quick Start

### 1️. Clone the Repository

```bash
git clone https://github.com/StayDefault/Hybrid-Chess-Analyzer.git
cd Hybrid-Chess-Analyzer
```

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
### 2. Configure Environment Variables
copy .env and example edit .env and fill in：

```text
OPENAI_API_KEY=your-api-key
STOCKFISH_PATH=./engines/stockfish/stockfish-windows-x86-64-avx2.exe
```
### 3. Download Stockfish Engine
Download the correct binary for your OS from the official Stockfish website and place it into:
```text
engines/stockfish/
```
### 4. Run the Program
bash
python app.py
visit http://localhost:7860

## 📖 User Guide
### FEN Analysis Mode
1. Paste a FEN string

2. Click Analyze Position

3. View best move and evaluation

### AI Chat Mode
Make moves

I play e4
Black plays e5

Ask for analysis

Who is winning?
Evaluate this position

Reset game

Restart
New game

## 🏗️ Project Structure
```text
Hybrid_Chess_Analyzer/
├── app.py                 # Main application entry
├── chess_core/            # Core engine module
│   ├── engine.py
│   ├── utils.py
│   └── __init__.py
├── sessions/              # Session management
├── llm/                   # AI conversation module
├── ui/                    # User interface
├── engines/               # Stockfish binaries (not included)
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Requirements

- Python 3.9+
- Stockfish engine
- OpenAI / Gemini API access
- Modern web browser

---

## 🛠️ Troubleshooting

### ❗ Stockfish not found

Make sure:

- The binary exists  
- The path in `.env` is correct  
- The file has execute permission (Linux/macOS)

---

### ❗ Port already in use

Change the port in `app.py` or stop the conflicting process.

---

## 🔮 Roadmap

- [ ] PGN import support  
- [ ] Opening explorer  
- [ ] Multi-engine comparison  
- [ ] Cloud deployment guide  
- [ ] Mobile-friendly UI  

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repo  
2. Create your feature branch  
3. Commit your changes  
4. Open a Pull Request  

---

## 📜 License

This project is licensed under the **MIT License**.

---

## ⭐ Acknowledgements

- Stockfish team  
- Google Gemini  
- Python chess community  

---

**If you find this project useful, consider giving it a star ⭐**
