# 🎯 Streamlit Adjustable Columns

[![PyPI version](https://badge.fury.io/py/streamlit-adjustable-columns.svg)](https://badge.fury.io/py/streamlit-adjustable-columns)

**Version:** 0.2.0

Create resizable columns in Streamlit! This component provides `st.columns` functionality with **draggable resize handles** that allow users to adjust column widths dynamically.

![Adjustable Columns Demo](adjustable-columns-demo.gif)

## ✨ Features

- **🎯 Drop-in Replacement**: Works exactly like `st.columns` with the same API
- **🖱️ Resizable Boundaries**: Drag handles between columns to adjust widths  
- **💾 Persistent State**: Column widths persist across app reruns
- **🎨 Theme Integration**: Automatically matches your Streamlit theme
- **📱 Responsive**: Works on desktop and mobile devices
- **⚙️ Full Compatibility**: Supports all `st.columns` parameters (gap, alignment, border)
- **🔒 Minimum Width**: 6% minimum width constraint prevents unusably narrow columns
- **📊 Width Tracking**: Optional `return_widths` parameter for dynamic layouts

## 🚀 Quick Start

### Installation

```bash
pip install streamlit-adjustable-columns
```

**Note**: Packages installed from PyPI already include the compiled frontend so no additional tools are required. If you install from a source checkout (e.g. GitHub), Node.js and npm are needed to build the frontend assets.

### Basic Usage

```python
import streamlit as st
from streamlit_adjustable_columns import adjustable_columns

# Use exactly like st.columns - but with resize handles!
col1, col2, col3 = adjustable_columns(3, labels=["📊 Charts", "📋 Data", "⚙️ Settings"])

with col1:
    st.metric("Sales", "$1,234", "12%")
    
col2.write("This column can be resized!")
col3.button("Settings")
```

### ✅ Success Indicators

You know it's working when you see:
- ✅ Column headers with drag handles between them
- ✅ Ability to drag column separators to resize
- ✅ Column widths persist when you interact with other elements
- ✅ Responsive behavior on different screen sizes

## 📖 API Reference

### `adjustable_columns(spec, *, gap="small", vertical_alignment="top", border=False, labels=None, return_widths=False, initial_hidden=None, key=None)`

Creates resizable columns with draggable boundaries.

#### Parameters

- **`spec`** (int or list): Number of columns or width ratios
  - `3` → Three equal columns  
  - `[2, 1]` → Two columns with 2:1 ratio
- **`gap`** (str): Space between columns - `"small"`, `"medium"`, or `"large"`
- **`vertical_alignment`** (str): Content alignment - `"top"`, `"center"`, or `"bottom"`
- **`border`** (bool): Show borders around columns
- **`labels`** (list): Custom labels shown in resize handles
- **`return_widths`** (bool): Return width information along with columns
- **`initial_hidden`** (list of bool, optional): List of booleans indicating which columns should start hidden. Must match the number of columns. Example: `[False, True, False]` will start the second column hidden.
- **`key`** (str): Unique component key (recommended for multiple instances)

#### Returns

- **Default**: List of column containers (same as `st.columns`)
- **With `return_widths=True`**: Dict with `{'columns': [...], 'widths': [...], 'hidden': [...]}`

## 🎮 How to Resize & Hide Columns

1. **Look for resize handles** above each set of adjustable columns
2. **Hover over the boundaries** between column areas - you'll see resize cursors
3. **Click and drag** the handles to adjust column widths
4. **Double-click a column header** to hide/show that column
5. **Release** to apply changes - they persist across app reruns!

## 📚 Examples

### Dashboard Layout

```python
# Create a dashboard with resizable main content and sidebar
main, sidebar = adjustable_columns([4, 1], labels=["📊 Dashboard", "⚙️ Controls"])

with main:
    st.subheader("Analytics Overview")
    col1, col2 = st.columns(2)
    col1.metric("Revenue", "$45,231", "12%")
    col2.metric("Users", "1,429", "3%")
    st.line_chart(data)

with sidebar:
    st.selectbox("Time Period", ["1D", "1W", "1M"])
    st.checkbox("Show Trends")
    st.button("Refresh Data")
```

### Width Tracking

```python
# Track column widths for dynamic layouts
result = adjustable_columns([2, 1], labels=["Content", "Sidebar"], return_widths=True)
content, sidebar = result['columns']
current_widths = result['widths']

st.info(f"Current ratios: {[f'{w:.1f}' for w in current_widths]}")

with content:
    st.write("Main content area")
    
with sidebar:
    st.write("Adjustable sidebar")
```

### Multiple Column Sets

```python
# Each set of columns needs a unique key
cols1 = adjustable_columns(3, labels=["A", "B", "C"], key="top")
cols2 = adjustable_columns([1, 2], labels=["Left", "Right"], key="bottom")

# First row
cols1[0].metric("Metric 1", "100")
cols1[1].metric("Metric 2", "200") 
cols1[2].metric("Metric 3", "300")

# Second row  
cols2[0].button("Action")
cols2[1].write("Content area")
```

### All Parameters

```python
columns = adjustable_columns(
    spec=[3, 2, 1],                    # Custom width ratios
    gap="large",                       # Large spacing
    vertical_alignment="center",       # Center-align content
    border=True,                       # Show column borders
    labels=["📊 Charts", "📋 Data", "⚙️ Tools"],  # Custom labels
    return_widths=True,               # Get width info
    key="advanced_example"            # Unique identifier
)

cols = columns['columns']
widths = columns['widths']
```

### Start with Some Columns Hidden

```python
# Start with the second column hidden
cols = adjustable_columns(
    [1, 1, 1],
    labels=["Main", "Side", "Tools"],
    initial_hidden=[False, True, False],
    key="hidden_example"
)

with cols[0]:
    st.write("Main column is visible!")
with cols[1]:
    st.write("Side column starts hidden!")
with cols[2]:
    st.write("Tools column is visible!")
```

## 🎨 Customization

### Column Labels

Customize the labels shown in resize handles:

```python
cols = adjustable_columns(
    3, 
    labels=["📈 Analytics", "🛠️ Tools", "📱 Mobile"]
)
```

### Responsive Layouts

Use width information for responsive behavior:

```python
result = adjustable_columns([2, 1], return_widths=True)
main_col, side_col = result['columns']
widths = result['widths']

# Adapt content based on current column width
if widths[0] > 3:  # Main column is wide
    main_col.plotly_chart(fig, use_container_width=True)
else:  # Main column is narrow
    main_col.write("Chart too narrow - expand column to view")
```

## 🔧 Development

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/danieljannai/streamlit-adjustable-columns
cd streamlit-adjustable-columns

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
make install-dev

# Or manually:
pip install -e ".[dev]"
cd streamlit_adjustable_columns/frontend
npm install
cd ../..
```

### Development Workflow

```bash
# Terminal 1: Start frontend development server
make frontend-dev  # Or: cd streamlit_adjustable_columns/frontend && npm start

# Terminal 2: Run the demo (make sure venv is activated)
source venv/bin/activate
streamlit run example.py
```

### What You'll See

1. **Frontend Dev Server**: http://localhost:3001
   - This serves the interactive column resizer component

2. **Streamlit App**: http://localhost:8501
   - Your main app with the adjustable columns

### Testing

The project includes comprehensive tests using pytest and Playwright:

```bash
# Run all tests
make test

# Run only unit tests
make test-unit

# Run only E2E tests  
make test-e2e

# Run with coverage
pytest --cov=streamlit_adjustable_columns
```

### Code Quality

```bash
# Format code
make format

# Check linting
make lint

# Run full check (format + lint + test)
make format && make lint && make test
```

### Building and Publishing

```bash
# Build the package
make build

# Upload to PyPI (requires credentials)
make upload
```

## 🐛 Troubleshooting

### Component shows "Loading..." forever
- Make sure the frontend dev server is running on port 3001
- Check that `_RELEASE = False` in `streamlit_adjustable_columns/__init__.py`

### "Module not found" error
- Make sure your virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `make install-dev`

### Frontend won't start
- Make sure Node.js and npm are installed
- Delete `node_modules` and run `npm install` again

### Port conflicts
- If port 3001 or 8501 are busy, kill other processes or change ports in the configuration

## 🧪 Test Coverage

The project includes comprehensive test coverage:

- **Unit Tests**: Test core functionality, parameter handling, and state management
- **Integration Tests**: Test component behavior with Streamlit integration
- **E2E Tests**: Test user interactions, resize functionality, and visual elements
- **Cross-browser Testing**: Firefox and Chromium support via Playwright

Test files are organized in the `tests/` directory:
- `tests/test_unit.py` - Unit tests for Python code
- `tests/test_integration.py` - Integration tests
- `tests/test_*.py` - E2E tests for specific features
- `tests/streamlit_apps/` - Test Streamlit applications

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. This is a brief overview of how to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`make install-dev`)
4. Make your changes and add tests
5. Run the test suite (`make test`)
6. Format your code (`make format`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

**For detailed contributing guidelines, development setup, testing procedures, and release processes, please see [CONTRIBUTING.md](CONTRIBUTING.md).**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Inspired by the need for flexible column layouts in Streamlit applications
- Developed with great assistance from [Cursor](https://cursor.com/) AI coding assistant

## 👨‍💻 Author

**Daniel Jannai Epstein**

- GitHub: [@danieljannai](https://github.com/danieljannai)
- Created this component to enhance Streamlit's column functionality

---

**Made with ❤️ for the Streamlit community** 
