#!/usr/bin/env python3
"""
Animation module for maze drawing and algorithm solving visualization.
Supports line-by-line maze drawing animation and step-by-step pathfinding visualization.
"""

import time
import sys
from typing import Dict, List, Optional, Set, Tuple, TYPE_CHECKING
from collections import deque

from maze_visualize import visualize

if TYPE_CHECKING:
    from mazegen import MazeGenerator


def _clear_screen() -> None:
    """Clear the terminal screen."""
    print("\033[2J\033[H", end="", flush=True)


def _move_cursor_up(lines: int) -> None:
    """Move cursor up by specified number of lines."""
    print(f"\033[{lines}A", end="", flush=True)


def animate_maze_drawing(
    gen: "MazeGenerator",
    delay: float = 0.06,
    use_color: bool = True,
) -> None:
    """
    Animate drawing the maze line by line (row by row).

    Args:
        gen: A MazeGenerator instance with a generated maze.
        delay: Delay in seconds between each line.
        use_color: If True, use ANSI color codes.
    """
    RESET = "\033[0m"
    WALL_COLOR = "\033[34m"  # Blue for walls
    EMPTY_COLOR = "\033[37m"  # White for empty space

    vis_width = gen.width * 2 + 1
    vis_height = gen.height * 2 + 1
    grid = [[" " for _ in range(vis_width)] for _ in range(vis_height)]

    # Build grid
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
                    if walls & gen.SOUTH:
                        grid[vr + 2][vc + 1] = "-"
                    if walls & gen.EAST:
                        grid[vr + 1][vc + 2] = "|"

    # Mark entry and exit in cell interiors (not corners)
    entry_vr = gen.entry[1] * 2 + 1
    entry_vc = gen.entry[0] * 2 + 1
    grid[entry_vr][entry_vc] = "S"

    exit_vr = gen.exit[1] * 2 + 1
    exit_vc = gen.exit[0] * 2 + 1
    grid[exit_vr][exit_vc] = "E"

    _clear_screen()

    # Animate line by line
    for vr in range(vis_height):
        line = ""
        for vc in range(vis_width):
            char = grid[vr][vc]
            if use_color:
                if char in "+-|":
                    line += f"{WALL_COLOR}{char}{RESET}"
                elif char in "SE":
                    line += f"\033[32m{char}{RESET}"  # Green for entry/exit
                else:
                    line += char
            else:
                line += char
        print(line)
        time.sleep(delay)


def animate_pathfinding(
    gen: "MazeGenerator",
    delay: float = 0.08,
    use_color: bool = True,
) -> List[str]:
    """
    Animate BFS pathfinding algorithm showing exploration step by step.
    Displays explored cells, current frontier, and final path.

    Args:
        gen: A MazeGenerator instance with a generated maze.
        delay: Delay in seconds between each step.
        use_color: If True, use ANSI color codes.

    Returns:
        List of direction characters representing the shortest path.
    """
    RESET = "\033[0m"
    WALL_COLOR = "\033[34m"  # Blue
    EMPTY_COLOR = "\033[37m"  # White
    EXPLORED_COLOR = "\033[33m"  # Yellow
    FRONTIER_COLOR = "\033[36m"  # Cyan
    PATH_COLOR = "\033[32m"  # Green
    FOURTY_TWO_COLOR = "\033[33M"  # Yellow

    entry_row, entry_col = gen.entry[1], gen.entry[0]
    exit_row, exit_col = gen.exit[1], gen.exit[0]

    queue: deque = deque([(entry_row, entry_col, [])])
    visited: Set[Tuple[int, int]] = {(entry_row, entry_col)}
    exploration_order: List[Tuple[int, int]] = [(entry_row, entry_col)]
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {}

    print("\n" + "=" * 50)
    print("Starting pathfinding visualization...")
    print("=" * 50)
    time.sleep(1)

    step = 0
    final_path = []

    while queue:
        row, col, path = queue.popleft()

        if row == exit_row and col == exit_col:
            final_path = path
            break

        for direction, (dr, dc) in gen.DIRECTIONS.items():
            _, wall_mask, _ = gen.OPPOSITE[direction]
            if gen.maze[(row, col)] & wall_mask:
                continue

            new_row, new_col = row + dr, col + dc

            if not (0 <= new_row < gen.height and 0 <= new_col < gen.width):
                continue
            if (new_row, new_col) in visited:
                continue

            visited.add((new_row, new_col))
            exploration_order.append((new_row, new_col))
            parent[(new_row, new_col)] = (row, col)
            queue.append((new_row, new_col, path + [direction]))

            step += 1
            if step % 5 == 0:  # Print status every 5 steps
                print(f"Explored: {step} cells | Queue size: {len(queue)}", end="\r")
            time.sleep(delay)

    print(f"\nExplored: {len(visited)} cells")
    print(f"Shortest path length: {len(final_path)} steps")
    print("=" * 50 + "\n")

    return final_path


def animate_maze_with_path(
    gen: "MazeGenerator",
    path: List[str],
    draw_delay: float = 0.05,
    highlight_delay: float = 0.08,
    use_color: bool = True,
) -> None:
    """
    First animate drawing the maze, then animate highlighting the solution path.

    Args:
        gen: A MazeGenerator instance with a generated maze.
        path: List of direction characters representing the shortest path.
        draw_delay: Delay for maze drawing animation.
        highlight_delay: Delay for path highlighting animation.
        use_color: If True, use ANSI color codes.
    """
    # First, draw the maze
    print("STEP 1: Drawing maze structure...")
    time.sleep(1)
    animate_maze_drawing(gen, delay=draw_delay, use_color=use_color)

    time.sleep(1)

    # Build the maze visual
    vis_width = gen.width * 2 + 1
    vis_height = gen.height * 2 + 1
    grid = [[" " for _ in range(vis_width)] for _ in range(vis_height)]

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
    RESET = "\033[0m"
    WALL_COLOR = "\033[34m"
    for i in range(9):
        for j in range(13):
            row = start_row + i
            col = start_col + j
            if pattern_42[i][j] == 1:  # Cell should be locked (fully walled)
                grid[row + 1][col + 1] = f"{WALL_COLOR}{chr(9608)}{RESET}"

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

    # Mark start and end points in cell interiors (not corners)
    entry_vr = gen.entry[1] * 2 + 1
    entry_vc = gen.entry[0] * 2 + 1
    grid[entry_vr][entry_vc] = "S"

    exit_vr = gen.exit[1] * 2 + 1
    exit_vc = gen.exit[0] * 2 + 1
    grid[exit_vr][exit_vc] = "E"

    # Display start and end before path animation
    RESET = "\033[0m"
    WALL_COLOR = "\033[34m"  # Blue for walls
    PATH_COLOR = "\033[32m"  # Green for path
    ENTRY_COLOR = "\033[33m"  # Yellow
    EXIT_COLOR = "\033[31m"  # Red

    _clear_screen()
    for r in range(vis_height):
        line = ""
        for c in range(vis_width):
            char = grid[r][c]
            if use_color:
                if char in "+-|":
                    line += f"{WALL_COLOR}{char}{RESET}"
                elif char == "S":
                    line += f"{ENTRY_COLOR}{char}{RESET}"
                elif char == "E":
                    line += f"{EXIT_COLOR}{char}{RESET}"
                else:
                    line += char
            else:
                line += char
        print(line)

    print("\nSTEP 2: Tracing solution path...")
    time.sleep(2)

    # Trace the path from entry
    current_row, current_col = gen.entry[1], gen.entry[0]
    path_cells = [(current_row, current_col)]

    for direction in path:
        dr, dc = gen.DIRECTIONS[direction]
        current_row += dr
        current_col += dc
        path_cells.append((current_row, current_col))

    # Animate path highlighting
    for idx, (row, col) in enumerate(path_cells):
        if idx == 0 or idx == len(path_cells) - 1:
            continue  # Skip start and end as they're already marked

        # Mark path in cell interior (not corner)
        vr = row * 2 + 1
        vc = col * 2 + 1
        grid[vr][vc] = "*"

        # Redraw entire maze
        _clear_screen()
        for r in range(vis_height):
            line = ""
            for c in range(vis_width):
                char = grid[r][c]
                if use_color:
                    if char in "+-|":
                        line += f"{WALL_COLOR}{char}{RESET}"
                    elif char == "S":
                        line += f"{ENTRY_COLOR}{char}{RESET}"
                    elif char == "E":
                        line += f"{EXIT_COLOR}{char}{RESET}"
                    elif char == "*":
                        line += f"{PATH_COLOR}{char}{RESET}"
                    else:
                        line += char
                else:
                    line += char
            print(line)

        time.sleep(highlight_delay)

    print("\nPath trace complete!")
