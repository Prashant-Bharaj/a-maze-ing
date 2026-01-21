#!/usr/bin/env python3
"""
MazeGen - A reusable maze generation module.

This module provides a MazeGenerator class for creating configurable mazes
with customizable dimensions, entry/exit points, and maze characteristics.

Example usage:
    from mazegen import MazeGenerator

    # Create a basic maze
    gen = MazeGenerator(width=10, height=8)
    gen.generate()

    # Access the maze structure (2D grid with wall encoding)
    maze_data = gen.maze

    # Get the solution path
    path = gen.solution_path

    # Export to hex format
    hex_output = gen.to_hex_string()

Wall encoding (bits):
    - Bit 0 (value 1): North wall closed
    - Bit 1 (value 2): East wall closed
    - Bit 2 (value 4): South wall closed
    - Bit 3 (value 8): West wall closed
    - Value 15 (0xF): All walls closed
    - Value 0: All walls open
"""

import random
from collections import deque
from typing import Tuple, Set, Dict, Optional, List

__version__ = "1.0.0"
__all__ = ["MazeGenerator"]


class MazeGenerator:
    """
    Generates a maze with configurable parameters.

    The maze is represented as a 2D grid where each cell stores wall information
    as a 4-bit integer (hexadecimal value 0-15).

    Attributes:
        width (int): Number of columns in the maze
        height (int): Number of rows in the maze
        entry (Tuple[int, int]): Entry coordinates as (x, y) - column, row
        exit (Tuple[int, int]): Exit coordinates as (x, y) - column, row
        perfect (bool): Whether the maze has exactly one path between any two points
        seed (Optional[int]): Random seed for reproducible mazes
        maze (Dict[Tuple[int, int], int]): The maze grid data (row, col) -> wall_value
        solution_path (List[Tuple[int, int]]): List of (row, col) coordinates from entry to exit
    """

    # Wall bit masks
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL_WALLS = 15  # All walls closed

    # Direction vectors: (row_delta, col_delta)
    DIRECTIONS = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

    # Opposite walls for consistency
    OPPOSITE = {
        "N": ("S", NORTH, SOUTH),
        "E": ("W", EAST, WEST),
        "S": ("N", SOUTH, NORTH),
        "W": ("E", WEST, EAST),
    }

    def __init__(
        self,
        width: int = 10,
        height: int = 10,
        entry: Optional[Tuple[int, int]] = None,
        exit: Optional[Tuple[int, int]] = None,
        perfect: bool = True,
        seed: Optional[int] = None,
    ):
        """
        Initialize maze generator.

        Args:
            width: Number of columns (default: 10)
            height: Number of rows (default: 10)
            entry: Entry coordinates (x, y) - column, row. Defaults to (0, 0)
            exit: Exit coordinates (x, y) - column, row. Defaults to (width-1, height-1)
            perfect: If True, generates a perfect maze with single path between any points (default: True)
            seed: Random seed for reproducibility (default: None, uses random)

        Raises:
            ValueError: If dimensions are invalid or coordinates are out of bounds
        """
        self.width = width
        self.height = height
        self.entry = entry if entry is not None else (0, 0)
        self.exit = exit if exit is not None else (width - 1, height - 1)
        self.perfect = perfect
        self.seed = seed

        if seed is not None:
            random.seed(seed)

        # Initialize maze with all walls closed
        self.maze: Dict[Tuple[int, int], int] = {}
        for row in range(height):
            for col in range(width):
                self.maze[(row, col)] = self.ALL_WALLS

        self.locked_cells: Set[Tuple[int, int]] = set()
        self.visited: Set[Tuple[int, int]] = set()
        self.solution_path: List[Tuple[int, int]] = []

        # Validate parameters
        self._validate_parameters()

    def _validate_parameters(self) -> None:
        """Validate maze parameters."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be positive")

        ex, ey = self.entry
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ValueError(f"Entry ({ex}, {ey}) is outside maze bounds")

        xx, xy = self.exit
        if not (0 <= xx < self.width and 0 <= xy < self.height):
            raise ValueError(f"Exit ({xx}, {xy}) is outside maze bounds")

        if self.entry == self.exit:
            raise ValueError("Entry and exit must be different")

    def _is_valid_cell(self, row: int, col: int) -> bool:
        """Check if cell coordinates are within maze bounds."""
        return 0 <= row < self.height and 0 <= col < self.width

    def _carve_passage(
        self, row: int, col: int, direction: str
    ) -> Optional[Tuple[int, int]]:
        """
        Carve a passage from current cell in the given direction.
        Returns the next cell coordinates or None if not possible.
        """
        dr, dc = self.DIRECTIONS[direction]
        new_row, new_col = row + dr, col + dc

        if not self._is_valid_cell(new_row, new_col):
            return None

        # Remove walls between cells
        _, wall_from, wall_to = self.OPPOSITE[direction]
        self.maze[(row, col)] &= ~wall_from
        self.maze[(new_row, new_col)] &= ~wall_to

        return (new_row, new_col)

    def _generate_perfect_maze_dfs(self, start_row: int, start_col: int) -> None:
        """Generate a perfect maze using recursive backtracking (DFS)."""
        stack = [(start_row, start_col)]
        self.visited.add((start_row, start_col))

        while stack:
            row, col = stack[-1]

            # Get unvisited neighbors
            neighbors = []
            for direction in ["N", "E", "S", "W"]:
                dr, dc = self.DIRECTIONS[direction]
                new_row, new_col = row + dr, col + dc

                if (
                    self._is_valid_cell(new_row, new_col)
                    and (new_row, new_col) not in self.visited
                    and (new_row, new_col) not in self.locked_cells
                ):
                    neighbors.append((direction, new_row, new_col))

            if neighbors:
                # Choose random unvisited neighbor
                direction, new_row, new_col = random.choice(neighbors)
                self._carve_passage(row, col, direction)
                self.visited.add((new_row, new_col))
                stack.append((new_row, new_col))
            else:
                # Backtrack
                stack.pop()

    def _check_wide_corridor(self, row: int, col: int) -> bool:
        """
        Check if opening a passage would create a corridor wider than 2 cells.
        Returns True if it would create an invalid wide corridor.
        """
        # Check for 3x3 open areas
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = row + dr, col + dc
                if not self._is_valid_cell(r, c):
                    continue

                # Check if we have a 3x3 open area centered at (r, c)
                open_count = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        check_r, check_c = r + i, c + j
                        if self._is_valid_cell(check_r, check_c):
                            walls = self.maze[(check_r, check_c)]
                            # Count as open if it has at least one open wall
                            if walls != self.ALL_WALLS:
                                open_count += 1

                if open_count >= 9:  # All 9 cells in 3x3 are open
                    return True

        return False

    def _add_extra_paths(self) -> None:
        """Add extra passages for non-perfect mazes."""
        # Number of extra passages to add
        num_extra = max(1, (self.width * self.height) // 20)

        attempts = 0
        added = 0
        max_attempts = num_extra * 10

        while added < num_extra and attempts < max_attempts:
            attempts += 1
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)

            if (row, col) in self.locked_cells:
                continue

            # Try to remove a wall
            directions = list(self.DIRECTIONS.keys())
            random.shuffle(directions)

            for direction in directions:
                dr, dc = self.DIRECTIONS[direction]
                new_row, new_col = row + dr, col + dc

                if (
                    self._is_valid_cell(new_row, new_col)
                    and (new_row, new_col) not in self.locked_cells
                ):
                    # Check if wall exists
                    _, wall_from, _ = self.OPPOSITE[direction]
                    if self.maze[(row, col)] & wall_from:
                        # Try removing the wall
                        self._carve_passage(row, col, direction)

                        # Check if it creates a wide corridor
                        if self._check_wide_corridor(row, col):
                            # Restore the wall
                            _, wall_from, wall_to = self.OPPOSITE[direction]
                            self.maze[(row, col)] |= wall_from
                            self.maze[(new_row, new_col)] |= wall_to
                        else:
                            added += 1
                            break

    def _ensure_entry_exit(self) -> None:
        """Ensure entry and exit are accessible."""
        entry_row, entry_col = self.entry[1], self.entry[0]
        exit_row, exit_col = self.exit[1], self.exit[0]

        # Make sure entry and exit are not locked
        if (entry_row, entry_col) in self.locked_cells:
            self.locked_cells.remove((entry_row, entry_col))

        if (exit_row, exit_col) in self.locked_cells:
            self.locked_cells.remove((exit_row, exit_col))

    def _find_shortest_path(self) -> List[str]:
        """
        Find the shortest path from entry to exit using BFS.

        Returns:
            List of direction characters: N, E, S, W. Empty if no path exists.
        """
        entry_row, entry_col = self.entry[1], self.entry[0]
        exit_row, exit_col = self.exit[1], self.exit[0]

        queue: deque = deque([(entry_row, entry_col, [])])
        visited_set: Set[Tuple[int, int]] = {(entry_row, entry_col)}

        while queue:
            row, col, path = queue.popleft()

            if row == exit_row and col == exit_col:
                return path

            for direction, (dr, dc) in self.DIRECTIONS.items():
                _, wall_mask, _ = self.OPPOSITE[direction]
                if self.maze[(row, col)] & wall_mask:
                    continue  # Wall is closed

                new_row, new_col = row + dr, col + dc

                if not self._is_valid_cell(new_row, new_col):
                    continue
                if (new_row, new_col) in visited_set:
                    continue

                visited_set.add((new_row, new_col))
                queue.append((new_row, new_col, path + [direction]))

        return []

    def _compute_solution_path(self) -> None:
        """Compute and store the solution path as cell coordinates."""
        path_dirs = self._find_shortest_path()
        cells: List[Tuple[int, int]] = []

        r, c = self.entry[1], self.entry[0]
        cells.append((r, c))

        for d in path_dirs:
            dr, dc = self.DIRECTIONS[d]
            r, c = r + dr, c + dc
            cells.append((r, c))

        self.solution_path = cells

    def generate(self) -> "MazeGenerator":
        """
        Generate the maze.

        Returns:
            Self for method chaining

        Example:
            gen = MazeGenerator(width=10, height=10).generate()
            print(gen.to_hex_string())
        """
        # Start generation from entry point
        entry_row, entry_col = self.entry[1], self.entry[0]

        # Generate perfect maze using DFS
        self._generate_perfect_maze_dfs(entry_row, entry_col)

        # Add extra paths if not perfect
        if not self.perfect:
            self._add_extra_paths()

        # Ensure entry and exit are accessible
        self._ensure_entry_exit()

        # Compute solution path
        self._compute_solution_path()

        return self

    def to_hex_string(self) -> str:
        """
        Convert maze to hexadecimal string format.

        Each row is represented as a line of hexadecimal digits (0-F),
        where each digit encodes the wall configuration for one cell.

        Returns:
            Multi-line string with hex-encoded maze data

        Example:
            >>> gen = MazeGenerator(width=4, height=3, seed=42).generate()
            >>> print(gen.to_hex_string())
            FEFE
            ABAA
            BABA
        """
        lines = []
        for row in range(self.height):
            row_hex = ""
            for col in range(self.width):
                wall_value = self.maze[(row, col)]
                row_hex += f"{wall_value:X}"
            lines.append(row_hex)
        return "\n".join(lines)

    def get_maze_grid(self) -> List[List[int]]:
        """
        Get the maze as a 2D list.

        Returns:
            2D list where maze[row][col] is the wall value for that cell

        Example:
            >>> gen = MazeGenerator(width=3, height=2, seed=42).generate()
            >>> grid = gen.get_maze_grid()
            >>> print(grid[0][0])  # Wall value for top-left cell
            13
        """
        grid = []
        for row in range(self.height):
            row_data = []
            for col in range(self.width):
                row_data.append(self.maze[(row, col)])
            grid.append(row_data)
        return grid

    def has_wall(self, row: int, col: int, direction: str) -> bool:
        """
        Check if a cell has a wall in the given direction.

        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            direction: One of 'N', 'E', 'S', 'W'

        Returns:
            True if wall exists in that direction, False if open

        Raises:
            ValueError: If direction is invalid or coordinates out of bounds

        Example:
            >>> gen = MazeGenerator(width=5, height=5, seed=42).generate()
            >>> gen.has_wall(0, 0, 'N')  # Check north wall of top-left cell
            True
        """
        if not self._is_valid_cell(row, col):
            raise ValueError(f"Cell ({row}, {col}) is out of bounds")

        if direction not in self.DIRECTIONS:
            raise ValueError(f"Invalid direction '{direction}'. Must be N, E, S, or W")

        _, wall_mask, _ = self.OPPOSITE[direction]
        return bool(self.maze[(row, col)] & wall_mask)

    def get_solution_directions(self) -> str:
        """
        Get the solution path as a string of direction characters.

        Returns:
            String of 'N', 'E', 'S', 'W' characters representing the path

        Example:
            >>> gen = MazeGenerator(width=5, height=5, seed=42).generate()
            >>> directions = gen.get_solution_directions()
            >>> print(directions)
            EESSEENNW
        """
        path_dirs = self._find_shortest_path()
        return "".join(path_dirs)

    def __repr__(self) -> str:
        """String representation of the maze generator."""
        return (
            f"MazeGenerator(width={self.width}, height={self.height}, "
            f"entry={self.entry}, exit={self.exit}, perfect={self.perfect}, "
            f"seed={self.seed})"
        )


if __name__ == "__main__":
    # Example usage
    print("MazeGen - Maze Generation Module")
    print("=" * 50)
    print()

    # Create a small maze with seed for reproducibility
    gen = MazeGenerator(width=8, height=6, seed=42, perfect=True)
    gen.generate()

    print(f"Generated {gen.width}x{gen.height} maze")
    print(f"Entry: {gen.entry}, Exit: {gen.exit}")
    print(f"Solution path length: {len(gen.solution_path)} cells")
    print()
    print("Hex format:")
    print(gen.to_hex_string())
    print()
    print("Solution directions:", gen.get_solution_directions())
