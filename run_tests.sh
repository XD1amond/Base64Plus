#!/bin/bash
# Simple wrapper script for run_tests.py

# Make the script executable
chmod +x run_tests.py

# Run the tests script with all arguments passed to this script
./run_tests.py "$@"