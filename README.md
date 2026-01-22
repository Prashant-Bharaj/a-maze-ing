*This project has been created as part of the 42 curriculum by prasingh, msantos2.*

# A-MAZE-ING

## Description

A-Maze-ing is a Python project that generates random mazes based on a configuration file.
The program supports both perfect and non-perfect mazes, produces a hexadecimal wall representation as output, computes the shortest path between entry and exit, and provides a terminal-based visual representation with optional animation.

The project is designed with code reusability in mind: the maze generation (`mazegen`) logic is implemented as a standalone Python package that can be reused in future projects.

---

## mazegen

Reusable maze generator providing a single-module `MazeGenerator` class plus solution extraction.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .
```

## Example
```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=8, height=6, seed=42)
print(gen.to_hex_string())
hex grid lines
print(gen.solution_path)     
```

## Build wheel / sdist
```bash
source .venv/bin/activate
pip install --upgrade build
python -m build
ls dist
```

## Format details
- Grid stored as 2D list of ints; bits mark openings (N=1, E=2, S=4, W=8).
- `to_hex_string()` returns newline-separated hex digits per row; matches the validator format.
- `solution_path` gives the shortest path from `start` to `goal` using carved passages.

## Instructions

### Compilation

Install project dependencies

```bash
make install
```
Execute the main script of your project 
```bash
make run
```
Run the main script in debug mode using Python’s built-in debugger
```bash
make debug
```

Remove temporary files or caches (e.g., `__pycache__`, .`mypy_cache`) to keep the project environment clean.
 ```bash
make clean
```
Execute the commands flake8 . and mypy
 ```bash
make lint
```
Execute the commands flake8 . and mypy . --strict
 ```bash
make lint-strict
```

#### Running flake8 and MyPy

Mypy is an optional static type checker for Python that aims to combine the benefits of **dynamic typing** and **static typing**.

Mypy requires `Python 3.9` or later to run. You can install `mypy` using `pip`:
```bash
python3 -m pip install mypy
```

Flake8 is a Python tool that combines three code analysis utilities: `PyFlakes` (for syntax and logical errors), `pycodestyle` (formerly pep8, for PEP 8 style compliance), and `McCabe` (for measuring code complexity)—into a single command-line interface.

It helps enforce coding standards, detect style violations, identify potential bugs, and flag overly complex code blocks.

To install `Flake8`, use `pip` with the correct `Python` version:
 ```bash
python -m pip install flake8   
```

Once `mypy` and `flake8` are installed, you can execute using
 ```bash
make lint
```
Execute the commands `flake8` and `mypy` --strict
```bash
make lint-strict
```

### Execution

Run the main program with a configuration file:
```bash
python3 a_maze_ing.py config.txt
```

- -v        Run interactive terminal visual mode
- -a        Animate maze generation

### Configuration File Format

The configuration file is a plain text file containing one `KEY=VALUE` pair per line.
Lines starting with `#` are ignored.
```bash
WIDTH=number           Maze width in cells
HEIGHT=number          Maze height in cells
ENTRY=x,y              Entry coordinates
EXIT=x,y               Exit coordinates
OUTPUT_FILE=path       Output file path
PERFECT=True or False  Perfect maze flag
SEED=number            Random seed for reproducibility
ALGORITHM=dfs, kruskal or prim         
```

## Maze Generation Algorithm

The maze is generated using the Recursive Backtracker algorithm, a randomized
depth-first search (DFS) approach.

### How it works

The maze grid starts with all walls closed.

A random starting cell is chosen.

The algorithm visits unvisited neighboring cells, removing walls as it progresses.

Backtracking occurs when no unvisited neighbors remain.

Each cell is visited exactly once.

### Why this algorithm was chosen

Guarantees full connectivity of the maze

Naturally produces perfect mazes (single path between any two cells)

Simple, efficient, and easy to reason about

Well suited for reproducibility using a random seed

For non-perfect mazes, additional walls are removed after generation to introduce cycles and multiple paths.

### Output Format

The generated maze is written to the output file using one hexadecimal digit per cell.
Each digit encodes which walls are closed (North, East, South, West).

After the maze grid, the file includes:

- Entry coordinates
- Exit coordinates
- The shortest valid path from entry to exit (N, E, S, W)

### Reusable Code

The maze generation logic is implemented as a standalone Python package named `mazegen`.

The package provides:

- A MazeGenerator class
- Maze generation with configurable size, seed, and perfection
- Access to the internal maze structure
- The package can be installed via pip and reused independently of the main program.

### Visualization

The project includes a terminal-based ASCII visualization with support for:
- Regenerating mazes
- Showing or hiding the solution path
- Changing wall colors
- Optional animation of maze generation and pathfinding

## Team and Project Management

### Team

msantos2 and prasingh

### Planning and evolution

The project was developed incrementally:

- Maze data model and wall representation
- Maze generation algorithm
- Pathfinding (BFS)
- Output encoding and validation
- Visualization and interaction
- Packaging and documentation

### What worked well
- Clear separation between generation logic and application code
- Early focus on correctness and constraints
- Reusable architecture

### What could be improved
- Implementation of a graphical display using the MiniLibX

### Tools used
- Python 3.10
- flake8
- mypy
- pip / virtual environments
- AI tools for explanations, refactoring guidance, and documentation support

## Resources

- For the creation of virtual environment:[link](https://docs.python.org/3/library/venv.html)
- For the study of the python modules:[link](https://docs.python.org/3/tutorial/modules.html)
- For git conflict resolution:[link](https://stackoverflow.com/questions/51274430/change-from-master-to-a-new-default-branch-git)
- Recursive algorithm that solves mazes and generates mazes: [Link](https://inventwithpython.com/recursion/chapter11.html)
- Python’s Path Through Mazes: A Journey of Creation and Solution[Link](https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96)

### AI Usage:
* AI is used for the understanding the problem, and specifics
* Creating the requirements list for the project
* Writing custom test scripts for the verification of implementation
* Brainstorming the approach for the animation and visualize 
