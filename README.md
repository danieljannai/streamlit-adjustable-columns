# 🎯 Streamlit Expandable Columns

[![PyPI version](https://badge.fury.io/py/streamlit-expandable-columns.svg)](https://badge.fury.io/py/streamlit-expandable-columns)
[![Test](https://github.com/danieljannai/streamlit-expandable-columns/actions/workflows/test.yml/badge.svg)](https://github.com/danieljannai/streamlit-expandable-columns/actions/workflows/test.yml)

**Version:** 0.1.1

Create resizable columns in Streamlit! This component provides `st.columns` functionality with **draggable resize handles** that allow users to adjust column widths dynamically.

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
pip install streamlit-expandable-columns
```

**Note**: Packages installed from PyPI already include the compiled frontend so no additional tools are required. If you install from a source checkout (e.g. GitHub), Node.js and npm are needed to build the frontend assets.

### Basic Usage

```python
import streamlit as st
from streamlit_expandable_columns import expandable_columns

# Use exactly like st.columns - but with resize handles!
col1, col2, col3 = expandable_columns(3, labels=["📊 Charts", "📋 Data", "⚙️ Settings"])

with col1:
    st.metric("Sales", "$1,234", "12%")
    
col2.write("This column can be resized!")
col3.button("Settings")
```

## 📖 API Reference

### `expandable_columns(spec, *, gap="small", vertical_alignment="top", border=False, labels=None, return_widths=False, key=None)`

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
- **`key`** (str): Unique component key (recommended for multiple instances)

#### Returns

- **Default**: List of column containers (same as `st.columns`)
- **With `return_widths=True`**: Dict with `{'columns': [...], 'widths': [...]}`

## 🎮 How to Resize

1. **Look for resize handles** above each set of expandable columns
2. **Hover over the boundaries** between column areas - you'll see resize cursors
3. **Click and drag** the handles to adjust column widths
4. **Release** to apply changes - they persist across app reruns!

## 📚 Examples

### Dashboard Layout

```python
# Create a dashboard with resizable main content and sidebar
main, sidebar = expandable_columns([4, 1], labels=["📊 Dashboard", "⚙️ Controls"])

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
result = expandable_columns([2, 1], labels=["Content", "Sidebar"], return_widths=True)
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
cols1 = expandable_columns(3, labels=["A", "B", "C"], key="top")
cols2 = expandable_columns([1, 2], labels=["Left", "Right"], key="bottom")

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
columns = expandable_columns(
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

## 🎨 Customization

### Column Labels

Customize the labels shown in resize handles:

```python
cols = expandable_columns(
    3, 
    labels=["📈 Analytics", "🛠️ Tools", "📱 Mobile"]
)
```

### Responsive Layouts

Use width information for responsive behavior:

```python
result = expandable_columns([2, 1], return_widths=True)
main_col, side_col = result['columns']
widths = result['widths']

# Adapt content based on current column width
if widths[0] > 3:  # Main column is wide
    main_col.plotly_chart(fig, use_container_width=True)
else:  # Main column is narrow
    main_col.write("Chart too narrow - expand column to view")
```

## 🔧 Development

### Setup

```bash
# Clone the repository
git clone https://github.com/your-username/streamlit-expandable-columns
cd streamlit-expandable-columns

# Install in development mode
make install-dev

# Start the frontend development server
make frontend-dev

# In another terminal, run Streamlit
streamlit run example.py
```

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
pytest --cov=streamlit_expandable_columns
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

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`make install-dev`)
4. Make your changes and add tests
5. Run the test suite (`make test`)
6. Format your code (`make format`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Inspired by the need for flexible column layouts in Streamlit applications
- Thanks to the Streamlit community for feedback and suggestions

---

**Made with ❤️ for the Streamlit community** 
