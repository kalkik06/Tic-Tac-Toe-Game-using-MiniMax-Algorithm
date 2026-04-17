# Tic-Tac-Toe-Game-using-MiniMax-Algorithm
A full-stack game with an unbeatable Minimax AI.

```
tictactoe-ai/
├── backend/
│   ├── main.py          # FastAPI entry point
│   ├── logic.py         # Minimax algorithm & game state
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js       # Root component + game state
│   │   ├── App.css      # Global styles
│   │   ├── Board.js     # 3×3 grid rendering
│   │   ├── Board.css    # Board & cell styles
│   │   └── api.js       # Fetch calls to backend
│   └── package.json
└── README.md
```

---

## Tech Stack

| Layer    | Technology                         |
|----------|------------------------------------|
| Backend  | Python · FastAPI · Uvicorn         |
| AI Logic | Minimax + Alpha-Beta Pruning       |
| Frontend | React 18 · plain CSS               |
| API      | REST / JSON (no WebSockets needed) |

---

## How It Works

### Board representation
A flat `list[str]` of 9 elements (indices 0-8):

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

Each cell is `""` (empty), `"X"` (human), or `"O"` (AI).

### Minimax algorithm
- **Maximiser** → AI (`"O"`), score `+10 − depth`
- **Minimiser** → Human (`"X"`), score `−10 + depth`
- **Alpha-beta pruning** eliminates branches that can't affect the result.
- Depth-adjusted scoring ensures the AI prefers **faster wins** and **longer losses**.

### API flow
```
Human clicks cell
       ↓
POST /move  { board, cell }
       ↓
Server applies "X", runs Minimax, applies "O"
       ↓
Returns { board, ai_cell, winner, is_draw, over }
       ↓
React updates UI
```

---

## API Reference

### `POST /move`

**Request**
```json
{ "board": ["X","","","","O","","","",""], "cell": 2 }
```

**Response**
```json
{
  "board":   ["X","","X","","O","","O","",""],
  "ai_cell": 6,
  "winner":  null,
  "is_draw": false,
  "over":    false
}
```

### `POST /reset`

Returns a blank board with all status fields set to their initial values.

---
