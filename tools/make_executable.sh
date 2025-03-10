#!/bin/bash
# Make all scripts executable

# Get the base directory
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Make Python scripts executable
chmod +x "$BASE_DIR/install.py"
chmod +x "$BASE_DIR/install.sh"
chmod +x "$BASE_DIR/run_tests.py"
chmod +x "$BASE_DIR/run_tests.sh"
chmod +x "$BASE_DIR/tools/generate_test_image.py"
chmod +x "$BASE_DIR/tools/generate_docs.py"

echo "All scripts are now executable."