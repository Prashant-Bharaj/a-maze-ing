#!/usr/bin/env python3
"""
Test suite for A-MAZE-ING maze generator
"""

import os
import sys
import subprocess


def run_test(name, config_file, should_succeed=True):
    """Run a single test case."""
    print(f"\n{'='*60}")
    print(f"Test: {name}")
    print(f"{'='*60}")
    
    cmd = ["python3", "a_maze_ing.py", config_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    success = (result.returncode == 0) == should_succeed
    
    if success:
        print(f"✓ Test PASSED")
    else:
        print(f"✗ Test FAILED (expected {'success' if should_succeed else 'failure'})")
    
    return success


def main():
    """Run all tests."""
    print("A-MAZE-ING Test Suite")
    print("=" * 60)
    
    tests = [
        ("Default configuration (20x15, perfect)", "config.txt", True),
        ("Small maze (5x4, perfect)", "config_small.txt", True),
        ("Large maze (25x20, perfect)", "config_large.txt", True),
        ("Imperfect maze (15x12, non-perfect)", "config_imperfect.txt", True),
        ("Missing file (should fail)", "nonexistent.txt", False),
        ("Invalid configuration (should fail)", "config_invalid.txt", False),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, config_file, should_succeed in tests:
        if run_test(test_name, config_file, should_succeed):
            passed += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Test Summary")
    print(f"{'='*60}")
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
