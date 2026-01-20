# mazegen

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
print(gen.to_hex_string())   # hex grid lines
print(gen.solution_path)     # list of (row, col)
```

## Build wheel / sdist
```bash
source .venv/bin/activate
pip install --upgrade build
python -m build
ls dist  # contains mazegen-<version>-py3-none-any.whl and .tar.gz
```

## Format details
- Grid stored as 2D list of ints; bits mark openings (N=1, E=2, S=4, W=8).
- `to_hex_string()` returns newline-separated hex digits per row; matches the validator format.
- `solution_path` gives the shortest path from `start` to `goal` using carved passages.
