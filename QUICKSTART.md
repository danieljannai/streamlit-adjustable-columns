# Quick Start Guide

Get the Streamlit Expandable Columns component running in under 5 minutes!

## 📦 Installing the Package

### From PyPI (Recommended)
```bash
pip install streamlit-expandable-columns
```

### From GitHub
```bash
pip install git+https://github.com/danieljannai/streamlit-expandable-columns.git
```

**Important**: This package requires Node.js and npm to build the frontend components during installation. If you don't have them installed:

1. Install Node.js from [nodejs.org](https://nodejs.org/)
2. Reinstall the package: `pip install streamlit-expandable-columns`

### Using the Package
```python
import streamlit as st
from streamlit_expandable_columns import expandable_columns

# Create resizable columns
col1, col2, col3 = expandable_columns(3, labels=["📊 Charts", "📋 Data", "⚙️ Settings"])

with col1:
    st.metric("Sales", "$1,234", "12%")
    
col2.write("This column can be resized!")
col3.button("Settings")
```

## 🚀 Development Setup (Automated)

Run the setup script to handle everything automatically:

```bash
./dev_setup.sh
```

This script will:
- ✅ Check prerequisites (Python 3.7+, Node.js, npm)
- ✅ Create a Python virtual environment
- ✅ Install all Python dependencies
- ✅ Install all frontend dependencies
- ✅ Provide next steps

## 🛠️ Manual Development Setup

If you prefer to set up manually:

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
cd streamlit_expandable_columns/frontend
npm install
cd ../..
```

## 🎯 Testing the Component

### Option 1: Run the Full Demo
```bash
# Terminal 1: Start frontend development server
cd streamlit_expandable_columns/frontend
npm start

# Terminal 2: Run the demo (make sure venv is activated)
source venv/bin/activate
streamlit run example.py
```

### Option 2: Run Basic Tests
```bash
# Make sure venv is activated
source venv/bin/activate

# Terminal 1: Start frontend development server
cd streamlit_expandable_columns/frontend
npm start

# Terminal 2: Run tests
streamlit run test_component.py
```

### Option 3: Quick Test (No Frontend Dev Server)
If you just want to see if the Python component loads:

```bash
source venv/bin/activate
streamlit run test_component.py
```

*Note: Without the frontend dev server, you'll see a loading placeholder instead of the interactive resizer, but the Streamlit columns will still work.*

## 🌐 What You'll See

1. **Frontend Dev Server**: http://localhost:3001
   - This serves the interactive column resizer component

2. **Streamlit App**: http://localhost:8501
   - Your main app with the expandable columns

## ✅ Success Indicators

You know it's working when you see:
- ✅ Column headers with drag handles between them
- ✅ Ability to drag column separators to resize
- ✅ Column widths persist when you interact with other elements
- ✅ Responsive behavior on different screen sizes

## 🐛 Troubleshooting

### Component shows "Loading..." forever
- Make sure the frontend dev server is running on port 3001
- Check that `_RELEASE = False` in `streamlit_expandable_columns/__init__.py`

### "Module not found" error
- Make sure your virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Make sure Node.js and npm are installed
- Delete `node_modules` and run `npm install` again

### Port conflicts
- If port 3001 or 8501 are busy, kill other processes or change ports in the configuration

## 🎊 Next Steps

Once everything is working:

1. **Explore the examples** in `example.py`
2. **Read the full documentation** in `README.md`
3. **Try the API** with different column configurations
4. **Build your own app** using the component

Happy coding! 🎛️