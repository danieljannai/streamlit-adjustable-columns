from setuptools import setup
import os
import subprocess
import sys


def build_frontend():
    """Build the frontend assets during installation."""

    this_directory = os.path.abspath(os.path.dirname(__file__))
    frontend_dir = os.path.join(this_directory, "streamlit_adjustable_columns", "frontend")
    build_dir = os.path.join(frontend_dir, "build")

    # Skip build if compiled assets already exist
    required = ["index.html", "main.js"]
    if all(os.path.exists(os.path.join(build_dir, f)) for f in required):
        print("Frontend already built. Skipping build.")
        return True

    # Check if Node.js and npm are available
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: Node.js and npm are required to build the frontend.")
        print("Please install Node.js and npm, then reinstall this package.")
        return False
    
    # Install dependencies and build
    try:
        print("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, capture_output=True)
        
        print("Building frontend...")
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True, capture_output=True)
        
        print("Frontend built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building frontend: {e}")
        return False

# Build frontend during setup - handle more installation scenarios
if any(arg in sys.argv for arg in ["install", "develop", "bdist_wheel", "sdist", "bdist"]):
    build_frontend()

# Minimal setup - all metadata is now in pyproject.toml
setup() 
