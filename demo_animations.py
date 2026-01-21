#!/usr/bin/env python3
"""
Demo script to showcase maze animations.
Run this to see:
1. Maze drawing animation
2. Algorithm solving animation
3. Combined maze + path animation
"""

import sys
import time
from maze import MazeGenerator
from maze_animate import (
    animate_maze_drawing,
    animate_pathfinding,
    animate_maze_with_path,
)
from maze_pathfinding import find_shortest_path


def demo_1_maze_drawing():
    """Demo 1: Animate maze drawing line by line."""
    print("\n" + "="*60)
    print("DEMO 1: Maze Drawing Animation")
    print("="*60)
    print("Drawing a 10x8 maze line by line...\n")
    time.sleep(2)

    gen = MazeGenerator(10, 8, (0, 0), (9, 7), perfect=True, seed=42)
    gen.generate()

    animate_maze_drawing(gen, delay=0.03, use_color=True)

    time.sleep(2)
    print("\n" + "="*60)
    print("Demo 1 complete!")
    print("="*60)


def demo_2_algorithm():
    """Demo 2: Animate pathfinding algorithm."""
    print("\n" + "="*60)
    print("DEMO 2: Algorithm Solving Animation")
    print("="*60)
    print("Visualizing BFS algorithm solving the maze...\n")
    time.sleep(2)

    gen = MazeGenerator(8, 6, (0, 0), (7, 5), perfect=True, seed=123)
    gen.generate()

    path = animate_pathfinding(gen, delay=0.01, use_color=True)

    print(f"Found path with {len(path)} steps: {''.join(path)}")
    time.sleep(2)


def demo_3_combined():
    """Demo 3: Draw maze then trace solution path."""
    print("\n" + "="*60)
    print("DEMO 3: Combined Animation (Maze + Solution)")
    print("="*60)
    print("Drawing maze and then tracing the solution...\n")
    time.sleep(2)

    gen = MazeGenerator(8, 6, (1, 0), (7, 5), perfect=True, seed=99)
    gen.generate()
    path = find_shortest_path(gen)

    animate_maze_with_path(gen, path, draw_delay=0.03, highlight_delay=0.08)
    time.sleep(2)


def main():
    """Run all animation demos."""
    print("\n" + "="*60)
    print("MAZE ANIMATION DEMOS")
    print("="*60)

    demo_1_maze_drawing()
    time.sleep(1)
    demo_2_algorithm()
    time.sleep(1)
    demo_3_combined()

    print("\n" + "="*60)
    print("All demos complete!")
    print("="*60)


if __name__ == "__main__":
    main()
