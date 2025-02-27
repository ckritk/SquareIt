# SquareIt
## Overview
This is a Python-based grid game implemented using Pygame, where two players take turns selecting dots to form squares. The first player to complete a square wins. The game includes an AI agent using the Minimax algorithm for single-player mode.

## Game Rules
- Players take turns selecting unmarked dots on a grid.
- A square is formed when four selected dots align to create a perfect square (any size or orientation).
- The first player to complete a square wins.
- If all dots are selected without forming a square, the game ends in a draw.

## Files in the Repository
1. **`gameboard.py`** – Handles the graphical user interface (UI) for the game.
2. **`gameai.py`** – Implements the Minimax algorithm for the AI opponent.
3. **`sq.py`** – Contains core game functions like updating weights, checking for winners, and evaluating board states.

## AI Implementation
The AI prioritizes moves using:
1. **Initial Point Ordering** – Points are pre-ranked based on the number of squares they contribute to.
2. **Weight Updates** – Points adjacent to previous moves (both opponent and AI) get increased weight.
3. **Critical Move Identification** – The highest priority is given to moves that form a square (placing the fourth point when three of the same color exist).

## Getting Started
### Prerequisites
- Python 3.x
- Pygame library

### Running the Game
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd square-game
   ```
2. Install dependencies:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python gameboard.py
   ```
