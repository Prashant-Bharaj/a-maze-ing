*This project has been created as part of the 42 curriculum by prasingh, msantos2.*

# A-MAZE-ING

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

## Description

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

#### Resources

For the creation of virtual environment:[link](https://docs.python.org/3/library/venv.html)
For the study of the python modules:[link](https://docs.python.org/3/tutorial/modules.html)
For git conflict resolution:[link](https://stackoverflow.com/questions/51274430/change-from-master-to-a-new-default-branch-git)

### AI Usage:
* AI is used for the understanding the problem, and specifics
* Creating the requirements list for the project
* Writing custom test scripts for the verification of implementation
* Brainstorming the approach for the animation and visualize 
