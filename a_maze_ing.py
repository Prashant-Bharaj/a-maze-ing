#!/usr/bin/env python3
"""
A-MAZE-ING Maze Generator
Generates a maze from a configuration file and outputs it in
hexadecimal format. Supports interactive visual mode with: regenerate,
show/hide path, wall/path/42 colors.
"""

import sys
import os
import time
from typing import Dict, Any, Tuple, List

from mazegen import MazeGenerator
from maze_pathfinding import find_shortest_path
from maze_format import to_output_format
from maze_visualize import visualize
from maze_animate import (
    animate_pathfinding,
    animate_maze_with_path,
)


def _enable_windows_ansi() -> None:
    """Enable ANSI escape sequences in Windows console if possible."""
    if sys.platform != "win32":
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        # ENABLE_VT + ENABLE_PROCESSED_OUTPUT etc.
        kernel32.SetConsoleMode(handle, 7)
        # ENABLE_VT + ENABLE_PROCESSED_OUTPUT etc.
        kernel32.SetConsoleMode(handle, 7)
    except Exception:
        pass


def _clear_screen() -> None:
    """Clear the terminal screen (ANSI or fallback)."""
    print("\033[2J\033[H", end="", flush=True)


def _next_item(options: List[Any], current: Any) -> Any:
    """Cycle to the next item in options; return first if not in list."""
    try:
        i = options.index(current)
        return options[(i + 1) % len(options)]
    except ValueError:
        return options[0]


def run_visual_interactive(
    params: Dict[str, Any],
    generator: MazeGenerator,
) -> None:
    """
    Run an interactive terminal visualisation of the maze.
    - [R]egenerate: create a new maze and write to OUTPUT_FILE.
    - [P]ath: show/hide the shortest path.
    - [C]olors: cycle wall colour.
    - [F] 42: cycle '42' pattern colour (off / cyan / magenta / blue).
    - [A]ccent: cycle path/accent colour.
    - [Q]uit: exit.
    """
    WALL_COLORS = [
        "white",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
    ]
    PATH_COLORS = ["green", "yellow", "magenta", "cyan"]
    PATTERN_42_COLOR = [
        "white",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
    ]

    show_path = True
    wall_color = "white"
    path_color = "green"
    entry_color = "yellow"
    exit_color = "yellow"
    pattern_42_color = "white"

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
            pattern_42_color = _next_item(PATTERN_42_COLOR, pattern_42_color)
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
        with open(filename, "r") as f:
            line_num = 0
            for line in f:
                line_num += 1
                # Remove whitespace and skip comments/empty lines
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Parse KEY=VALUE format
                if "=" not in line:
                    raise ValueError(
                        f"Line {line_num}: Invalid format (expected KEY=VALUE)"
                    )

                key, value = line.split("=", 1)
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
    mandatory_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    ]
    mandatory_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    ]
    missing_keys = [key for key in mandatory_keys if key not in config]

    if missing_keys:
        missing = ", ".join(missing_keys)
        raise ValueError(f"Missing mandatory configuration keys: {missing}")

    validated: Dict[str, Any] = {}

    # Parse WIDTH
    try:
        width_val = int(config["WIDTH"])
        if width_val <= 0:
            raise ValueError("WIDTH must be positive")
        validated["width"] = width_val
    except ValueError as e:
        raise ValueError(f"Invalid WIDTH value: {e}")

    # Parse HEIGHT
    try:
        height_val = int(config["HEIGHT"])
        if height_val <= 0:
            raise ValueError("HEIGHT must be positive")
        validated["height"] = height_val
    except ValueError as e:
        raise ValueError(f"Invalid HEIGHT value: {e}")

    # Parse ENTRY (x,y format)
    try:
        entry_parts = config["ENTRY"].split(",")
        if len(entry_parts) != 2:
            raise ValueError("ENTRY must be in format x,y")
        entry_val: Tuple[int, int] = (int(entry_parts[0]), int(entry_parts[1]))
        validated["entry"] = entry_val
    except ValueError as e:
        raise ValueError(f"Invalid ENTRY value: {e}")

    # Parse EXIT (x,y format)
    try:
        exit_parts = config["EXIT"].split(",")
        if len(exit_parts) != 2:
            raise ValueError("EXIT must be in format x,y")
        exit_val: Tuple[int, int] = (int(exit_parts[0]), int(exit_parts[1]))
        validated["exit"] = exit_val
    except ValueError as e:
        raise ValueError(f"Invalid EXIT value: {e}")

    # Parse PERFECT
    perfect_value = config["PERFECT"].lower()
    if perfect_value in ["true", "1", "yes"]:
        validated["perfect"] = True
    elif perfect_value in ["false", "0", "no"]:
        validated["perfect"] = False
    else:
        raise ValueError(
            f"Invalid PERFECT value: {config['PERFECT']} (expected True/False)"
        )

    # OUTPUT_FILE
    validated["output_file"] = config["OUTPUT_FILE"]

    # Optional: SEED
    if "SEED" in config:
        try:
            validated["seed"] = int(config["SEED"])
        except ValueError:
            raise ValueError(f"Invalid SEED value: {config['SEED']}")
    else:
        seed_value: Any = None
        validated["seed"] = seed_value

    
    if "ALGORITHM" in config:
        algo_value: Any = config["ALGORITHM"].lower()
        validated["algorithm"] = algo_value
    else:
        default_algo: Any = "dfs"
        validated["algorithm"] = default_algo

    return validated


def generate_maze_from_config(
    config_file: str,
    visual: bool = False,
    animate: bool = False,
    animate_algo: bool = False,
) -> None:
    """
    Main function to generate a maze from a configuration file.

    Args:
        config_file: Path to the configuration file
        visual: If True, run interactive terminal visual mode after
                generating.
        animate: If True, animate maze drawing line by line.
        animate_algo: If True, animate the pathfinding algorithm solving
                      the maze.
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
            width=params["width"],
            height=params["height"],
            entry=params["entry"],
            exit=params["exit"],
            perfect=params["perfect"],
            seed=params["seed"],
        )

        # Generate the maze
        generator.generate()
        generator.generate()

        if animate_algo:
            print("\n" + "=" * 50)
            path = animate_pathfinding(
                generator,
                delay=0.08,
                use_color=True,
            )
            print("=" * 50)
        else:
            path = find_shortest_path(generator)

        if not path:
            print("ERROR: No path exists between entry and exit!")
            sys.exit(1)

        print("Maze generated successfully!")
        print("Maze generated successfully!")
        print(f"Shortest path length: {len(path)} steps")

        output_file = params["output_file"]
        print(f"Writing maze to '{output_file}'...")
        with open(output_file, "w") as f:
            f.write(to_output_format(generator, path))
        print(f"Maze written successfully to '{output_file}'")

        # Animation: maze drawing + path tracing
        if animate:
            _clear_screen()
            animate_maze_with_path(
                generator,
                path,
                draw_delay=0.05,
                highlight_delay=0.08,
                use_color=True,
            )
            print(f"\nEntry: {params['entry']}")
            print(f"Exit: {params['exit']}")
            print(f"Path: {''.join(path)}")
            time.sleep(2)
        elif not visual:
            print("\nVisual representation:")
            print(visualize(generator, path))

            print(f"\nEntry: {params['entry']}")
            print(f"Exit: {params['exit']}")
            print(f"Path: {''.join(path)}")
        else:
            print(f"\nEntry: {params['entry']}")
            print(f"Exit: {params['exit']}")
            print(f"Path: {''.join(path)}")

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


def main() -> None:
    """Main entry point for the program."""
    if len(sys.argv) < 2:
        print(
            "Usage: python3 a_maze_ing.py config.txt [OPTIONS]",
            file=sys.stderr,
        )
        print("\nGenerates a maze from a configuration file.", file=sys.stderr)
        print("Options:", file=sys.stderr)
        print(
            "  -v, --visual         Run interactive terminal visual mode.",
            file=sys.stderr,
        )
        print(
            "  -a, --animate        Animate maze drawing line by line.",
            file=sys.stderr,
        )
        print(
            "  --animate-algo       Animate pathfinding algorithm ",
            end="",
            file=sys.stderr,
        )
        print(
            "visualization.",
            file=sys.stderr,
        )
        print("\nConfiguration file format:", file=sys.stderr)
        print(
            "  WIDTH=<number>        - Maze width in cells",
            file=sys.stderr,
        )
        print(
            "  HEIGHT=<number>       - Maze height in cells",
            file=sys.stderr,
        )
        print("  ENTRY=<x>,<y>         - Entry coordinates", file=sys.stderr)
        print("  EXIT=<x>,<y>          - Exit coordinates", file=sys.stderr)
        print(
            "  OUTPUT_FILE=<path>    - Output file path",
            file=sys.stderr,
        )
        print(
            "  PERFECT=<True|False>  - Perfect maze flag",
            file=sys.stderr,
        )
        print(
            "  SEED=<number>         - Random seed (optional)",
            file=sys.stderr,
        )
        sys.exit(1)

    config_file = sys.argv[1]
    visual = "--visual" in sys.argv or "-v" in sys.argv
    animate = "--animate" in sys.argv or "-a" in sys.argv
    animate_algo = "--animate-algo" in sys.argv
    _enable_windows_ansi()
    generate_maze_from_config(
        config_file, visual=visual, animate=animate, animate_algo=animate_algo
    )


if __name__ == "__main__":
    main()
