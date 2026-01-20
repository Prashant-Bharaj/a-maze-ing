#!/bin/bash
# Quick test script for A-MAZE-ING maze generator

echo "=========================================="
echo "A-MAZE-ING Quick Test"
echo "=========================================="
echo ""

# Test 1: Default maze
echo "Test 1: Generating default maze..."
python3 a_maze_ing.py config.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Default maze generated"
    python3 output_validator.py output_maze.txt 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ Default maze validated"
    else
        echo "✗ Default maze validation failed"
    fi
else
    echo "✗ Default maze generation failed"
fi
echo ""

# Test 2: Small maze
echo "Test 2: Generating small maze..."
python3 a_maze_ing.py config_small.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Small maze generated"
    python3 output_validator.py small_maze.txt 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ Small maze validated"
    else
        echo "✗ Small maze validation failed"
    fi
else
    echo "✗ Small maze generation failed"
fi
echo ""

# Test 3: Large maze
echo "Test 3: Generating large maze..."
python3 a_maze_ing.py config_large.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Large maze generated"
    python3 output_validator.py large_maze.txt 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ Large maze validated"
    else
        echo "✗ Large maze validation failed"
    fi
else
    echo "✗ Large maze generation failed"
fi
echo ""

# Test 4: Error handling
echo "Test 4: Testing error handling..."
python3 a_maze_ing.py nonexistent.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "✓ Error handling works correctly"
else
    echo "✗ Error handling failed"
fi
echo ""

echo "=========================================="
echo "Tests complete!"
echo "=========================================="
