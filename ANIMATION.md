# Maze Animation Features

## Overview

The maze animation system provides three types of visual animations:

1. **Maze Drawing Animation** - Draw the maze line by line
2. **Algorithm Solving Animation** - Visualize how the BFS algorithm explores the maze
3. **Combined Animation** - Draw maze and trace the solution path

## Usage

### Command Line Options

```bash
# Animate maze drawing (line by line)
python3 a_maze_ing.py config.txt --animate

# Animate pathfinding algorithm
python3 a_maze_ing.py config.txt --animate-algo

# Run interactive mode (existing feature)
python3 a_maze_ing.py config.txt --visual
```

### Demo Script

Run all animation demonstrations:

```bash
python3 demo_animations.py
```

This shows:
- Demo 1: Maze drawing animation (10x8 maze)
- Demo 2: Algorithm solving animation (8x6 maze)
- Demo 3: Combined animation (maze + path tracing)

## Features

### 1. Maze Drawing Animation (`animate_maze_drawing`)

**What it does:**
- Draws the maze structure line by line (top to bottom)
- Each row appears sequentially with a configurable delay
- Walls are colored blue, entry is green, exit is green

**Parameters:**
- `gen`: MazeGenerator instance
- `delay`: Time between each line (default: 0.02 seconds)
- `use_color`: Enable ANSI colors (default: True)

**Visual Example:**
```
+-S-+-E-+-+-+-+-+
| | |   | | | | |
+-+ +-+ +-+-+-+ +
| |         | | |
...continues line by line
```

### 2. Algorithm Solving Animation (`animate_pathfinding`)

**What it does:**
- Visualizes BFS algorithm exploring the maze
- Shows real-time exploration progress
- Displays number of explored cells and queue size
- Returns the shortest path found

**Parameters:**
- `gen`: MazeGenerator instance
- `delay`: Time between exploration steps (default: 0.05 seconds)
- `use_color`: Enable ANSI colors (default: True)

**Output:**
```
==================================================
Starting pathfinding visualization...
==================================================
Explored: 5 cells | Queue size: 3
Explored: 10 cells | Queue size: 5
...
Explored: 45 cells
Shortest path length: 67 steps
==================================================
```

### 3. Combined Animation (`animate_maze_with_path`)

**What it does:**
1. Draws the maze line by line
2. Then traces the solution path step by step
3. Path cells are highlighted with '*' symbol
4. Entry marked as 'S', exit marked as 'E'

**Parameters:**
- `gen`: MazeGenerator instance
- `path`: List of direction characters from pathfinding
- `draw_delay`: Delay for maze drawing (default: 0.02 seconds)
- `highlight_delay`: Delay for path tracing (default: 0.05 seconds)
- `use_color`: Enable ANSI colors (default: True)

**Visual Sequence:**
```
Step 1: Drawing maze structure (line by line)
Step 2: Tracing solution path (step by step)
```

## Animation Colors

| Element | Color | Code |
|---------|-------|------|
| Walls | Blue | `\033[34m` |
| Path | Green | `\033[32m` |
| Entry (S) | Yellow | `\033[33m` |
| Exit (E) | Red | `\033[31m` |
| Explored cells | Yellow | `\033[33m` |
| Frontier cells | Cyan | `\033[36m` |

## Performance Tips

- **Large mazes (>50x50)**: Use `delay=0.01` for smooth animation
- **Small delays**: Set `delay=0` to skip animation pauses
- **Algorithm animation**: Automatically updates every 5 steps for efficiency
- **Disable colors**: Set `use_color=False` for faster rendering

## Examples

### Quick maze drawing animation
```python
from maze import MazeGenerator
from maze_animate import animate_maze_drawing

gen = MazeGenerator(10, 8, (0, 0), (9, 7))
gen.generate()
animate_maze_drawing(gen, delay=0.03)
```

### Visualize solving algorithm
```python
from maze import MazeGenerator
from maze_animate import animate_pathfinding

gen = MazeGenerator(8, 6, (0, 0), (7, 5))
gen.generate()
path = animate_pathfinding(gen, delay=0.02)
print(f"Solution: {''.join(path)}")
```

### Complete animation flow
```python
from maze import MazeGenerator
from maze_animate import animate_maze_with_path
from maze_pathfinding import find_shortest_path

gen = MazeGenerator(10, 8, (0, 0), (9, 7))
gen.generate()
path = find_shortest_path(gen)
animate_maze_with_path(gen, path)
```

## Technical Details

- **Terminal Requirement**: ANSI escape code support needed for colors
- **Speed**: Animation speed depends on terminal rendering capabilities
- **Compatibility**: Works on Linux, macOS, and Windows (with ANSI enabled)
- **Algorithm**: Uses BFS (Breadth-First Search) for optimal pathfinding

## Troubleshooting

**Colors not showing?**
- Use `use_color=False` flag
- Check if terminal supports ANSI codes

**Animation too fast/slow?**
- Adjust `delay` parameter (in seconds)
- Increase for slower, decrease for faster

**Incomplete maze display?**
- Ensure terminal has enough width/height
- Try smaller maze dimensions

## Future Enhancements

Potential improvements:
- Reverse algorithm visualization (DFS, Dijkstra)
- Custom animation speeds per component
- Export animations as ASCII art files
- Different maze solving strategies visualization
