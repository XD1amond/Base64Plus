#!/usr/bin/env python3
"""
Installation script for Base64Plus library.
This script helps users install the Base64Plus library for their preferred language.
"""

import os
import sys
import subprocess
import platform
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

def install_python(ocr_engine="all", dev_mode=False):
    """Install the Python package."""
    print_header("Installing Base64Plus for Python")
    
    # Get the Python package directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    python_dir = os.path.join(base_dir, "python")
    
    if not os.path.exists(python_dir):
        print(f"Error: Python package directory not found at {python_dir}")
        return False
    
    # Install the package
    if dev_mode:
        print("Installing in development mode...")
        command = [sys.executable, "-m", "pip", "install", "-e", "."]
    else:
        print("Installing package...")
        command = [sys.executable, "-m", "pip", "install", "."]
    
    # Add OCR engine extras
    if ocr_engine == "easyocr":
        command[-1] += "[easyocr]"
    elif ocr_engine == "tesseract":
        command[-1] += "[tesseract]"
    elif ocr_engine == "all":
        command[-1] += "[all]"
    
    success = run_command(command, cwd=python_dir)
    
    if success:
        print("\nPython package installed successfully!")
        
        # Print additional instructions for Tesseract if needed
        if ocr_engine in ["tesseract", "all"]:
            print("\nNote: If you're using Tesseract, you also need to install the Tesseract executable:")
            if platform.system() == "Linux":
                print("  Ubuntu/Debian: sudo apt-get install tesseract-ocr")
            elif platform.system() == "Darwin":  # macOS
                print("  macOS: brew install tesseract")
            elif platform.system() == "Windows":
                print("  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
    
    return success

def install_javascript(dev_mode=False):
    """Install the JavaScript package."""
    print_header("Installing Base64Plus for JavaScript")
    
    # Get the JavaScript package directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    js_dir = os.path.join(base_dir, "javascript")
    
    if not os.path.exists(js_dir):
        print(f"Error: JavaScript package directory not found at {js_dir}")
        return False
    
    # Check if npm is available
    if not run_command(["npm", "--version"]):
        print("Error: npm is not installed or not in PATH")
        return False
    
    # Install dependencies
    print("Installing dependencies...")
    if dev_mode:
        success = run_command(["npm", "install"], cwd=js_dir)
    else:
        success = run_command(["npm", "install", "--production"], cwd=js_dir)
    
    if success:
        print("\nJavaScript package installed successfully!")
        
        # Print additional instructions for canvas on Linux
        if platform.system() == "Linux":
            print("\nNote: If you encounter issues with the 'canvas' package on Linux, you may need to install additional dependencies:")
            print("  Ubuntu/Debian: sudo apt-get install build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev")
    
    return success

def generate_test_image():
    """Generate test images for examples."""
    print_header("Generating Test Images")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, "tools", "generate_test_image.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Test image generator script not found at {script_path}")
        return False
    
    return run_command([sys.executable, script_path])

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Install Base64Plus library")
    parser.add_argument("--language", "-l", choices=["python", "javascript", "all"], default="all",
                        help="Language implementation to install (default: all)")
    parser.add_argument("--ocr", choices=["easyocr", "tesseract", "all"], default="all",
                        help="OCR engine to install for Python (default: all)")
    parser.add_argument("--dev", action="store_true",
                        help="Install in development mode")
    parser.add_argument("--test-image", action="store_true",
                        help="Generate test images for examples")
    
    args = parser.parse_args()
    
    # Print welcome message
    print_header("Base64Plus Installation")
    print("This script will help you install the Base64Plus library.")
    
    success = True
    
    # Install Python package
    if args.language in ["python", "all"]:
        success = install_python(args.ocr, args.dev) and success
    
    # Install JavaScript package
    if args.language in ["javascript", "all"]:
        success = install_javascript(args.dev) and success
    
    # Generate test images if requested
    if args.test_image:
        success = generate_test_image() and success
    
    # Print final message
    if success:
        print_header("Installation Complete")
        print("Base64Plus has been installed successfully!")
        print("\nTo generate test images for examples, run:")
        print("  python install.py --test-image")
        print("\nFor more information, see the README.md files in each language directory.")
    else:
        print_header("Installation Failed")
        print("There were errors during installation. Please check the output above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())