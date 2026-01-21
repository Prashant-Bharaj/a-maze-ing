#!/usr/bin/env python3
"""
Maze generation only. Pathfinding, output formatting, and visualization
live in maze_pathfinding, maze_format, and maze_visualize.
"""

import random
from typing import Tuple, Set, Dict, Optional


class MazeGenerator:
    """
    Generates a maze with configurable parameters.

    Wall encoding (hexadecimal):
    - Bit 0 (LSB, value 1): North wall
    - Bit 1 (value 2): East wall
    - Bit 2 (value 4): South wall
    - Bit 3 (value 8): West wall

    A wall being closed sets the bit to 1, open means 0.
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
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool = True,
        seed: Optional[int] = None,
    ):
        """
        Initialize maze generator.

        Args:
            width: Number of columns
            height: Number of rows
            entry: Entry coordinates (x, y) - column, row
            exit: Exit coordinates (x, y) - column, row
            perfect: If True, generates a perfect maze (single path)
            seed: Random seed for reproducibility
        """
        self.width = width
        self.height = height
        self.entry = entry  # (x, y) format
        self.exit = exit
        self.perfect = perfect
        self.seed = None

        if seed is not None:
            random.seed(seed)

        # Initialize maze with all walls closed
        self.maze: Dict[Tuple[int, int], int] = {}
        for row in range(height):
            for col in range(width):
                self.maze[(row, col)] = self.ALL_WALLS

        self.locked_cells: Set[Tuple[int, int]] = set()
        self.visited: Set[Tuple[int, int]] = set()
        self._pattern_42_cells: Set[Tuple[int, int]] = set()

        # Validate parameters
        self._validate_parameters()

    def _validate_parameters(self):
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
        
        if self.height < 5 or self.width < 7:
            raise ValueError("Maze is too small to include the '42' pattern (minimum 8x6 required)")
        
        if self.height == 5 or self.width == 7:
            raise ValueError("The maze is too small. Not all cells are reachable (minimum 8x6 required).")

    def _create_42_pattern(self) -> bool:
        """
        Create a '42' pattern using locked cells.
        Returns True if pattern was created, False if maze is too small.
        """
        # Need at least 7 columns and 5 rows for the pattern
        if self.width < 7 or self.height < 5:
            return False

        pattern_42 = [
            [1, 0, 0, 0, 1, 1, 1],  # Row 0
            [1, 0, 0, 0, 0, 0, 1],  # Row 1
            [1, 1, 1, 0, 1, 1, 1],  # Row 2
            [0, 0, 1, 0, 1, 0, 0],  # Row 3
            [0, 0, 1, 0, 1, 1, 1],  # Row 4
        ]

        # Center the pattern
        start_row = (self.height - 5) // 2
        start_col = (self.width - 7) // 2

        # Lock cells that are NOT part of the '42' shape; track cells that ARE the '42'
        for i in range(5):
            for j in range(7):
                row = start_row + i
                col = start_col + j
                if pattern_42[i][j] == 1:  # Cell should be locked (fully walled)
                    self.locked_cells.add((row, col))

        return True

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

    def _generate_perfect_maze_dfs(self, start_row: int, start_col: int):
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

    def _add_extra_paths(self):
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

    def generate(self) -> bool:
        """
        Generate the maze.
        Returns True if successful, False if maze is too small for '42' pattern.
        """
        # Create '42' pattern
        pattern_created = self._create_42_pattern()

        # Start generation from entry point
        entry_row, entry_col = (
            self.entry[1],
            self.entry[0],
        )  # Convert (x,y) to (row,col)

        # Generate perfect maze using DFS
        self._generate_perfect_maze_dfs(entry_row, entry_col)

        # Add extra paths if not perfect
        if not self.perfect:
            self._add_extra_paths()

        # Ensure entry and exit are accessible
        self._ensure_entry_exit()

        return pattern_created

    def _ensure_entry_exit(self):
        """Ensure entry and exit have proper wall configuration."""
        entry_row, entry_col = self.entry[1], self.entry[0]
        exit_row, exit_col = self.exit[1], self.exit[0]

        # Entry at top-left corner should have opening to the right or down
        # Exit at bottom-right should have opening to the left or up
        # But maintain external walls

        # Make sure entry has at least one passage
        if (entry_row, entry_col) in self.locked_cells:
            self.locked_cells.remove((entry_row, entry_col))

        # Make sure exit has at least one passage
        if (exit_row, exit_col) in self.locked_cells:
            self.locked_cells.remove((exit_row, exit_col))

    def get_42_pattern_cells(self) -> Set[Tuple[int, int]]:
        """Return the set of cell coordinates that form the '42' pattern."""
        return getattr(self, "_pattern_42_cells", set())
