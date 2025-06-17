#!/bin/bash

# Development setup script for streamlit-expandable-columns
# This script helps set up the development environment

set -e

echo "🚀 Setting up Streamlit Expandable Columns development environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14+ and try again."
    echo "   You can download it from: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm and try again."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd streamlit_expandable_columns/frontend
npm install
cd ../..

echo "✅ Dependencies installed successfully"

# Create development environment info
echo "
🎉 Development environment setup complete!

To start developing:

1. Activate the virtual environment (if not already active):
   source venv/bin/activate

2. Start the frontend development server:
   cd streamlit_expandable_columns/frontend
   npm start

3. In another terminal, activate venv and run the example:
   source venv/bin/activate
   streamlit run example.py

4. Or run tests:
   source venv/bin/activate
   streamlit run test_component.py

The frontend server will run on http://localhost:3001
Your Streamlit app will run on http://localhost:8501

Happy coding! 🎛️
"

echo "💡 Pro tips:"
echo "   - Set _RELEASE = False in __init__.py for development mode"
echo "   - Always activate your venv: source venv/bin/activate"
echo "   - To deactivate venv: deactivate" 