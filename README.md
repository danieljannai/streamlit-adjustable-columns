# Streamlit Expandable Columns

A Streamlit custom component that creates columns with adjustable widths. Users can drag column separators to resize columns, and the adjustments persist when other page elements change.

![Demo](https://img.shields.io/badge/demo-available-brightgreen)
![Python](https://img.shields.io/badge/python-3.7+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.0+-red)

## Features

- 🎛️ **Draggable column separators** - Click and drag to resize columns
- 💾 **Persistent widths** - Column proportions are maintained when page updates
- 📏 **Minimum width constraints** - Prevents columns from becoming too narrow
- 📱 **Responsive design** - Works on different screen sizes
- 🔢 **Multiple column configurations** - Support for 2, 3, 4+ columns
- ⚙️ **Customizable** - Set initial widths and minimum width constraints

## Installation

```bash
pip install streamlit-expandable-columns
```

## Quick Start

```python
import streamlit as st
from streamlit_expandable_columns import expandable_columns

st.title("My App with Resizable Columns")

# Create expandable columns
result = expandable_columns([1, 2, 1], key="my_columns")
col1, col2, col3 = result['columns']

# Use columns like normal Streamlit columns
with col1:
    st.header("Left Sidebar")
    st.selectbox("Options:", ["A", "B", "C"])

with col2:
    st.header("Main Content")
    st.write("This is the main content area")
    st.line_chart([1, 2, 3, 4, 5])

with col3:
    st.header("Right Sidebar")
    st.button("Action Button")

# Access current column widths
st.write(f"Current widths: {result['widths']}")
```

## Usage Examples

### Basic Two-Column Layout

```python
result = expandable_columns([1, 1], key="two_columns")
col1, col2 = result['columns']

with col1:
    st.write("Left column content")

with col2:
    st.write("Right column content")
```

### Three Columns with Different Initial Widths

```python
# Create columns with 1:2:1 ratio
result = expandable_columns([1, 2, 1], key="three_columns")
col1, col2, col3 = result['columns']
```

### Advanced Configuration with Minimum Widths

```python
config = {
    'widths': [2, 3, 1],           # Initial width ratios
    'min_widths': [0.2, 0.2, 0.2]  # Minimum 20% width for each column
}

result = expandable_columns(config, key="advanced_columns")
col1, col2, col3 = result['columns']
```

## API Reference

### `expandable_columns(columns_config=None, key=None)`

Creates columns with adjustable widths.

**Parameters:**

- `columns_config` (list or dict, optional): 
  - **List**: Initial width ratios (e.g., `[1, 2, 1]` for 3 columns with 1:2:1 ratio)
  - **Dict**: Configuration with `'widths'` and optional `'min_widths'` keys
  - **None** (default): Creates 2 equal columns `[1, 1]`

- `key` (str, optional): Unique key for the component. Required for state persistence.

**Returns:**

Dictionary containing:
- `'widths'`: Current width ratios of columns (list of numbers)
- `'columns'`: List of Streamlit column objects for content placement
- `'component_value'`: Raw component return value (for advanced use)

## Development

### Setting up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/danieljannai/streamlit-expandable-columns.git
cd streamlit-expandable-columns
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Install frontend dependencies and start development server:
```bash
cd streamlit_expandable_columns/frontend
npm install
npm start
```

5. In another terminal, activate venv and run the example:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
streamlit run example.py
```

**Quick Setup with Script:**
```bash
./dev_setup.sh  # Handles venv creation and all dependencies
```

### Building for Production

1. Build the frontend:
```bash
cd streamlit_expandable_columns/frontend
npm run build
```

2. Update the `_RELEASE` flag in `__init__.py` to `True`

3. Build and distribute:
```bash
python setup.py sdist bdist_wheel
```

## How It Works

The component consists of:

1. **Python Backend** (`streamlit_expandable_columns/__init__.py`):
   - Interfaces with Streamlit's component system
   - Manages column configuration and state
   - Creates actual Streamlit columns with current widths

2. **JavaScript Frontend** (`frontend/src/main.js`):
   - Renders interactive column separators
   - Handles drag-and-drop resize functionality
   - Communicates width changes back to Python

3. **Visual Interface** (`frontend/public/index.html`):
   - Displays resizable column headers
   - Provides visual feedback during resizing

## Browser Compatibility

- Chrome/Chromium 70+
- Firefox 65+
- Safari 12+
- Edge 79+

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Guidelines

1. Follow PEP 8 for Python code
2. Use ESLint configuration for JavaScript
3. Add tests for new features
4. Update documentation for API changes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v0.1.0
- Initial release
- Basic column resizing functionality
- Support for 2-8 columns
- Minimum width constraints
- Responsive design

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/danieljannai/streamlit-expandable-columns/issues) page
2. Create a new issue with:
   - Python version
   - Streamlit version
   - Browser information
   - Minimal code example
   - Error messages (if any)

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [streamlit-component-lib](https://github.com/streamlit/streamlit/tree/develop/component-lib/src/streamlit-component-lib)
- Inspired by traditional desktop application splitter panels 