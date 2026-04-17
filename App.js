/**
 * App.js
 * ------
 * Root component. Owns all game state and orchestrates API calls.
 *
 * State
 * -----
 * board      {string[]}    9-cell board ("", "X", "O")
 * status     {object}      { winner, is_draw, over } from the API
 * thinking   {boolean}     true while waiting for the server response
 * lastAiCell {number|null} index of the AI's most recent move
 * error      {string|null} user-visible error message
 */
/* eslint-disable */
import React, { useState, useEffect, useCallback } from "react";
import Board from "./Board";
import { sendMove, resetGame } from "./api";
import "./App.css";

// Win-line lookup (mirrors logic.py WIN_LINES) — used client-side only
// to highlight the winning triplet without an extra round-trip.
const WIN_LINES = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
  [0, 3, 6], [1, 4, 7], [2, 5, 8], // cols
  [0, 4, 8], [2, 4, 6],            // diagonals
];

function getWinnerCells(board, winner) {
  if (!winner) return [];
  for (const [a, b, c] of WIN_LINES) {
    if (board[a] === winner && board[b] === winner && board[c] === winner) {
      return [a, b, c];
    }
  }
  return [];
}

const INITIAL_BOARD = Array(9).fill("");
const INITIAL_STATUS = { winner: null, is_draw: false, over: false };

export default function App() {
  const [board, setBoard]           = useState(INITIAL_BOARD);
  const [status, setStatus]         = useState(INITIAL_STATUS);
  const [thinking, setThinking]     = useState(false);
  const [lastAiCell, setLastAiCell] = useState(null);
  const [error, setError]           = useState(null);
  const [score, setScore]           = useState({ X: 0, O: 0, draws: 0 });

  // Update the scoreboard whenever a game ends.
  useEffect(() => {
    if (!status.over) return;
    setScore((prev) => {
      if (status.winner === "X") return { ...prev, X: prev.X + 1 };
      if (status.winner === "O") return { ...prev, O: prev.O + 1 };
      if (status.is_draw)        return { ...prev, draws: prev.draws + 1 };
      return prev;
    });
  }, [status.over]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleCellClick = useCallback(
    async (cellIndex) => {
      if (thinking || status.over) return;
      setError(null);
      setThinking(true);

      try {
        const data = await sendMove(board, cellIndex);
        setBoard(data.board);
        setStatus({ winner: data.winner, is_draw: data.is_draw, over: data.over });
        setLastAiCell(data.ai_cell);
      } catch (err) {
        setError(err.message || "Something went wrong. Please try again.");
      } finally {
        setThinking(false);
      }
    },
    [board, thinking, status.over]
  );

  const handleReset = useCallback(async () => {
    setError(null);
    setThinking(true);
    try {
      const data = await resetGame();
      setBoard(data.board);
      setStatus(INITIAL_STATUS);
      setLastAiCell(null);
    } catch (err) {
      setError(err.message || "Could not reset the game.");
    } finally {
      setThinking(false);
    }
  }, []);

  const winnerCells = getWinnerCells(board, status.winner);

  // ── Status message ────────────────────────────────────────────────────────
  let statusMsg = "Your turn — you are X";
  if (thinking)             statusMsg = "AI is thinking…";
  else if (status.winner === "X") statusMsg = "You win! 🎉";
  else if (status.winner === "O") statusMsg = "AI wins! 🤖";
  else if (status.is_draw)        statusMsg = "It's a draw!";

  return (
    <div className="app">
      {/* Header */}
      <header className="app__header">
        <h1 className="app__title">
          <span className="app__title-x">X</span>
          <span className="app__title-sep"> vs </span>
          <span className="app__title-o">O</span>
        </h1>
        <p className="app__subtitle">Minimax AI · unbeatable</p>
      </header>

      {/* Scoreboard */}
      <div className="scoreboard">
        <div className="scoreboard__item scoreboard__item--x">
          <span className="scoreboard__label">You (X)</span>
          <span className="scoreboard__value">{score.X}</span>
        </div>
        <div className="scoreboard__item scoreboard__item--draw">
          <span className="scoreboard__label">Draws</span>
          <span className="scoreboard__value">{score.draws}</span>
        </div>
        <div className="scoreboard__item scoreboard__item--o">
          <span className="scoreboard__label">AI (O)</span>
          <span className="scoreboard__value">{score.O}</span>
        </div>
      </div>

      {/* Status banner */}
      <div
        className={[
          "status-banner",
          thinking ? "status-banner--thinking" : "",
          status.winner === "X" ? "status-banner--win" : "",
          status.winner === "O" ? "status-banner--loss" : "",
          status.is_draw ? "status-banner--draw" : "",
        ]
          .filter(Boolean)
          .join(" ")}
        aria-live="polite"
      >
        {statusMsg}
      </div>

      {/* Board */}
      <main className="app__board-wrapper">
        <Board
          board={board}
          onCellClick={handleCellClick}
          disabled={thinking || status.over}
          winnerCells={winnerCells}
          lastAiCell={lastAiCell}
        />
      </main>

      {/* Error */}
      {error && (
        <p className="app__error" role="alert">
          ⚠ {error}
        </p>
      )}

      {/* New Game button */}
      <button
        className="btn-new-game"
        onClick={handleReset}
        disabled={thinking}
      >
        {status.over ? "Play Again" : "New Game"}
      </button>
    </div>
  );
}