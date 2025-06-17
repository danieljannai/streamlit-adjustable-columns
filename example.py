import streamlit as st
from streamlit_expandable_columns import expandable_columns

# Set page config
st.set_page_config(page_title="Expandable Columns Demo", layout="wide")

st.title("🎛️ Streamlit Expandable Columns Demo")

st.markdown("""
This demo showcases the **Streamlit Expandable Columns** component, which allows you to create 
columns with adjustable widths that persist when other page elements change.

### Features:
- ✅ **Draggable column separators** - Click and drag to resize
- ✅ **Persistent widths** - Column proportions are maintained when page updates
- ✅ **Minimum width constraints** - Prevents columns from becoming too narrow
- ✅ **Responsive design** - Works on different screen sizes
- ✅ **Multiple column configurations** - Support for 2, 3, 4+ columns
""")

st.markdown("---")

# Example 1: Basic two-column layout
st.header("Example 1: Basic Two-Column Layout")
st.markdown("Drag the separator between the columns to adjust their widths.")

result1 = expandable_columns([1, 1], key="basic_two_columns")
col1, col2 = result1['columns']

with col1:
    st.subheader("Left Column")
    st.write("This is the left column content.")
    st.button("Button in Left Column", key="btn1")
    st.selectbox("Select an option:", ["Option 1", "Option 2", "Option 3"], key="select1")

with col2:
    st.subheader("Right Column")
    st.write("This is the right column content.")
    st.slider("Slider:", 0, 100, 50, key="slider1")
    st.text_area("Text area:", "Type something here...", key="text1")

st.markdown("---")

# Example 2: Three-column layout with different initial widths
st.header("Example 2: Three-Column Layout (1:2:1 ratio)")
st.markdown("This example starts with a 1:2:1 width ratio.")

result2 = expandable_columns([1, 2, 1], key="three_columns")
col1, col2, col3 = result2['columns']

with col1:
    st.subheader("Narrow")
    st.write("Small column")
    st.checkbox("Checkbox", key="check1")

with col2:
    st.subheader("Wide Column")
    st.write("This is the wider middle column.")
    st.bar_chart({"A": [1, 2, 3], "B": [2, 4, 6]})

with col3:
    st.subheader("Narrow")
    st.write("Small column")
    st.radio("Radio:", ["A", "B", "C"], key="radio1")

st.markdown("---")

# Example 3: Four-column layout
st.header("Example 3: Four-Column Layout")
st.markdown("Equal width columns that can be adjusted.")

result3 = expandable_columns([1, 1, 1, 1], key="four_columns")
col1, col2, col3, col4 = result3['columns']

with col1:
    st.subheader("Col 1")
    st.metric("Metric 1", "123", "12%")

with col2:
    st.subheader("Col 2")
    st.metric("Metric 2", "456", "-5%")

with col3:
    st.subheader("Col 3")
    st.metric("Metric 3", "789", "8%")

with col4:
    st.subheader("Col 4")
    st.metric("Metric 4", "012", "3%")

st.markdown("---")

# Example 4: Advanced configuration with minimum widths
st.header("Example 4: Advanced Configuration")
st.markdown("Columns with custom minimum widths (20% minimum for each column).")

advanced_config = {
    'widths': [2, 3, 1],
    'min_widths': [0.2, 0.2, 0.2]  # 20% minimum width for each column
}

result4 = expandable_columns(advanced_config, key="advanced_columns")
col1, col2, col3 = result4['columns']

with col1:
    st.subheader("Min 20% Width")
    st.info("This column cannot be resized below 20% of the total width.")

with col2:
    st.subheader("Main Content")
    st.success("This is the main content area with more initial space.")
    st.line_chart({"Data": [1, 3, 2, 4, 5, 3, 6]})

with col3:
    st.subheader("Sidebar")
    st.warning("This is a sidebar area.")
    st.write("Controls go here.")

st.markdown("---")

# Example 5: Collapsible sidebar with zero minimum width
st.header("Example 5: Collapsible Sidebar")
st.markdown("**The left and right sidebars can be completely collapsed** (min_width = 0). Try dragging the separators all the way to collapse them!")

collapsible_config = {
    'widths': [1, 3, 1],
    'min_widths': [0, 0.15, 0],  # Left and right columns can collapse to 0 width
}

result5 = expandable_columns(collapsible_config, key="collapsible_columns")
col1, col2, col3 = result5['columns']

with col1:
    st.subheader("📋 Collapsible Sidebar")
    st.write("This sidebar can be completely hidden!")
    st.selectbox("Filter by:", ["All", "Active", "Inactive"], key="filter1")
    st.checkbox("Show advanced options", key="advanced_opts")
    
    if st.button("🔄 Reset Layout", key="reset_btn"):
        st.rerun()

with col2:
    st.subheader("📊 Main Dashboard")
    st.write("This is the main content area that expands when the sidebar is collapsed.")
    
    # Sample data
    import pandas as pd
    import numpy as np
    
    # Create sample chart data
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Series A', 'Series B', 'Series C']
    )
    
    st.area_chart(chart_data)
    
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.metric("Total Users", "1,234", "12%")
        st.metric("Revenue", "$56,789", "8%")
    with col2_2:
        st.metric("Conversion Rate", "3.2%", "-0.3%")
        st.metric("Active Sessions", "89", "15%")

with col3:
    st.subheader("🔧 Tools")
    st.write("Tool panel with minimum 15% width.")
    st.button("🔄 Refresh Data", key="refresh_btn")
    st.button("📥 Export", key="export_btn")
    st.button("⚙️ Settings", key="settings_btn")
    
    st.markdown("**Status:**")
    st.success("✅ System Online")
    st.info("🔄 Last updated: 2 min ago")

st.markdown("---")

# Display current column widths
st.header("Column Width Information")
st.markdown("Current column widths (as ratios):")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.subheader("Example 1 - Two Columns")
    st.write(f"Widths: {result1['widths']}")
    
    st.subheader("Example 2 - Three Columns")  
    st.write(f"Widths: {result2['widths']}")
    
    st.subheader("Example 3 - Four Columns")
    st.write(f"Widths: {result3['widths']}")

with col_info2:
    st.subheader("Example 4 - Advanced")
    st.write(f"Widths: {result4['widths']}")
    
    st.subheader("Example 5 - Collapsible")
    st.write(f"Widths: {result5['widths']}")
    if result5['widths'][0] < 0.01:  # First column is practically collapsed
        st.success("🎉 Sidebar is collapsed!")

st.markdown("---")

# Instructions
st.header("How to Use")
st.markdown("""
### Installation
```bash
pip install streamlit-expandable-columns
```

### Basic Usage
```python
import streamlit as st
from streamlit_expandable_columns import expandable_columns

# Create expandable columns
result = expandable_columns([1, 2, 1], key="my_columns")
col1, col2, col3 = result['columns']

# Use columns normally
with col1:
    st.write("Column 1 content")
    
with col2:
    st.write("Column 2 content")
    
with col3:
    st.write("Column 3 content")

# Access current widths
current_widths = result['widths']
```

### Advanced Configuration
```python
# With minimum widths
config = {
    'widths': [2, 3, 1],
    'min_widths': [0.15, 0.15, 0.15]  # 15% minimum each
}
result = expandable_columns(config, key="advanced")
```

### Collapsible Columns
```python
# Column that can be completely collapsed (min_width = 0)
collapsible_config = {
    'widths': [1, 3, 1],
    'min_widths': [0, 0.15, 0.15]  # First column can collapse to 0
}
result = expandable_columns(collapsible_config, key="collapsible")
```
""")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit") 