/**
 * Board.js
 * --------
 * Renders the 3×3 Tic-Tac-Toe grid.
 *
 * Props
 * -----
 * board        {string[]}   - 9-element array: "", "X", or "O"
 * onCellClick  {Function}   - Called with the cell index when a player clicks.
 * disabled     {boolean}    - If true, no clicks are processed (AI thinking / game over).
 * winnerCells  {number[]}   - Indices of the three winning cells (highlighted).
 * lastAiCell   {number|null}- Index of the AI's last move (pulse animation).
 */

import React from "react";
import "./Board.css";

export default function Board({
  board,
  onCellClick,
  disabled,
  winnerCells = [],
  lastAiCell = null,
}) {
  return (
    <div className="board" role="grid" aria-label="Tic-Tac-Toe board">
      {board.map((value, idx) => {
        const isWinner = winnerCells.includes(idx);
        const isAiLast = idx === lastAiCell;
        const isEmpty = value === "";

        const classes = [
          "cell",
          value === "X" ? "cell--x" : value === "O" ? "cell--o" : "",
          isWinner ? "cell--winner" : "",
          isAiLast ? "cell--ai-last" : "",
          isEmpty && !disabled ? "cell--playable" : "",
        ]
          .filter(Boolean)
          .join(" ");

        return (
          <button
            key={idx}
            className={classes}
            onClick={() => !disabled && isEmpty && onCellClick(idx)}
            aria-label={
              value
                ? `Cell ${idx + 1}: ${value}`
                : `Cell ${idx + 1}: empty`
            }
            aria-disabled={disabled || !isEmpty}
          >
            {value && <span className="cell__symbol">{value}</span>}
          </button>
        );
      })}
    </div>
  );
}