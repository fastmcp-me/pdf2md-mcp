#!/usr/bin/env python3
"""
Setup script for PDF2MD MCP Server development environment.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Set up the development environment."""
    print("Setting up PDF2MD MCP Server development environment...\n")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment detected")
    else:
        print("⚠ Warning: Not in a virtual environment. Consider creating one:")
        print("  python -m venv venv")
        print("  venv\\Scripts\\activate  # Windows")
        print("  source venv/bin/activate  # Linux/Mac")
        print()
    
    # Install package in development mode
    if not run_command("pip install -e .", "Installing package in development mode"):
        return False
    
    # Install development dependencies
    if not run_command("pip install -e \".[dev]\"", "Installing development dependencies"):
        return False
    
    # Run tests
    if Path("tests").exists():
        run_command("pytest tests/", "Running tests")
    
    # Check code formatting
    run_command("black --check .", "Checking code formatting")
    run_command("isort --check-only .", "Checking import sorting")
    
    print("\n" + "="*50)
    print("Setup completed!")
    print("\nNext steps:")
    print("1. Run tests: pytest")
    print("2. Start the server: pdf2md-mcp")
    print("3. Format code: black .")
    print("4. Sort imports: isort .")
    print("5. Type checking: mypy pdf2md_mcp/")
    print("\nFor help: pdf2md-mcp --help")
    

if __name__ == "__main__":
    main()
