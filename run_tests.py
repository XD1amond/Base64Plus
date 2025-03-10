#!/usr/bin/env python3
"""
Run all tests for the Base64Plus library.
"""

import os
import sys
import subprocess
import argparse

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def run_command(command, cwd=None):
    """Run a shell command and print output."""
    print(f"> {' '.join(command)}")
    try:
        result = subprocess.run(
            command, 
            cwd=cwd,
            check=True, 
            text=True, 
            capture_output=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False

def run_python_tests():
    """Run Python tests."""
    print_header("Running Python Tests")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    python_dir = os.path.join(base_dir, "python")
    
    if not os.path.exists(python_dir):
        print(f"Error: Python package directory not found at {python_dir}")
        return False
    
    # Run unittest
    test_dir = os.path.join(python_dir, "tests")
    if not os.path.exists(test_dir):
        print(f"Error: Python tests directory not found at {test_dir}")
        return False
    
    return run_command([sys.executable, "-m", "unittest", "discover", test_dir])

def run_javascript_tests():
    """Run JavaScript tests."""
    print_header("Running JavaScript Tests")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    js_dir = os.path.join(base_dir, "javascript")
    
    if not os.path.exists(js_dir):
        print(f"Error: JavaScript package directory not found at {js_dir}")
        return False
    
    # Check if node is available
    if not run_command(["node", "--version"]):
        print("Error: Node.js is not installed or not in PATH")
        return False
    
    # Run the test script
    test_script = os.path.join(js_dir, "tests", "test-base64plus.js")
    if not os.path.exists(test_script):
        print(f"Error: JavaScript test script not found at {test_script}")
        return False
    
    return run_command(["node", test_script])

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run tests for Base64Plus library")
    parser.add_argument("--language", "-l", choices=["python", "javascript", "all"], default="all",
                        help="Language implementation to test (default: all)")
    
    args = parser.parse_args()
    
    # Print welcome message
    print_header("Base64Plus Tests")
    print("This script will run tests for the Base64Plus library.")
    
    success = True
    
    # Run Python tests
    if args.language in ["python", "all"]:
        success = run_python_tests() and success
    
    # Run JavaScript tests
    if args.language in ["javascript", "all"]:
        success = run_javascript_tests() and success
    
    # Print final message
    if success:
        print_header("All Tests Passed")
        print("All Base64Plus tests completed successfully!")
    else:
        print_header("Tests Failed")
        print("There were errors during testing. Please check the output above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())