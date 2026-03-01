# A-Maze-ing — Project Requirements

> Derived from the project specification. Written in our own words for reference.

---

## 1. General Code Standards

- **Language**: Python 3.10 or later.
- **Style**: Must comply with `flake8` coding standard throughout.
- **Exception handling**: All functions must handle exceptions gracefully using `try-except`. Programs must never crash unexpectedly; always emit a clear error message.
- **Resource management**: Use context managers (`with` statements) for file handles and other resources to prevent leaks.
- **Type hints**: All function parameters, return types, and variables must carry type hints (using the `typing` module). Code must pass `mypy` without errors.
- **Docstrings**: Every function and class must have a docstring following PEP 257 (Google or NumPy style), documenting purpose, parameters, and return values.

---

## 2. Makefile

A `Makefile` must be present at the repo root with the following rules:

| Rule | Purpose |
|------|---------|
| `install` | Install project dependencies (via `pip`, `uv`, `pipx`, etc.) |
| `run` | Execute the main script |
| `debug` | Run the main script under Python's built-in debugger (`pdb`) |
| `clean` | Remove temporary files and caches (`__pycache__`, `.mypy_cache`, etc.) |
| `lint` | Run `flake8 .` **and** `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs` |
| `lint-strict` *(optional)* | Run `flake8 .` and `mypy . --strict` |

---

## 3. Additional Development Guidelines

- A `.gitignore` must exclude Python artifacts.
- Test programs should be written using `pytest` or `unittest` (not submitted or graded).
- Virtual environments (`venv`, `conda`) are recommended for dependency isolation.

---

## 4. Program Usage

```
python3 a_maze_ing.py config.txt
```

- The main entry point **must** be named `a_maze_ing.py`.
- It accepts exactly one argument: the path to a configuration file.
- All errors (missing file, invalid config, impossible parameters, etc.) must be handled gracefully with a clear message — no uncaught exceptions.

---

## 5. Configuration File Format

- One `KEY=VALUE` pair per line.
- Lines beginning with `#` are comments and must be ignored.

### Mandatory keys

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | Entry cell coordinates `x,y` | `ENTRY=0,0` |
| `EXIT` | Exit cell coordinates `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether the maze is perfect | `PERFECT=True` |

Optional keys (e.g., `SEED`, `ALGORITHM`, display mode) may be added as needed.

A default `config.txt` must be committed to the repository.

---

## 6. Maze Requirements

- **Randomised with seed**: The maze must be randomly generated but fully reproducible when the same seed is supplied.
- **Cell walls**: Each cell has 0–4 walls (North, East, South, West).
- **Validity**:
  - Entry and exit must be distinct cells inside the maze bounds.
  - The maze must be fully connected — no isolated cells (except the "42" pattern, see below).
  - External border cells must have walls on their outer edges except at the entry/exit openings.
  - Wall data must be coherent: if cell A has a wall on its East side, the neighbouring cell B must have a wall on its West side.
- **No large open areas**: Corridors cannot be wider than 2 cells. A 2×3 or 3×2 open area is allowed; a 3×3 open area is not.
- **"42" pattern**: The visual representation must contain a visible "42" formed by several fully-walled (closed) cells. If the maze is too small to include the pattern, print an error message on the console and omit it.
- **Perfect maze** (when `PERFECT=True`): Exactly one path must exist between entry and exit.

---

## 7. Output File Format

Each cell is encoded as a single hexadecimal digit where the bits indicate closed walls:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

- Bit = `1` → wall is **closed**; bit = `0` → wall is **open**.
- Example: `3` (binary `0011`) = North and East walls closed. `A` (binary `1010`) = East and West walls closed.
- Cells are written row by row, one row per line.
- After a blank line, three additional lines are appended:
  1. Entry coordinates (e.g., `1,1`)
  2. Exit coordinates (e.g., `19,14`)
  3. Shortest valid path from entry to exit using the letters `N`, `E`, `S`, `W`.
- Every line ends with `\n`.

---

## 8. Visual Representation

The program must display the maze visually using **at least one** of:

- Terminal ASCII rendering
- Graphical display via the MiniLibX (MLX) library

The display must clearly show walls, the entry cell, the exit cell, and the solution path.

### Required user interactions

| Action | Description |
|--------|-------------|
| Re-generate | Generate a new maze and display it |
| Show/Hide path | Toggle display of the shortest path from entry to exit |
| Change wall colour | Cycle or set maze wall colours |
| *(Optional)* Highlight "42" | Set a distinct colour for the "42" pattern cells |

Additional interactions may be added freely.

---

## 9. Code Reusability — `mazegen` Package

- The maze generation logic must be implemented as a single class (e.g., `MazeGenerator`) inside a standalone importable module.
- The module must be packaged as a pip-installable package named `mazegen-*` (`.whl` or `.tar.gz`), located at the repository root.
  - Example filename: `mazegen-1.0.0-py3-none-any.whl`
- All source files needed to **rebuild** the package must be committed to the repository.
- The package must expose at minimum:
  - How to instantiate and use the generator (with a basic example).
  - How to pass custom parameters (size, seed, etc.).
  - How to access the generated maze structure and a solution path.
- Note: the internal maze structure exposed by the module does not need to match the hex output file format.

---

## 10. README Requirements

The root `README.md` must include:

- **First line** (italicised): `This project has been created as part of the 42 curriculum by <login1>[, <login2>[, ...]]`.
- **Description** section: project goal and brief overview.
- **Instructions** section: installation, compilation, and execution steps.
- **Resources** section: references (docs, articles, tutorials) and a description of how AI was used (which tasks, which parts of the project).
- Config file structure and format (complete).
- The maze generation algorithm chosen and the reason for choosing it.
- What part of the code is reusable and how to use it (mirrors the `mazegen` package documentation).
- Team and project management:
  - Roles of each team member.
  - Anticipated planning and how it evolved.
  - What worked well and what could be improved.
  - Tools used.
- If advanced features are implemented (multiple algorithms, display options), describe them.

---

## 11. Bonuses

Optional enhancements that can earn bonus points:

- Support multiple maze generation algorithms.
- Add animation during maze generation.

---

## 12. Submission

- Submit via the Git repository. Only committed work is evaluated.
- During peer-evaluation, a **brief live modification** of the project may be requested (minor behaviour change, a few lines of code, or a small feature). Be prepared to demonstrate real understanding of the code.
