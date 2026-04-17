"""
backend/main.py
---------------
FastAPI entry point for the Tic-Tac-Toe AI server.

Endpoints
---------
POST /move        — Human plays a cell; server responds with the AI's move.
POST /reset       — Returns a fresh board.
GET  /status      — Returns game status for a given board (query param).

Run with:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from logic import best_move, empty_board, game_status

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(title="Tic-Tac-Toe AI", version="1.0.0")

# Allow the React dev server (port 3000) and any local origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class MoveRequest(BaseModel):
    """
    Payload for POST /move.

    board : list[str]  – Current 9-cell board BEFORE the human's move.
    cell  : int        – Index (0-8) the human wants to play.
    """
    board: list[str]
    cell: int

    @field_validator("board")
    @classmethod
    def validate_board(cls, v: list[str]) -> list[str]:
        if len(v) != 9:
            raise ValueError("board must have exactly 9 elements")
        allowed = {"", "X", "O"}
        for item in v:
            if item not in allowed:
                raise ValueError(f"Invalid cell value: {item!r}. Must be '', 'X', or 'O'.")
        return v

    @field_validator("cell")
    @classmethod
    def validate_cell(cls, v: int) -> int:
        if not (0 <= v <= 8):
            raise ValueError("cell must be between 0 and 8 inclusive")
        return v


class BoardRequest(BaseModel):
    """Payload that carries only a board (used by POST /reset-like helpers)."""
    board: list[str]

    @field_validator("board")
    @classmethod
    def validate_board(cls, v: list[str]) -> list[str]:
        if len(v) != 9:
            raise ValueError("board must have exactly 9 elements")
        return v


class GameResponse(BaseModel):
    """
    Unified response shape returned by /move and /reset.

    board      : updated 9-cell board
    ai_cell    : index the AI played, or None if AI did not move
    winner     : "X" | "O" | None
    is_draw    : bool
    over       : bool
    """
    board: list[str]
    ai_cell: int | None
    winner: str | None
    is_draw: bool
    over: bool


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Tic-Tac-Toe AI is running. POST /move to play."}


@app.post("/move", response_model=GameResponse)
def make_move(payload: MoveRequest):
    """
    1. Validate and apply the human's move ("X").
    2. Check whether the game is already over after the human's move.
    3. If not, let the AI ("O") pick and apply its best move.
    4. Return the updated board + game status.
    """
    board: list[str] = list(payload.board)
    cell = payload.cell

    # --- Guard: cell must be empty ---
    if board[cell] != "":
        raise HTTPException(status_code=400, detail="Cell is already occupied.")

    # --- Apply human move ---
    board[cell] = "X"

    status = game_status(board)
    if status["over"]:
        return GameResponse(board=board, ai_cell=None, **status)

    # --- AI move ---
    ai_cell = best_move(board)
    if ai_cell is not None:
        board[ai_cell] = "O"

    status = game_status(board)
    return GameResponse(board=board, ai_cell=ai_cell, **status)


@app.post("/reset", response_model=GameResponse)
def reset():
    """Return a brand-new empty board."""
    board = empty_board()
    status = game_status(board)
    return GameResponse(board=board, ai_cell=None, **status)