# A-MAZE-ING Maze Generator

A Python implementation of a configurable maze generator that creates perfect or imperfect mazes with hexadecimal wall encoding.

## Features

- **Configurable maze generation** via simple text configuration files
- **Perfect maze support**: Generates mazes with exactly one path from entry to exit
- **Imperfect maze support**: Generates mazes with multiple possible paths
- **Visual '42' pattern**: Automatically includes a visible "42" pattern in the maze (when size permits)
- **Hexadecimal output format**: Efficient wall encoding using 4 bits per cell
- **Reproducible results**: Optional seed parameter for deterministic generation
- **Path finding**: Automatically computes shortest path from entry to exit
- **Visual representation**: ASCII art visualization of the generated maze
- **Robust error handling**: Comprehensive validation and clear error messages

## Installation

No special installation required. The project uses only Python standard library.

```bash
# Clone or download the repository
cd A-MAZE-ING
```

## Usage

### Basic Usage

```bash
python3 a_maze_ing.py config.txt
```

### Configuration File Format

Create a text file with one `KEY=VALUE` pair per line:

```ini
# Maze dimensions
WIDTH=20
HEIGHT=15

# Entry and exit coordinates (x,y format)
ENTRY=0,0
EXIT=19,14

# Output file for the generated maze
OUTPUT_FILE=output_maze.txt

# Perfect maze flag (True = single path, False = multiple paths)
PERFECT=True

# Optional: Random seed for reproducibility
SEED=42

# Optional: Algorithm choice (currently only 'dfs' is implemented)
ALGORITHM=dfs
```

#### Mandatory Keys

- `WIDTH`: Maze width in cells (positive integer)
- `HEIGHT`: Maze height in cells (positive integer)
- `ENTRY`: Entry coordinates in format `x,y` (0-indexed)
- `EXIT`: Exit coordinates in format `x,y` (0-indexed)
- `OUTPUT_FILE`: Path to the output file
- `PERFECT`: Boolean flag (`True` or `False`)

#### Optional Keys

- `SEED`: Random seed for reproducibility (integer)
- `ALGORITHM`: Generation algorithm (default: `dfs`)

### Example Configurations

**Default maze (20x15, perfect):**
```bash
python3 a_maze_ing.py config.txt
```

**Small maze (5x4):**
```bash
python3 a_maze_ing.py config_small.txt
```

**Large maze (25x20):**
```bash
python3 a_maze_ing.py config_large.txt
```

## Output Format

The generated maze is written to the specified output file with the following format:

### Hexadecimal Wall Encoding

Each cell is represented by one hexadecimal digit (0-F), where each bit indicates a wall:

- **Bit 0 (value 1)**: North wall
- **Bit 1 (value 2)**: East wall
- **Bit 2 (value 4)**: South wall
- **Bit 3 (value 8)**: West wall

**Example:** 
- `F` (binary 1111) = all walls closed
- `3` (binary 0011) = North and East walls closed, South and West open
- `A` (binary 1010) = East and West walls closed, North and South open

### File Structure

```
DDDDDDDDDD...   (First row of maze)
DDDDDDDDDD...   (Second row)
...             (Remaining rows)
                (Empty line)
x,y             (Entry coordinates)
x,y             (Exit coordinates)
NESW...         (Shortest path: N=North, E=East, S=South, W=West)
```

## Validation

Validate the output file using the provided validator:

```bash
python3 output_validator.py output_maze.txt
```

The validator checks that neighboring cells have consistent wall encodings.

## Maze Requirements

The generated mazes satisfy the following constraints:

1. **Valid connectivity**: All cells (except locked cells for the '42' pattern) are connected
2. **Entry and exit**: Different cells within maze bounds
3. **Wall consistency**: Neighboring cells share wall states (no contradictions)
4. **External borders**: Maze has walls on all external edges
5. **No wide corridors**: Prevents corridors wider than 2 cells (no 3x3 open areas)
6. **'42' pattern**: Visible "42" drawn by fully closed cells (when maze is ≥7x5)
7. **Perfect maze option**: Exactly one path between entry and exit when PERFECT=True

## Error Handling

The program handles all common errors gracefully:

- Missing configuration file
- Invalid configuration format
- Missing mandatory keys
- Invalid parameter values
- Out-of-bounds coordinates
- Entry and exit at the same location
- File I/O errors

All errors produce clear messages and exit with non-zero status codes.

## Project Structure

```
A-MAZE-ING/
├── a_maze_ing.py          # Main program
├── maze.py                # MazeGenerator class (reusable)
├── config.txt             # Default configuration
├── config_small.txt       # Small maze example
├── config_large.txt       # Large maze example
├── output_validator.py    # Output validation script
├── README.md              # This file
└── requirements.txt       # Python dependencies (empty - uses stdlib only)
```

## Technical Details

### Algorithm

The maze generator uses **Recursive Backtracking (Depth-First Search)** to create perfect mazes:

1. Start at entry cell
2. Mark current cell as visited
3. Randomly choose an unvisited neighbor
4. Carve a passage by removing walls
5. Recursively visit the neighbor
6. Backtrack when no unvisited neighbors remain

For imperfect mazes, additional random passages are added after perfect maze generation.

### '42' Pattern

The '42' pattern is a 7x5 cell arrangement centered in the maze. Cells not part of the pattern are "locked" (kept fully walled) to create the visible shape.

If the maze is smaller than 7x5, a warning is printed and the pattern is skipped.

## Examples

### Small Perfect Maze (5x4)

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

Entry: (0,0)  
Exit: (4,3)  
Path: ESEEESWSE

### Medium Maze (20x15)

See `output_maze.txt` for the complete hexadecimal output.

## Authors

Created as part of the 42 curriculum.

## License

This project is part of educational coursework.
