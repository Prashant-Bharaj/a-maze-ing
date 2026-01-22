*This project has been created as part of the 42 curriculum by prasingh, msantos2.*

# MazeGen Package Information

## Package Overview

- **Name**: mazegen
- **Version**: 1.0.0
- **Type**: Single-module Python package
- **Format**: Both .whl (wheel) and .tar.gz (source distribution)

## Files in Repository

### Core Package Files
- `mazegen.py` - Single-file reusable module with MazeGenerator class
- `pyproject.toml` - Package configuration and metadata
- `mazegen-1.0.0-py3-none-any.whl` - Built wheel package (in root)

### Distribution Files (dist/)
- `mazegen-1.0.0-py3-none-any.whl` - Wheel distribution
- `mazegen-1.0.0.tar.gz` - Source distribution

### Documentation
- `README.md` - Comprehensive documentation with examples
- `build_package.sh` - Build script for rebuilding from source

## Building the Package

### Method 1: Using make
```bash
make package
```

### Method 2: Using build script
```bash
./build_package.sh
```

### Method 3: Manual build
```bash
source .venv/bin/activate
pip install --upgrade build
python -m build
```

## Installing the Package

### From wheel file
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### From source
```bash
pip install .
```

### From tar.gz
```bash
pip install dist/mazegen-1.0.0.tar.gz
```

## Package Features

### MazeGenerator Class
- Configurable width and height
- Custom entry and exit points
- Perfect or imperfect maze generation
- Reproducible with seed parameter

### Output Formats
- 2D grid (list of lists)
- Hexadecimal string format
- Individual wall checking
- Solution path as coordinates or directions

### Documentation Included
- Instantiation examples
- Parameter customization
- Structure access methods
- Solution retrieval methods

## Quick Example

```python
from mazegen import MazeGenerator

# Create and generate maze
gen = MazeGenerator(width=10, height=8, seed=42).generate()

# Access maze data
print(gen.to_hex_string())          # Hex format
print(gen.solution_path)            # List of (row, col) coordinates
print(gen.get_solution_directions())  # Direction string

# Check individual walls
has_wall = gen.has_wall(0, 0, 'N')
```
