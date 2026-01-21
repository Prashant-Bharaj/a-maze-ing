#!/usr/bin/env python3
"""Output formatting for mazes: hex string and full output format."""

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from maze import MazeGenerator


def to_hex_string(gen: "MazeGenerator") -> str:
    """
    Convert maze to hexadecimal string format.

    Args:
        gen: A MazeGenerator instance with a generated maze.

    Returns:
        One hex digit per cell, rows separated by newlines.
    """
    lines = []
    for row in range(gen.height):
        line = ""
        for col in range(gen.width):
            hex_val = hex(gen.maze[(row, col)])[2:].upper()
            line += hex_val
        lines.append(line)
    return "\n".join(lines)


def to_output_format(gen: "MazeGenerator", path: List[str]) -> str:
    """
    Generate complete output format: hex maze, entry, exit, and path.

    Args:
        gen: A MazeGenerator instance with a generated maze.
        path: Shortest path from find_shortest_path (maze_pathfinding).

    Returns:
        Full output string with trailing newline.
    """
    output = []
    output.append(to_hex_string(gen))
    output.append("")
    output.append(f"{gen.entry[0]},{gen.entry[1]}")
    output.append(f"{gen.exit[0]},{gen.exit[1]}")
    output.append("".join(path))
    return "\n".join(output) + "\n"
