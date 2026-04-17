"""
backend/logic.py
----------------
Core game logic for Tic-Tac-Toe.

Board representation
--------------------
A flat list of 9 elements indexed 0-8:

    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8

Each cell holds one of three values:
    ""   – empty
    "X"  – human player
    "O"  – AI player

The Minimax algorithm always plays as "O" (maximising player) and
assumes the human plays as "X" (minimising player).
"""

from typing import Optional

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

Board = list[str]          # length-9 list of "", "X", or "O"
Score = int                # +10  → O wins  |  -10 → X wins  |  0 → draw

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WIN_LINES: list[tuple[int, int, int]] = [
    # rows
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    # columns
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    # diagonals
    (0, 4, 8),
    (2, 4, 6),
]

# ---------------------------------------------------------------------------
# Board helpers
# ---------------------------------------------------------------------------

def empty_board() -> Board:
    """Return a fresh, empty 9-cell board."""
    return [""] * 9


def get_empty_cells(board: Board) -> list[int]:
    """Return indices of all empty cells."""
    return [i for i, cell in enumerate(board) if cell == ""]


def check_winner(board: Board) -> Optional[str]:
    """
    Check whether someone has won.

    Returns
    -------
    "X"  if X has three in a row
    "O"  if O has three in a row
    None if no winner yet
    """
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board: Board) -> bool:
    """Return True when the board is full and there is no winner."""
    return not get_empty_cells(board) and check_winner(board) is None


def is_terminal(board: Board) -> bool:
    """Return True when the game is over (win or draw)."""
    return check_winner(board) is not None or is_draw(board)


# ---------------------------------------------------------------------------
# Minimax
# ---------------------------------------------------------------------------

def minimax(
    board: Board,
    depth: int,
    is_maximising: bool,
    alpha: int = -1000,
    beta: int = 1000,
) -> Score:
    """
    Minimax with alpha-beta pruning.

    Parameters
    ----------
    board          : current board state (mutated in place, then restored)
    depth          : recursion depth (used to prefer faster wins)
    is_maximising  : True when it is O's turn (AI), False for X's turn (human)
    alpha          : best score the maximiser can guarantee so far
    beta           : best score the minimiser can guarantee so far

    Returns
    -------
    Score
        +10 - depth  →  O wins  (prefer quicker wins)
        -10 + depth  →  X wins  (prefer longer losses)
         0           →  draw
    """
    winner = check_winner(board)
    if winner == "O":
        return 10 - depth          # AI wins — reward faster victories
    if winner == "X":
        return -10 + depth         # Human wins — delay defeat as long as possible
    if is_draw(board):
        return 0

    empty = get_empty_cells(board)

    if is_maximising:              # O's turn — maximise score
        best: Score = -1000
        for cell in empty:
            board[cell] = "O"
            score = minimax(board, depth + 1, False, alpha, beta)
            board[cell] = ""
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:      # β cut-off
                break
        return best

    else:                          # X's turn — minimise score
        best = 1000
        for cell in empty:
            board[cell] = "X"
            score = minimax(board, depth + 1, True, alpha, beta)
            board[cell] = ""
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:      # α cut-off
                break
        return best


# ---------------------------------------------------------------------------
# AI move selector
# ---------------------------------------------------------------------------

def best_move(board: Board) -> Optional[int]:
    """
    Choose the best cell index for the AI ("O") to play.

    Iterates over all empty cells, scores each with minimax, and returns
    the index that yields the highest score.

    Returns None if the board is already terminal (no move to make).
    """
    if is_terminal(board):
        return None

    best_score: Score = -1000
    chosen: Optional[int] = None

    for cell in get_empty_cells(board):
        board[cell] = "O"
        score = minimax(board, depth=0, is_maximising=False)
        board[cell] = ""

        if score > best_score:
            best_score = score
            chosen = cell

    return chosen


# ---------------------------------------------------------------------------
# Game-state summary  (convenience for the API layer)
# ---------------------------------------------------------------------------

def game_status(board: Board) -> dict:
    """
    Return a concise summary of the current game state.

    Returns
    -------
    dict with keys:
        winner  : "X" | "O" | None
        is_draw : bool
        over    : bool
    """
    winner = check_winner(board)
    draw = is_draw(board)
    return {
        "winner": winner,
        "is_draw": draw,
        "over": winner is not None or draw,
    }