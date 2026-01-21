#!/bin/bash
# Build script for mazegen package
# This script builds the mazegen package from sources

set -e  # Exit on error

echo "Building mazegen package..."
echo "=============================="
echo

# Clean previous build artifacts
echo "1. Cleaning previous build artifacts..."
rm -rf dist/ build/ mazegen.egg-info/
echo "   ✓ Cleaned"
echo

# Ensure build tools are installed
echo "2. Installing build tools..."
.venv/bin/pip install --quiet --upgrade build
echo "   ✓ Build tools ready"
echo

# Build the package
echo "3. Building package (this may take a moment)..."
.venv/bin/python -m build
echo "   ✓ Build complete"
echo

# Show results
echo "4. Build results:"
echo "   Generated files in dist/:"
ls -lh dist/
echo

# Copy wheel to root
echo "5. Copying wheel file to repository root..."
cp dist/mazegen-*.whl .
echo "   ✓ Done"
echo

echo "=============================="
echo "Build completed successfully!"
echo
echo "You can now install the package with:"
echo "  pip install mazegen-1.0.0-py3-none-any.whl"
echo
echo "Or install from source:"
echo "  pip install ."
