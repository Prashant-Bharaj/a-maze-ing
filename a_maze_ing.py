#!/usr/bin/env python3
"""
A-MAZE-ING Maze Generator
Generates a maze from a configuration file and outputs it in hexadecimal format.
Supports interactive visual mode with: regenerate, show/hide path, wall/path/42 colors.
"""

import sys
import os
from typing import Dict, Any

from maze import MazeGenerator
from maze_pathfinding import find_shortest_path
from maze_format import to_output_format
from maze_visualize import visualize


def _enable_windows_ansi() -> None:
    """Enable ANSI escape sequences in Windows console if possible."""
    if sys.platform != "win32":
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        kernel32.SetConsoleMode(handle, 7)  # ENABLE_VT + ENABLE_PROCESSED_OUTPUT etc.
    except Exception:
        pass


def _clear_screen() -> None:
    """Clear the terminal screen (ANSI or fallback)."""
    print("\033[2J\033[H", end="", flush=True)


def _next_item(options: list, current: Any) -> Any:
    """Cycle to the next item in options; if current not in list, return first."""
    try:
        i = options.index(current)
        return options[(i + 1) % len(options)]
    except ValueError:
        return options[0]


def run_visual_interactive(params: Dict[str, Any], generator: MazeGenerator) -> None:
    """
    Run an interactive terminal visualisation of the maze.
    - [R]egenerate: create a new maze and write to OUTPUT_FILE.
    - [P]ath: show/hide the shortest path.
    - [C]olors: cycle wall colour.
    - [F] 42: cycle '42' pattern colour (off / cyan / magenta / blue).
    - [A]ccent: cycle path/accent colour.
    - [Q]uit: exit.
    """
    WALL_COLORS = ["white", "red", "green", "yellow", "blue", "magenta", "cyan"]
    PATH_COLORS = ["green", "yellow", "magenta", "cyan"]
    PATTERN_42_OPTS: list = [None, "cyan", "magenta", "blue"]

    show_path = True
    wall_color = "white"
    path_color = "green"
    entry_color = "yellow"
    exit_color = "yellow"
    pattern_42_color: Any = None

    _enable_windows_ansi()
    path = find_shortest_path(generator)

    while True:
        _clear_screen()
        print(
            visualize(
                generator,
                path,
                show_path=show_path,
                wall_color=wall_color,
                path_color=path_color,
                entry_color=entry_color,
                exit_color=exit_color,
                pattern_42_color=pattern_42_color,
                use_color=True,
            )
        )
        print(
            "[R]egenerate  [P]ath  [C]olors  [F] 42  [A]ccent  [Q]uit  "
            "(path=%s, walls=%s)" % ("on" if show_path else "off", wall_color)
        )
        try:
            cmd = input("> ").strip().lower()[:1]
        except (EOFError, KeyboardInterrupt):
            cmd = "q"

        if cmd == "q":
            break
        if cmd == "r":
            gen = MazeGenerator(
                width=params["width"],
                height=params["height"],
                entry=params["entry"],
                exit=params["exit"],
                perfect=params["perfect"],
                seed=None,
            )
            gen.generate()
            path = find_shortest_path(gen)
            if not path:
                gen = MazeGenerator(
                    width=params["width"],
                    height=params["height"],
                    entry=params["entry"],
                    exit=params["exit"],
                    perfect=params["perfect"],
                    seed=None,
                )
                gen.generate()
                path = find_shortest_path(gen)
            if path:
                generator = gen
                with open(params["output_file"], "w") as f:
                    f.write(to_output_format(generator, path))
            else:
                input("No path in new maze. Press Enter to keep current.")
            continue
        if cmd == "p":
            show_path = not show_path
        elif cmd == "c":
            wall_color = _next_item(WALL_COLORS, wall_color)
        elif cmd == "f":
            pattern_42_color = _next_item(PATTERN_42_OPTS, pattern_42_color)
        elif cmd == "a":
            path_color = _next_item(PATH_COLORS, path_color)


def parse_config_file(filename: str) -> Dict[str, Any]:
    """
    Parse the configuration file and extract maze parameters.
    
    Args:
        filename: Path to the configuration file
        
    Returns:
        Dictionary with configuration parameters
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If configuration is invalid
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Configuration file '{filename}' not found")
    
    config = {}
    
    try:
        with open(filename, 'r') as f:
            line_num = 0
            for line in f:
                line_num += 1
                # Remove whitespace and skip comments/empty lines
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse KEY=VALUE format
                if '=' not in line:
                    raise ValueError(f"Line {line_num}: Invalid format (expected KEY=VALUE)")
                
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                if not key or not value:
                    raise ValueError(f"Line {line_num}: Empty key or value")
                
                config[key] = value
    
    except IOError as e:
        raise IOError(f"Error reading configuration file: {e}")
    
    return config


def validate_and_convert_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate configuration and convert values to appropriate types.
    
    Args:
        config: Raw configuration dictionary
        
    Returns:
        Validated and converted configuration
        
    Raises:
        ValueError: If configuration is invalid
    """
    # Check mandatory keys
    mandatory_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    missing_keys = [key for key in mandatory_keys if key not in config]
    
    if missing_keys:
        raise ValueError(f"Missing mandatory configuration keys: {', '.join(missing_keys)}")
    
    validated = {}
    
    # Parse WIDTH
    try:
        validated['width'] = int(config['WIDTH'])
        if validated['width'] <= 0:
            raise ValueError("WIDTH must be positive")
    except ValueError as e:
        raise ValueError(f"Invalid WIDTH value: {e}")
    
    # Parse HEIGHT
    try:
        validated['height'] = int(config['HEIGHT'])
        if validated['height'] <= 0:
            raise ValueError("HEIGHT must be positive")
    except ValueError as e:
        raise ValueError(f"Invalid HEIGHT value: {e}")
    
    # Parse ENTRY (x,y format)
    try:
        entry_parts = config['ENTRY'].split(',')
        if len(entry_parts) != 2:
            raise ValueError("ENTRY must be in format x,y")
        validated['entry'] = (int(entry_parts[0]), int(entry_parts[1]))
    except ValueError as e:
        raise ValueError(f"Invalid ENTRY value: {e}")
    
    # Parse EXIT (x,y format)
    try:
        exit_parts = config['EXIT'].split(',')
        if len(exit_parts) != 2:
            raise ValueError("EXIT must be in format x,y")
        validated['exit'] = (int(exit_parts[0]), int(exit_parts[1]))
    except ValueError as e:
        raise ValueError(f"Invalid EXIT value: {e}")
    
    # Parse PERFECT
    perfect_value = config['PERFECT'].lower()
    if perfect_value in ['true', '1', 'yes']:
        validated['perfect'] = True
    elif perfect_value in ['false', '0', 'no']:
        validated['perfect'] = False
    else:
        raise ValueError(f"Invalid PERFECT value: {config['PERFECT']} (expected True/False)")
    
    # OUTPUT_FILE
    validated['output_file'] = config['OUTPUT_FILE']
    
    # Optional: SEED
    if 'SEED' in config:
        try:
            validated['seed'] = int(config['SEED'])
        except ValueError:
            raise ValueError(f"Invalid SEED value: {config['SEED']}")
    else:
        validated['seed'] = None
    
    # Optional: ALGORITHM
    if 'ALGORITHM' in config:
        validated['algorithm'] = config['ALGORITHM'].lower()
    else:
        validated['algorithm'] = 'dfs'
    
    return validated


def generate_maze_from_config(
    config_file: str, visual: bool = False, graphical: bool = False
) -> None:
    """
    Main function to generate a maze from a configuration file.

    Args:
        config_file: Path to the configuration file
        visual: If True, run interactive terminal visual mode after generating.
        graphical: If True, open a MiniLibX (mlx) window with the maze. Requires mlx on Ubuntu: pip install ./mlx-2.2-py3-ubuntu-any.whl
    """
    try:
        # Parse configuration
        print(f"Reading configuration from '{config_file}'...")
        config = parse_config_file(config_file)
        
        # Validate and convert configuration
        print("Validating configuration...")
        params = validate_and_convert_config(config)
        
        # Create maze generator
        print(f"Generating {params['width']}x{params['height']} maze...")
        generator = MazeGenerator(
            width=params['width'],
            height=params['height'],
            entry=params['entry'],
            exit=params['exit'],
            perfect=params['perfect'],
            seed=params['seed']
        )
        
        # Generate the maze
        pattern_created = generator.generate()
        
        if not pattern_created:
            print("WARNING: Maze is too small to include the '42' pattern (minimum 7x5 required)")
        
        path = find_shortest_path(generator)
        if not path:
            print("ERROR: No path exists between entry and exit!")
            sys.exit(1)

        print(f"Maze generated successfully!")
        print(f"Shortest path length: {len(path)} steps")

        output_file = params['output_file']
        print(f"Writing maze to '{output_file}'...")
        with open(output_file, 'w') as f:
            f.write(to_output_format(generator, path))
        print(f"Maze written successfully to '{output_file}'")

        if not visual:
            print("\nVisual representation:")
            print(visualize(generator, path))

        print(f"\nEntry: {params['entry']}")
        print(f"Exit: {params['exit']}")
        print(f"Path: {''.join(path)}")

        if graphical:
            try:
                from maze_graphics import run_graphics

                print("\nOpening graphical display (close window or press ESC/Q to exit)...")
                run_graphics(generator, path, show_path=True, show_42=True)
            except ImportError:
                print(
                    "Graphics (mlx) not available. On Ubuntu: pip install ./mlx-2.2-py3-ubuntu-any.whl",
                    file=sys.stderr,
                )
            except RuntimeError as e:
                print(f"Graphics unavailable: {e}", file=sys.stderr)
                print(
                    "On Ubuntu: pip install ./mlx-2.2-py3-ubuntu-any.whl",
                    file=sys.stderr,
                )

        if visual:
            print("\nStarting interactive visual mode...")
            run_visual_interactive(params, generator)

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"ERROR: I/O error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the program."""
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt [-v|--visual] [-g|--graphical]", file=sys.stderr)
        print("\nGenerates a maze from a configuration file.", file=sys.stderr)
        print("  -v, --visual     Run interactive terminal visual mode.", file=sys.stderr)
        print("  -g, --graphical  Open a graphical (MiniLibX/mlx) window of the maze.", file=sys.stderr)
        print("\nConfiguration file format:", file=sys.stderr)
        print("  WIDTH=<number>        - Maze width in cells", file=sys.stderr)
        print("  HEIGHT=<number>       - Maze height in cells", file=sys.stderr)
        print("  ENTRY=<x>,<y>         - Entry coordinates", file=sys.stderr)
        print("  EXIT=<x>,<y>          - Exit coordinates", file=sys.stderr)
        print("  OUTPUT_FILE=<path>    - Output file path", file=sys.stderr)
        print("  PERFECT=<True|False>  - Perfect maze flag", file=sys.stderr)
        print("  SEED=<number>         - Random seed (optional)", file=sys.stderr)
        sys.exit(1)

    config_file = sys.argv[1]
    visual = "--visual" in sys.argv or "-v" in sys.argv
    graphical = "--graphical" in sys.argv or "-g" in sys.argv
    generate_maze_from_config(config_file, visual=visual, graphical=graphical)


if __name__ == "__main__":
    main()
