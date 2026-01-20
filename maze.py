#!/usr/bin/env python3

import random
from typing import Any, List, Dict, Union, Optional


WIDTH = 30
HEIGHT = 30
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

forty_two_sign = [1, 2, 3,
                  8, 9, 10, 11, 12,
                  17,
                  21, 22, 24, 26, 27,
                  28, 29, 31]
locked_cells = []
maze = {}

for r in range(HEIGHT):
    for c in range(WIDTH):
        maze[(r, c)] = INITIAL_WALLS

def print_maze(maze):
    for r in range(HEIGHT):
        for c in range(WIDTH):
                s = str(hex(maze[(r, c)])[2:])
                #if (s != 'f'):
                #    s = ' '
                print(s, end='')

        print()

def check_42() -> bool:
    count = 0
    x = int(HEIGHT / 2) - 3

    for _ in range(5):
        y = int(WIDTH / 2) - 4
        for _ in range (7):
            if count not in forty_two_sign:
                locked_cells.append((x, y))
            count += 1
            y += 1
        x += 1

def open_walls(r, c):
    WEST_WALL = 8
    SOUTH_WALL = 4
    EAST_WALL = 2
    NORTH_WALL = 1

    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    random.shuffle(directions)
    for dir_row, dir_column in directions:
        new_row, new_column = r + dir_row, c + dir_column
        if 0 <= new_row < HEIGHT and 0 <= new_column < WIDTH and maze[(new_row, new_column)] == INITIAL_WALLS and (new_row, new_column) not in locked_cells:
            if dir_row == 0 and dir_column == -1:  # West
                maze[(r, c)] &= ~WEST_WALL
                maze[(new_row, new_column)] &= ~EAST_WALL
            elif dir_row == 1 and dir_column == 0:  # South
                maze[(r, c)] &= ~SOUTH_WALL
                maze[(new_row, new_column)] &= ~NORTH_WALL
            elif dir_row == 0 and dir_column == 1:  # East
                maze[(r, c)] &= ~EAST_WALL
                maze[(new_row, new_column)] &= ~WEST_WALL
            elif dir_row == -1 and dir_column == 0:  # North
                maze[(r, c)] &= ~NORTH_WALL
                maze[(new_row, new_column)] &= ~SOUTH_WALL
            # print_maze(maze)
            # print("\n\n")
            open_walls(new_row, new_column)

check_42()
open_walls(0, 0)
print_maze(maze)