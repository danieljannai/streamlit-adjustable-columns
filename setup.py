from setuptools import setup, find_packages
import os
import subprocess
import sys

# Read the README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

def build_frontend():
    """Build the frontend assets during installation."""

    frontend_dir = os.path.join(this_directory, "streamlit_expandable_columns", "frontend")
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

setup(
    name="streamlit-expandable-columns",
    version="0.1.2",
    author="Daniel Jannai Epstein",
    description="A Streamlit custom component for creating columns with adjustable widths",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danieljannai/streamlit-expandable-columns",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        # "Framework :: Streamlit",
    ],
    python_requires=">=3.9",
    install_requires=[
        "streamlit>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "playwright>=1.30.0",
            "requests>=2.25.0",
        ]
    },
) 
