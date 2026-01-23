#!/usr/bin/env python3
"""Pathfinding for mazes: BFS, DFS, and A* shortest path algorithms."""

from collections import deque
from typing import List, Set, Tuple, TYPE_CHECKING
import heapq

if TYPE_CHECKING:
    from mazegen import MazeGenerator


def find_shortest_path(gen: "MazeGenerator", algorithm: str = "bfs") -> List[str]:
    """
    Find the shortest path from entry to exit using specified algorithm.

    Args:
        gen: A MazeGenerator instance with a generated maze.
        algorithm: "bfs", "dfs", or "astar". Default is "bfs".

    Returns:
        List of direction characters: N, E, S, W. Empty if no path exists.

    Raises:
        ValueError: If algorithm is not one of the supported options.
        TypeError: If algorithm is not a string.
    """
    if not isinstance(algorithm, str):
        raise TypeError(f"Algorithm must be a string, got {type(algorithm).__name__}")
    
    algorithm_lower = algorithm.strip().lower()
    valid_algorithms = {"bfs", "dfs", "astar"}
    
    if algorithm_lower == "bfs":
        return _bfs_pathfind(gen)
    elif algorithm_lower == "dfs":
        return _dfs_pathfind(gen)
    elif algorithm_lower == "astar":
        return _astar_pathfind(gen)
    else:
        raise ValueError(
            f"Unknown algorithm: '{algorithm}'. Supported algorithms are: {', '.join(sorted(valid_algorithms))}"
        )


def _bfs_pathfind(gen: "MazeGenerator") -> List[str]:
    """Find shortest path using Breadth-First Search."""
    entry_row, entry_col = gen.entry[1], gen.entry[0]
    exit_row, exit_col = gen.exit[1], gen.exit[0]

    queue: deque[Tuple[int, int, List[str]]] = deque(
        [
            (entry_row, entry_col, []),
        ]
    )
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


def _dfs_pathfind(gen: "MazeGenerator") -> List[str]:
    """Find path using Depth-First Search (may not be shortest)."""
    entry_row, entry_col = gen.entry[1], gen.entry[0]
    exit_row, exit_col = gen.exit[1], gen.exit[0]

    stack: List[Tuple[int, int, List[str]]] = [(entry_row, entry_col, [])]
    visited: Set[Tuple[int, int]] = set()

    while stack:
        row, col, path = stack.pop()

        if (row, col) in visited:
            continue
        visited.add((row, col))

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

            stack.append((new_row, new_col, path + [direction]))

    return []


def _astar_pathfind(gen: "MazeGenerator") -> List[str]:
    """Find shortest path using A* algorithm with Manhattan distance heuristic."""
    entry_row, entry_col = gen.entry[1], gen.entry[0]
    exit_row, exit_col = gen.exit[1], gen.exit[0]

    def heuristic(r: int, c: int) -> int:
        """Manhattan distance heuristic."""
        return abs(r - exit_row) + abs(c - exit_col)

    # Priority queue: (f_score, counter, row, col, path)
    counter = 0
    open_set: List[Tuple[int, int, int, int, List[str]]] = [
        (heuristic(entry_row, entry_col), counter, entry_row, entry_col, [])
    ]
    visited: Set[Tuple[int, int]] = set()

    while open_set:
        _, _, row, col, path = heapq.heappop(open_set)

        if (row, col) in visited:
            continue
        visited.add((row, col))

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

            counter += 1
            new_path = path + [direction]
            f_score = len(new_path) + heuristic(new_row, new_col)
            heapq.heappush(open_set, (f_score, counter, new_row, new_col, new_path))

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
