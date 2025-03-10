#!/bin/bash
# Simple wrapper script for install.py

# Make the script executable
chmod +x install.py

# Run the installation script with all arguments passed to this script
./install.py "$@"