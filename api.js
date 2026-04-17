/**
 * api.js
 * ------
 * Thin wrapper around the FastAPI backend.
 * All network calls go through here so components stay clean.
 */

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

/**
 * Send the human's chosen cell to the backend.
 *
 * @param {string[]} board  - Current 9-cell board state before the move.
 * @param {number}   cell   - Index (0-8) the human wants to play.
 * @returns {Promise<GameResponse>}
 */
export async function sendMove(board, cell) {
  const res = await fetch(`${BASE_URL}/move`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ board, cell }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Server error: ${res.status}`);
  }

  return res.json();
}

/**
 * Ask the backend for a fresh, empty board.
 *
 * @returns {Promise<GameResponse>}
 */
export async function resetGame() {
  const res = await fetch(`${BASE_URL}/reset`, { method: "POST" });

  if (!res.ok) {
    throw new Error(`Server error: ${res.status}`);
  }

  return res.json();
}

/**
 * @typedef {Object} GameResponse
 * @property {string[]}     board    - Updated 9-cell board.
 * @property {number|null}  ai_cell  - Index the AI played, or null.
 * @property {string|null}  winner   - "X", "O", or null.
 * @property {boolean}      is_draw  - True if the game is a draw.
 * @property {boolean}      over     - True if the game has ended.
 */