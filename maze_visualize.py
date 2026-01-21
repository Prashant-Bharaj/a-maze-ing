#!/usr/bin/env python3
"""ASCII maze visualization with optional path and 42 pattern highlighting."""

from typing import Dict, List, Optional, TYPE_CHECKING

from maze_pathfinding import get_path_cells

if TYPE_CHECKING:
    from mazegen import MazeGenerator


def visualize(
    gen: "MazeGenerator",
    path: List[str],
    *,
    show_path: bool = False,
    wall_color: Optional[str] = None,
    path_color: Optional[str] = None,
    entry_color: Optional[str] = None,
    exit_color: Optional[str] = None,
    pattern_42_color: Optional[str] = None,
    use_color: bool = False,
) -> str:
    """
    Create a visual ASCII representation of the maze.

    Args:
        gen: A MazeGenerator instance with a generated maze.
        path: Shortest path from find_shortest_path; used when
        show_path is True.
        show_path: If True, display the shortest path with a marker.
        wall_color: ANSI color name for walls (e.g. 'red', 'cyan').
        path_color: ANSI color name for path cells.
        entry_color: ANSI color name for the entry (S) cell.
        exit_color: ANSI color name for the exit (E) cell.
        pattern_42_color: If set, display the '42' pattern in this color.
        use_color: If True, embed ANSI escape codes for colors.

    Returns:
        String representation of the maze (with optional ANSI colors).
    """
    RESET = "\033[0m"
    DEFAULT = "\033[39m"
    _ANSI: Dict[str, str] = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "default": DEFAULT,
    }

    def ansi(name: Optional[str]) -> str:
        if not name:
            return DEFAULT
        return _ANSI.get(name, DEFAULT)

    vis_width = gen.width * 2 + 1
    vis_height = gen.height * 2 + 1
    grid = [[" " for _ in range(vis_width)] for _ in range(vis_height)]

    for row in range(gen.height):
        for col in range(gen.width):
            walls = gen.maze[(row, col)]
            vr = row * 2
            vc = col * 2

            grid[vr][vc] = "+"
            if walls & gen.NORTH:
                grid[vr][vc + 1] = "-"
            if walls & gen.WEST:
                grid[vr + 1][vc] = "|"

            if col == gen.width - 1:
                grid[vr][vc + 2] = "+"
                if walls & gen.EAST:
                    grid[vr + 1][vc + 2] = "|"

            if row == gen.height - 1:
                grid[vr + 2][vc] = "+"
                if walls & gen.SOUTH:
                    grid[vr + 2][vc + 1] = "-"
                if col == gen.width - 1:
                    grid[vr + 2][vc + 2] = "+"

    start_row = ((gen.height - 5) // 2) * 2
    start_col = ((gen.width - 7) // 2) * 2

    pattern_42 = [
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],  # Row 0
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # Row 1
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],  # Row 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],  # Row 3
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],  # Row 4
    ]

    for i in range(9):
        for j in range(13):
            row = start_row + i
            col = start_col + j
            if pattern_42[i][j] == 1:  # Cell should be locked (fully walled)
                grid[row + 1][col + 1] = chr(9608)

    pattern_cells = gen.get_42_pattern_cells()
    if pattern_42_color:
        for r, c in pattern_cells:
            grid[r * 2 + 1][c * 2 + 1] = "\u2591"

    if show_path and path:
        for r, c in get_path_cells(gen, path):
            grid[r * 2 + 1][c * 2 + 1] = "*"

    entry_row, entry_col = gen.entry[1], gen.entry[0]
    exit_row, exit_col = gen.exit[1], gen.exit[0]
    grid[entry_row * 2 + 1][entry_col * 2 + 1] = "S"
    grid[exit_row * 2 + 1][exit_col * 2 + 1] = "E"

    if not use_color:
        return "\n".join("".join(row) for row in grid)

    wc = wall_color or "white"
    pc = path_color or "green"
    ec_in = entry_color or "yellow"
    ec_out = exit_color or "yellow"

    lines: List[str] = []
    current = ""
    for row in grid:
        for ch in row:
            if ch in "+-|":
                d = ansi(wc)
            elif ch == "S":
                d = ansi(ec_in)
            elif ch == "E":
                d = ansi(ec_out)
            elif ch == "*":
                d = ansi(pc)
            elif ch == "\u2591":
                d = ansi(pattern_42_color)
            else:
                d = DEFAULT
            if d != current:
                lines.append(d)
                current = d
            lines.append(ch)
        lines.append("\n")
    lines.append(RESET)
    return "".join(lines)
