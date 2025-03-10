#!/usr/bin/env python3
"""
Generate documentation for the Base64Plus library.
This script uses pdoc for Python and JSDoc for JavaScript.
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

def generate_python_docs():
    """Generate Python documentation using pdoc."""
    print_header("Generating Python Documentation")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    python_dir = os.path.join(base_dir, "python")
    
    if not os.path.exists(python_dir):
        print(f"Error: Python package directory not found at {python_dir}")
        return False
    
    # Check if pdoc is installed
    try:
        import pdoc
        print("✓ pdoc is installed")
    except ImportError:
        print("Installing pdoc...")
        if not run_command([sys.executable, "-m", "pip", "install", "pdoc"]):
            print("Error: Failed to install pdoc")
            return False
    
    # Create output directory
    docs_dir = os.path.join(base_dir, "docs", "python")
    os.makedirs(docs_dir, exist_ok=True)
    
    # Generate documentation
    print(f"Generating documentation in {docs_dir}...")
    return run_command([
        sys.executable, "-m", "pdoc", 
        "--html", 
        "--output-dir", docs_dir, 
        "base64plus"
    ])

def generate_javascript_docs():
    """Generate JavaScript documentation using JSDoc."""
    print_header("Generating JavaScript Documentation")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    js_dir = os.path.join(base_dir, "javascript")
    
    if not os.path.exists(js_dir):
        print(f"Error: JavaScript package directory not found at {js_dir}")
        return False
    
    # Check if npm is available
    if not run_command(["npm", "--version"]):
        print("Error: npm is not installed or not in PATH")
        return False
    
    # Check if JSDoc is installed
    print("Installing JSDoc locally...")
    if not run_command(["npm", "install", "--no-save", "jsdoc"], cwd=js_dir):
        print("Error: Failed to install JSDoc")
        return False
    
    # Create output directory
    docs_dir = os.path.join(base_dir, "docs", "javascript")
    os.makedirs(docs_dir, exist_ok=True)
    
    # Generate documentation
    print(f"Generating documentation in {docs_dir}...")
    return run_command([
        "npx", "jsdoc", 
        "-d", docs_dir, 
        "index.js", "README.md"
    ], cwd=js_dir)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate documentation for Base64Plus library")
    parser.add_argument("--language", "-l", choices=["python", "javascript", "all"], default="all",
                        help="Language implementation to document (default: all)")
    
    args = parser.parse_args()
    
    # Print welcome message
    print_header("Base64Plus Documentation Generator")
    print("This script will generate documentation for the Base64Plus library.")
    
    success = True
    
    # Generate Python documentation
    if args.language in ["python", "all"]:
        success = generate_python_docs() and success
    
    # Generate JavaScript documentation
    if args.language in ["javascript", "all"]:
        success = generate_javascript_docs() and success
    
    # Print final message
    if success:
        print_header("Documentation Generation Complete")
        print("Documentation has been generated successfully!")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        docs_dir = os.path.join(base_dir, "docs")
        print(f"\nDocumentation is available in: {docs_dir}")
        print("- Python: docs/python/base64plus/index.html")
        print("- JavaScript: docs/javascript/index.html")
    else:
        print_header("Documentation Generation Failed")
        print("There were errors during documentation generation. Please check the output above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())