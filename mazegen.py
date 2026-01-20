"""Maze generator module with reusable `MazeGenerator` class.

Usage (basic):
    from mazegen import MazeGenerator

    generator = MazeGenerator(width=8, height=6, seed=42)
    print(generator.to_hex_string())           # Hex-encoded grid lines
    print(generator.solution_path)             # List of (row, col) from start to goal
    generator.save("output_maze.txt")         # Persist as the expected text format

Custom parameters:
- width / height (int): positive dimensions.
- seed (int | None): for deterministic mazes across runs.
- start / goal ((row, col)): entry/exit cells (default: (0,0) to bottom-right).

Structure access:
- `grid`: 2D list[int] of bitfields; bits mark open passages (N=1, E=2, S=4, W=8).
- `solution_path`: shortest path as a list of (row, col) coordinates using openings.
- `to_hex_rows()`: list[str] of hexadecimal digits (one row per string).
- `to_hex_string()`: newline-joined hex rows; same as output file body.
- `save(path)`: write the hex grid to disk.

The module is self-contained so it can be packaged (wheel or sdist) with `pip install .`
and later imported as `mazegen`.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, Iterable, List, Optional, Sequence, Tuple
import random

__all__ = ["MazeGenerator"]
__version__ = "0.1.0"

# Direction encoding (bit, opposite-bit, row delta, col delta)
@dataclass(frozen=True)
class Direction:
    name: str
    bit: int
    opposite: int
    dr: int
    dc: int


DIRECTIONS: Sequence[Direction] = (
    Direction("N", 1, 4, -1, 0),
    Direction("E", 2, 8, 0, 1),
    Direction("S", 4, 1, 1, 0),
    Direction("W", 8, 2, 0, -1),
)


class MazeGenerator:
    """Generate perfect mazes and expose their structure and solution.

    A *perfect* maze has exactly one path between any two cells.
    The grid stores passages as bitfields: N=1, E=2, S=4, W=8.
    """

    def __init__(
        self,
        width: int,
        height: int,
        *,
        seed: Optional[int] = None,
        start: Tuple[int, int] = (0, 0),
        goal: Optional[Tuple[int, int]] = None,
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive integers")
        self.width = width
        self.height = height
        self.start = start
        self._validate_cell(self.start, height, width, "start")
        self.goal = goal if goal is not None else (height - 1, width - 1)
        self._validate_cell(self.goal, height, width, "goal")
        self._rng = random.Random(seed)
        self.grid: List[List[int]] = []
        self.solution_path: List[Tuple[int, int]] = []
        self.generate()

    # Public API -----------------------------------------------------------
    def generate(self) -> None:
        """Generate a fresh maze and compute its solution path."""
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self._carve_passages()
        self.solution_path = self._compute_solution()

    def to_hex_rows(self) -> List[str]:
        """Return the maze as hexadecimal strings, one per row."""
        return ["".join(f"{cell:x}" for cell in row) for row in self.grid]

    def to_hex_string(self) -> str:
        """Return the maze as newline-joined hexadecimal rows."""
        return "\n".join(self.to_hex_rows())

    def save(self, path: str) -> None:
        """Write the hex-encoded maze to a file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_hex_string())

    # Internal helpers ----------------------------------------------------
    def _carve_passages(self) -> None:
        stack: List[Tuple[int, int]] = [self.start]
        visited = {self.start}

        while stack:
            r, c = stack[-1]
            candidates = self._unvisited_neighbors(r, c, visited)
            if not candidates:
                stack.pop()
                continue
            direction, nr, nc = self._rng.choice(candidates)
            self._open_passage(r, c, nr, nc, direction)
            visited.add((nr, nc))
            stack.append((nr, nc))

    def _unvisited_neighbors(
        self, r: int, c: int, visited: set[Tuple[int, int]]
    ) -> List[Tuple[Direction, int, int]]:
        neighbors: List[Tuple[Direction, int, int]] = []
        for direction in DIRECTIONS:
            nr, nc = r + direction.dr, c + direction.dc
            if 0 <= nr < self.height and 0 <= nc < self.width:
                if (nr, nc) not in visited:
                    neighbors.append((direction, nr, nc))
        return neighbors

    def _open_passage(
        self, r: int, c: int, nr: int, nc: int, direction: Direction
    ) -> None:
        # Set bits to mark a shared opening between (r,c) and (nr,nc)
        self.grid[r][c] |= direction.bit
        self.grid[nr][nc] |= direction.opposite

    def _compute_solution(self) -> List[Tuple[int, int]]:
        start, goal = self.start, self.goal
        queue: Deque[Tuple[int, int]] = deque([start])
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}

        while queue:
            r, c = queue.popleft()
            if (r, c) == goal:
                break
            for nr, nc in self._reachable_neighbors(r, c):
                if (nr, nc) not in came_from:
                    came_from[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

        if goal not in came_from:
            return []  # Should not happen in a perfect maze

        # Reconstruct path from goal to start
        path: List[Tuple[int, int]] = []
        cur: Optional[Tuple[int, int]] = goal
        while cur is not None:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        return path

    def _reachable_neighbors(self, r: int, c: int) -> Iterable[Tuple[int, int]]:
        for direction in DIRECTIONS:
            if self.grid[r][c] & direction.bit:
                nr, nc = r + direction.dr, c + direction.dc
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    yield nr, nc

    @staticmethod
    def _validate_cell(cell: Tuple[int, int], height: int, width: int, label: str) -> None:
        r, c = cell
        if not (0 <= r < height and 0 <= c < width):
            raise ValueError(f"{label} cell {cell} is out of bounds for grid {height}x{width}")


if __name__ == "__main__":
    # Quick manual demo when running `python mazegen.py`
    demo = MazeGenerator(width=8, height=6, seed=123)
    print(demo.to_hex_string())
    print("Solution:", demo.solution_path)
