#!/usr/bin/env python3
"""
A-MAZE-ING Maze Generator
Generates a maze from a configuration file and outputs it in hexadecimal format.
"""

import sys
import os
from typing import Dict, Any, Tuple
from maze import MazeGenerator


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


def generate_maze_from_config(config_file: str) -> None:
    """
    Main function to generate a maze from a configuration file.
    
    Args:
        config_file: Path to the configuration file
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
        
        # Find the shortest path
        path = generator.find_shortest_path()
        if not path:
            print("ERROR: No path exists between entry and exit!")
            sys.exit(1)
        
        print(f"Maze generated successfully!")
        print(f"Shortest path length: {len(path)} steps")
        
        # Write output file
        output_file = params['output_file']
        print(f"Writing maze to '{output_file}'...")
        
        with open(output_file, 'w') as f:
            f.write(generator.to_output_format())
        
        print(f"Maze written successfully to '{output_file}'")
        
        # Display visual representation
        print("\nVisual representation:")
        print(generator.visualize())
        
        print(f"\nEntry: {params['entry']}")
        print(f"Exit: {params['exit']}")
        print(f"Path: {''.join(path)}")
        
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
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        print("\nGenerates a maze from a configuration file.", file=sys.stderr)
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
    generate_maze_from_config(config_file)


if __name__ == "__main__":
    main()
