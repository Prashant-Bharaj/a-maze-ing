# A-MAZE-ING Implementation Summary

## Overview
Complete implementation of a maze generator in Python that meets all requirements from the 42 curriculum.

## ✅ Implemented Features

### 1. Core Requirements
- [x] Main program: `a_maze_ing.py`
- [x] Usage: `python3 a_maze_ing.py config.txt`
- [x] Reusable maze generation class in `maze.py`
- [x] Configuration file parsing with KEY=VALUE format
- [x] Comment support (lines starting with #)
- [x] Comprehensive error handling (no crashes)

### 2. Configuration File
- [x] Mandatory keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT
- [x] Optional keys: SEED, ALGORITHM
- [x] Default configuration file: `config.txt`
- [x] Multiple example configurations provided

### 3. Maze Generation
- [x] Random generation with reproducible seeds
- [x] Each cell has 0-4 walls (N, E, S, W)
- [x] Valid maze structure:
  - [x] Entry and exit are different and inside bounds
  - [x] Full connectivity (no isolated cells except '42' pattern)
  - [x] External borders have walls
  - [x] Coherent wall encoding between neighbors
- [x] No wide corridors (no 3x3 open areas)
- [x] Visible "42" pattern using fully closed cells
- [x] Perfect maze option (single path from entry to exit)
- [x] Imperfect maze option (multiple paths)

### 4. Output Format
- [x] Hexadecimal encoding (one digit per cell)
- [x] Wall encoding: Bit 0=North, 1=East, 2=South, 3=West
- [x] One row per line
- [x] Empty line separator
- [x] Entry coordinates (x,y format)
- [x] Exit coordinates (x,y format)
- [x] Shortest path (N/E/S/W directions)
- [x] All lines end with \n

### 5. Additional Features
- [x] Visual ASCII representation of maze (walls, S, E, path, optional 42 pattern)
- [x] Coloured terminal visualization (ANSI) with configurable wall/path/entry/exit/42 colours
- [x] Interactive visual mode: [R]egenerate, [P]ath show/hide, [C]olors, [F] 42, [A]ccent, [Q]uit
- [x] Graphical display (MiniLibX/mlx window) via `-g`/`--graphical`; path and 42 pattern highlighted. Requires: `pip install ./mlx-2.2-py3-ubuntu-any.whl` (Ubuntu only; pygame not allowed on eval)
- [x] BFS pathfinding for shortest path
- [x] Validation against provided validator script
- [x] Clear error messages for all failure cases
- [x] Console output showing maze details

## 📁 Project Structure

```
A-MAZE-ING/
├── a_maze_ing.py           # Main program (entry point)
├── maze.py                 # MazeGenerator class (reusable)
├── config.txt              # Default configuration (20x15)
├── config_small.txt        # Small maze (5x4)
├── config_large.txt        # Large maze (25x20)
├── config_imperfect.txt    # Non-perfect maze example
├── config_invalid.txt      # Invalid config for testing
├── output_maze.txt         # Generated output
├── output_validator.py     # Provided validator
├── maze_graphics.py        # MiniLibX (mlx) graphical viewer (-g/--graphical); Ubuntu only
├── test_maze.py            # Test suite
├── PROJECT_README.md       # Complete documentation
└── IMPLEMENTATION.md       # This file
```

## 🔧 Technical Implementation

### MazeGenerator Class (maze.py)

**Key Methods:**
- `__init__()`: Initialize maze with all walls closed
- `generate()`: Main generation method using DFS
- `_create_42_pattern()`: Create the '42' locked cells
- `_generate_perfect_maze_dfs()`: Recursive backtracking algorithm
- `_add_extra_paths()`: Add passages for non-perfect mazes
- `find_shortest_path()`: BFS to find optimal path
- `to_hex_string()`: Convert to hex format
- `to_output_format()`: Complete output with path
- `visualize(show_path, wall_color, path_color, ...)`: ASCII art, optional path/colours/42
- `get_path_cells()`, `get_42_pattern_cells()`: for path and "42" overlay in visualization

**Wall Encoding:**
```python
NORTH = 1  # Bit 0
EAST = 2   # Bit 1
SOUTH = 4  # Bit 2
WEST = 8   # Bit 3
```

### Main Program (a_maze_ing.py)

**Functions:**
- `parse_config_file()`: Read and parse configuration
- `validate_and_convert_config()`: Validate all parameters
- `generate_maze_from_config()`: Orchestrate generation
- `main()`: Entry point with argument handling

**Error Handling:**
- FileNotFoundError: Missing config file
- ValueError: Invalid configuration
- IOError: File write errors
- Generic Exception: Unexpected errors

## 🧪 Testing

### Test Cases
1. ✅ Default configuration (20x15, perfect)
2. ✅ Small maze (5x4, perfect) - Warning about '42' pattern
3. ✅ Large maze (25x20, perfect)
4. ✅ Imperfect maze (15x12, multiple paths)
5. ✅ Missing file error handling
6. ✅ Invalid configuration error handling
7. ✅ Validation with output_validator.py

### Validation Results
All generated mazes pass the validator with no errors:
```bash
python3 output_validator.py output_maze.txt
# No output = Success
```

## 📊 Example Outputs

### Small Maze (5x4)
```
+-+-+-+-+-+
|S  |     |
+-+ +-+-+ +
| |       |
+ +-+-+-+ +
|     |   |
+ +-+-+ +-+
|        E|
+-+-+-+-+-+
```

### Hexadecimal Output (excerpt)
```
D539553955553D517913
97C693C69553C53C56AA
8153AC55695693A9556A
...

0,0
19,14
EESENEEESENEEEEESEESSENEEENNESSSSWWWSWNWSSSENESSSWSESSESSENNNESSS
```

## 🎯 Requirements Compliance

| Requirement | Status | Notes |
|------------|--------|-------|
| Program name: a_maze_ing.py | ✅ | Correct |
| Usage: python3 a_maze_ing.py config.txt | ✅ | Correct |
| Config parsing (KEY=VALUE) | ✅ | Supports comments |
| Mandatory keys | ✅ | All validated |
| Random + reproducible | ✅ | SEED parameter |
| Wall encoding (0-4 walls) | ✅ | Hex format |
| Valid maze structure | ✅ | All checks |
| No wide corridors | ✅ | 3x3 prevention |
| '42' pattern | ✅ | With size warning |
| Perfect maze option | ✅ | Single path |
| Hex output format | ✅ | Correct encoding |
| Entry/exit/path output | ✅ | Correct format |
| Error handling | ✅ | Never crashes |
| Reusable code | ✅ | maze.py module |

## 🚀 Usage Examples

```bash
# Generate default maze
python3 a_maze_ing.py config.txt

# Generate small maze
python3 a_maze_ing.py config_small.txt

# Generate large maze with seed
python3 a_maze_ing.py config_large.txt

# Generate non-perfect maze
python3 a_maze_ing.py config_imperfect.txt

# Validate output
python3 output_validator.py output_maze.txt

# Graphical display (Ubuntu: pip install ./mlx-2.2-py3-ubuntu-any.whl first)
python3 a_maze_ing.py config.txt -g
```

## 💡 Key Design Decisions

1. **Recursive Backtracking (DFS)**: Chosen for perfect maze generation as it naturally creates a spanning tree with no cycles.

2. **'42' Pattern**: Implemented as locked cells in a 7x5 grid centered in the maze. Cells not part of the pattern remain fully walled.

3. **Wide Corridor Prevention**: Checked during passage creation to prevent 3x3 open areas.

4. **Path Finding**: BFS ensures shortest path is found and recorded.

5. **Error Handling**: Each function validates inputs and provides descriptive error messages.

6. **Modularity**: MazeGenerator class is fully reusable and independent of the CLI.

## 🔍 Edge Cases Handled

- ✅ Maze too small for '42' pattern (warning printed)
- ✅ Entry and exit at same position (error)
- ✅ Entry/exit outside bounds (error)
- ✅ Missing configuration keys (error with list)
- ✅ Invalid data types (conversion errors)
- ✅ File not found (clear message)
- ✅ No path between entry/exit (error)
- ✅ Invalid PERFECT values (boolean parsing)

## 📝 Notes

- All mazes are guaranteed to have a path from entry to exit
- The '42' pattern may affect path finding but cells remain connected
- External borders always have walls (no entry/exit on edges yet)
- The validator confirms wall consistency between all neighboring cells
- Perfect mazes have exactly one unique path (no loops)
- Imperfect mazes have additional passages creating multiple paths

## ✨ Future Enhancements (Optional)

- [ ] Additional algorithms (Prim's, Kruskal's)
- [ ] Entry/exit on maze borders (edge cells)
- [ ] Configurable '42' pattern position
- [x] Colored visualization (ANSI, interactive)
- [x] Graphical display (MiniLibX/mlx window, `-g`/`--graphical`); Ubuntu only
- [ ] Animation of generation process
- [ ] Multiple output formats (PNG, SVG)

## 🎓 Authors

Created as part of the 42 curriculum by msantos2, prasingh.

## ✅ Status: COMPLETE

All mandatory requirements implemented and tested.
