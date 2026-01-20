#!/usr/bin/env python3

import random

WIDTH = 10
HEIGHT = 10
SEED = 42
random.seed(SEED)

""" Every cell has walls on all four sides initially.
The maze must be written in the output file using one hexadecimal digit per cell
A wall being closed sets the bit to 1, open means the 0
Bit 0 (1): Wall to the north (1 if closed, 0 if open)
Bit 1 (2): Wall to the east (1 if closed, 0 if open)
Bit 2 (4): Wall to the south (1 if closed, 0 if open)
Bit 3 (8): Wall to the west (1 if closed, 0 if open)
"""

INITIAL_WALLS = 15

maze = {}
for r in range(HEIGHT):
    for c in range(WIDTH):
        maze[(r, c)] = INITIAL_WALLS

def print_maze(maze):
    for r in range(HEIGHT):
        for c in range(WIDTH):
            print(hex(maze[(r, c)])[2:], end='')
        print()

def carve_passages_from(r, c):
    WEST_WALL = 8
    SOUTH_WALL = 4
    EAST_WALL = 2
    NORTH_WALL = 1

    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    random.shuffle(directions)
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < HEIGHT and 0 <= nc < WIDTH and maze[(nr, nc)] == INITIAL_WALLS:
            if dr == 0 and dc == -1:  # West
                maze[(r, c)] &= ~WEST_WALL
                maze[(nr, nc)] &= ~EAST_WALL
            elif dr == 1 and dc == 0:  # South
                maze[(r, c)] &= ~SOUTH_WALL
                maze[(nr, nc)] &= ~NORTH_WALL
            elif dr == 0 and dc == 1:  # East
                maze[(r, c)] &= ~EAST_WALL
                maze[(nr, nc)] &= ~WEST_WALL
            elif dr == -1 and dc == 0:  # North
                maze[(r, c)] &= ~NORTH_WALL
                maze[(nr, nc)] &= ~SOUTH_WALL

            carve_passages_from(nr, nc)

carve_passages_from(0, 0)
print_maze(maze)