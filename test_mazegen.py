#!/usr/bin/env python3
"""
Comprehensive test and demonstration of the mazegen package.
This script shows all features and capabilities of the MazeGenerator class.
"""

from mazegen import MazeGenerator


def main():
    print("=" * 70)
    print("MazeGen Package - Comprehensive Feature Demonstration")
    print("=" * 70)
    print()

    # Test 1: Basic maze generation
    print("1. Basic Maze Generation")
    print("-" * 70)
    gen = MazeGenerator(width=8, height=6, seed=42)
    gen.generate()
    print(f"   Generated {gen.width}x{gen.height} maze")
    print(f"   Entry: {gen.entry}, Exit: {gen.exit}")
    print(f"   Perfect maze: {gen.perfect}")
    print()

    # Test 2: Custom parameters
    print("2. Custom Parameters")
    print("-" * 70)
    gen_custom = MazeGenerator(
        width=12, height=10, entry=(0, 0), exit=(11, 9), perfect=False, seed=123
    )
    gen_custom.generate()
    print(f"   Custom maze: {gen_custom.width}x{gen_custom.height}")
    print(f"   Entry: {gen_custom.entry}, Exit: {gen_custom.exit}")
    print(f"   Perfect: {gen_custom.perfect}")
    print()

    # Test 3: Hex string output
    print("3. Hexadecimal Format Output")
    print("-" * 70)
    small_gen = MazeGenerator(width=5, height=4, seed=100).generate()
    hex_output = small_gen.to_hex_string()
    print("   Maze in hex format:")
    for i, line in enumerate(hex_output.split("\n")):
        print(f"   Row {i}: {line}")
    print()

    # Test 4: Solution path as coordinates
    print("4. Solution Path (Coordinates)")
    print("-" * 70)
    solution_coords = small_gen.solution_path
    print(f"   Solution has {len(solution_coords)} cells:")
    print(f"   Start: {solution_coords[0]}")
    print(f"   End: {solution_coords[-1]}")
    print(f"   First 5 cells: {solution_coords[:5]}")
    print()

    # Test 5: Solution path as directions
    print("5. Solution Path (Directions)")
    print("-" * 70)
    solution_dirs = small_gen.get_solution_directions()
    print(f"   Direction string: {solution_dirs}")
    print(f"   Length: {len(solution_dirs)} moves")
    print()

    # Test 6: 2D grid format
    print("6. 2D Grid Format")
    print("-" * 70)
    grid = small_gen.get_maze_grid()
    print(f"   Grid dimensions: {len(grid)}x{len(grid[0])}")
    print(f"   Top-left cell value: {grid[0][0]} (0x{grid[0][0]:X})")
    print(f"   Top-right cell value: {grid[0][-1]} (0x{grid[0][-1]:X})")
    print()

    # Test 7: Wall checking
    print("7. Individual Wall Checking")
    print("-" * 70)
    print(f"   Cell (0,0) - North wall: {small_gen.has_wall(0, 0, 'N')}")
    print(f"   Cell (0,0) - East wall: {small_gen.has_wall(0, 0, 'E')}")
    print(f"   Cell (0,0) - South wall: {small_gen.has_wall(0, 0, 'S')}")
    print(f"   Cell (0,0) - West wall: {small_gen.has_wall(0, 0, 'W')}")
    print()

    # Test 8: Method chaining
    print("8. Method Chaining")
    print("-" * 70)
    chained = MazeGenerator(width=6, height=5, seed=999).generate()
    print(f"   Created and generated in one line")
    print(f"   Solution length: {len(chained.solution_path)} steps")
    print()

    # Test 9: Reproducibility with seed
    print("9. Reproducibility with Seed")
    print("-" * 70)
    maze1 = MazeGenerator(width=5, height=5, seed=42).generate()
    maze2 = MazeGenerator(width=5, height=5, seed=42).generate()
    hex1 = maze1.to_hex_string()
    hex2 = maze2.to_hex_string()
    print(f"   Same seed produces identical mazes: {hex1 == hex2}")
    print()

    # Test 10: Visual representation
    print("10. Visual Maze Example")
    print("-" * 70)
    visual_gen = MazeGenerator(width=10, height=7, seed=777).generate()
    print(f"   {visual_gen.width}x{visual_gen.height} Maze (hex format):")
    print()
    for i, line in enumerate(visual_gen.to_hex_string().split("\n")):
        print(f"   {line}")
    print()
    print(f"   Solution: {visual_gen.get_solution_directions()}")
    print(f"   Path length: {len(visual_gen.solution_path)} cells")
    print()

    print("=" * 70)
    print("All tests completed successfully! ✓")
    print("=" * 70)


if __name__ == "__main__":
    main()
