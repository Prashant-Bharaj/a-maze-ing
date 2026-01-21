# Animation Features - Quick Guide

## 🎬 Three Animation Types

### 1. **Maze Drawing Animation** 
Draw the maze structure line by line from top to bottom.

```bash
python3 a_maze_ing.py config.txt --animate
```

**What you see:**
- Walls gradually appear (blue color)
- Entry point marked as 'S'
- Exit point marked as 'E'
- Smooth line-by-line rendering

---

### 2. **Algorithm Solving Animation**
Watch the BFS algorithm explore the maze to find the shortest path.

```bash
python3 a_maze_ing.py config.txt --animate-algo
```

**What you see:**
```
==================================================
Starting pathfinding visualization...
==================================================
Explored: 5 cells | Queue size: 3
Explored: 10 cells | Queue size: 5
Explored: 45 cells
Shortest path length: 67 steps
==================================================
```

---

### 3. **Combined Animation**
Draw maze + trace the solution path step-by-step.

```bash
python3 a_maze_ing.py config.txt --animate
```

Then watch as it:
1. **STEP 1**: Draws maze structure line by line
2. **STEP 2**: Traces solution path with '*' markers

---

## 🚀 Try the Demo

See all three animations at once:

```bash
python3 demo_animations.py
```

This runs:
- **Demo 1**: Maze drawing (10x8 maze)
- **Demo 2**: Algorithm visualization (8x6 maze) 
- **Demo 3**: Combined animation (maze + path)

---

## 🎨 Color Guide

| Element | Color | Visual |
|---------|-------|--------|
| Walls | Blue | `+`, `-`, `\|` |
| Empty Space | White | (blank) |
| Solution Path | Green | `*` |
| Entry Point | Yellow | `S` |
| Exit Point | Red | `E` |

---

## ⚙️ Customization

### Change animation speed in Python code:

```python
from maze import MazeGenerator
from maze_animate import animate_maze_drawing

gen = MazeGenerator(10, 8, (0, 0), (9, 7))
gen.generate()

# Slower animation (0.1 seconds per line)
animate_maze_drawing(gen, delay=0.1)

# Faster animation (0.01 seconds per line)
animate_maze_drawing(gen, delay=0.01)

# No color (if terminal doesn't support it)
animate_maze_drawing(gen, use_color=False)
```

---

## 📊 Example Output

### Maze Drawing Animation
```
+-S-+-E-+-+-+-+-+
| | |   | | | | |
+-+ +-+ +-+-+-+ +
| |         | | |
+-+-+-+ +-+-+-+ +
| | | | | | | | |
+-+-+-+ +-+-+-+ +
|   | | | |     |
```

### Path Tracing Animation
```
+-S-*-*-+-+-+-+-+
| | |   | | | | |
+-* * * +-+-+-+ +
| |   |     | | |
+-+-+-* +-+-+-+ +
| | | | | | | | |
+-+-+-* +-+-+-+ +
|   | | | |     |
```

---

## 🔧 Performance

| Maze Size | Recommended Delay | Effect |
|-----------|-------------------|--------|
| 5x5 | 0.01s | Very fast |
| 10x10 | 0.02s | Smooth |
| 20x20 | 0.03s | Clear |
| 50x50 | 0.05s | Deliberate |
| 100x100 | 0.1s | Slow |

---

## 📝 All Commands

```bash
# Animate maze drawing
python3 a_maze_ing.py config.txt -a
python3 a_maze_ing.py config.txt --animate

# Animate algorithm solving
python3 a_maze_ing.py config.txt --animate-algo

# Interactive terminal mode (no animation)
python3 a_maze_ing.py config.txt -v
python3 a_maze_ing.py config.txt --visual

# Demo all animations
python3 demo_animations.py

# Normal generation (no animation)
python3 a_maze_ing.py config.txt
```

---

## 📚 Full Documentation

For more details, see:
- `ANIMATION.md` - Complete technical guide
- `maze_animate.py` - Source code with docstrings

---

## 💡 Tips

✅ Start with small mazes (8x8) to see animations clearly
✅ Use `--animate-algo` on medium-sized mazes (15x15)
✅ Increase delay if animation appears jerky
✅ Use `demo_animations.py` to see all features at once

---

## 🎯 What to Expect

Each animation:
- **Maze Drawing**: Complete in 1-3 seconds
- **Algorithm Solving**: Complete in 2-5 seconds  
- **Combined**: Complete in 3-8 seconds (depending on maze size)

---

Enjoy the maze animations! 🎬✨
