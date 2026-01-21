#!/usr/bin/env python3
"""Pathfinding for mazes: BFS shortest path and path cells."""

from collections import deque
from typing import List, Set, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen import MazeGenerator


def find_shortest_path(gen: "MazeGenerator") -> List[str]:
    """
    Find the shortest path from entry to exit using BFS.

    Args:
        gen: A MazeGenerator instance with a generated maze.

    Returns:
        List of direction characters: N, E, S, W. Empty if no path exists.
    """
    entry_row, entry_col = gen.entry[1], gen.entry[0]
    exit_row, exit_col = gen.exit[1], gen.exit[0]

    queue: deque = deque([(entry_row, entry_col, [])])
    visited: Set[Tuple[int, int]] = {(entry_row, entry_col)}

    while queue:
        row, col, path = queue.popleft()

        if row == exit_row and col == exit_col:
            return path

        for direction, (dr, dc) in gen.DIRECTIONS.items():
            _, wall_mask, _ = gen.OPPOSITE[direction]
            if gen.maze[(row, col)] & wall_mask:
                continue  # Wall is closed

            new_row, new_col = row + dr, col + dc

            if not (0 <= new_row < gen.height and 0 <= new_col < gen.width):
                continue
            if (new_row, new_col) in visited:
                continue

            visited.add((new_row, new_col))
            queue.append((new_row, new_col, path + [direction]))

    return []


def get_path_cells(
    gen: "MazeGenerator",
    path_dirs: List[str],
) -> Set[Tuple[int, int]]:
    """
    Return the set of cell coordinates (row, col) for the given path
    from entry to exit.

    Args:
        gen: A MazeGenerator instance.
        path_dirs: List of directions from find_shortest_path.

    Returns:
        Set of (row, col) tuples along the path including entry and exit.
    """
    cells: Set[Tuple[int, int]] = set()
    r, c = gen.entry[1], gen.entry[0]
    cells.add((r, c))
    for d in path_dirs:
        dr, dc = gen.DIRECTIONS[d]
        r, c = r + dr, c + dc
        cells.add((r, c))
    return cells
