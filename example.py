import streamlit as st
import pandas as pd
import numpy as np
from streamlit_expandable_columns import expandable_columns

# Set page config
st.set_page_config(page_title="Expandable Columns Demo", layout="wide")

st.title("🎯 Streamlit Expandable Columns Demo")
st.markdown("This component works exactly like `st.columns` but with a **draggable control bar** to adjust column widths!")

st.divider()

# Example 1: Basic usage with custom labels
st.subheader("📊 Example 1: Custom Labels")
st.code("""
col1, col2, col3 = expandable_columns(3, labels=["📈 Charts", "📋 Data", "⚙️ Settings"])

with col1:
    st.metric("Sales", "$1,234", "12%")
    
col2.metric("Users", "5,678", "-2%")
col3.metric("Revenue", "$9,012", "8%")
""")

col1, col2, col3 = expandable_columns(3, labels=["📈 Charts", "📋 Data", "⚙️ Settings"], key="example1")

with col1:
    st.metric("Sales", "$1,234", "12%")
    st.line_chart(np.random.randn(20, 1).cumsum())

col2.metric("Users", "5,678", "-2%")
col2.bar_chart(np.random.randn(20, 1))

col3.metric("Revenue", "$9,012", "8%")
col3.area_chart(np.random.randn(20, 1).cumsum())

st.divider()

# Example 2: Dashboard layout with descriptive labels
st.subheader("📈 Example 2: Dashboard Layout")
st.code("""
main, sidebar = expandable_columns([4, 1], labels=["🎛️ Main Dashboard", "🔧 Controls"])

with main:
    st.subheader("Analytics Overview")
    # ... main content
    
with sidebar:
    st.subheader("Filters & Settings")
    # ... sidebar controls
""")

main, sidebar = expandable_columns([4, 1], labels=["🎛️ Main Dashboard", "🔧 Controls"], key="example2")

with main:
    st.subheader("📊 Analytics Overview")
    
    # Create sample data
    chart_data = pd.DataFrame(
        np.random.randn(20, 3) + [1, 0.5, -0.5],
        columns=['Product A', 'Product B', 'Product C']
    ).cumsum()
    
    # Metrics row
    met1, met2, met3, met4 = st.columns(4)
    met1.metric("Revenue", "$45,231", "12%")
    met2.metric("Orders", "1,429", "3%") 
    met3.metric("Customers", "321", "8%")
    met4.metric("Conversion", "3.2%", "-0.1%")
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Sales Trends")
        st.line_chart(chart_data)
    
    with col_chart2:
        st.subheader("Product Performance")
        chart_data2 = pd.DataFrame({
            'Product': ['A', 'B', 'C', 'D'],
            'Sales': [23, 45, 56, 78]
        })
        st.bar_chart(chart_data2.set_index('Product'))

with sidebar:
    st.subheader("🔧 Filters & Settings")
    
    with st.expander("📅 Date Range", expanded=True):
        date_range = st.date_input("Select period:", [])
    
    with st.expander("🏷️ Categories"):
        categories = st.multiselect("Product categories:", 
                                   ["Electronics", "Clothing", "Home", "Books"])
    
    with st.expander("📊 Display Options"):
        show_trend = st.checkbox("Show trend lines", True)
        chart_type = st.radio("Chart style:", ["Line", "Bar", "Area"])
        
    st.info("💡 **Tip:** Drag the control bar above to resize the dashboard layout!")

st.divider()

# Example 3: New return_widths feature
st.subheader("🔢 Example 3: Width Information")
st.code("""
# Get both columns and their current widths
result = expandable_columns([2, 1, 1], labels=["Main", "Side", "Tools"], return_widths=True)
cols = result['columns']
widths = result['widths']

# Display current ratios
st.write(f"Current width ratios: {[round(w, 2) for w in widths]}")
""")

# Use return_widths to get both columns and width information
result = expandable_columns([2, 1, 1], labels=["Main Content", "Sidebar", "Tools"], return_widths=True, key="example3")
cols = result['columns']
current_widths = result['widths']

# Show current widths
st.info(f"**Current width ratios:** {[round(w, 2) for w in current_widths]} (try dragging to see changes)")

cols[0].subheader("📄 Main Content")
cols[0].write("This column adjusts its width based on your dragging. The ratios update in real-time!")
cols[0].write("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

cols[1].subheader("📋 Sidebar")
cols[1].write("Sidebar content")
cols[1].button("Action", key="btn1")

cols[2].subheader("🔧 Tools")
cols[2].write("Tools panel")
cols[2].button("Settings", key="btn2")

st.divider()

# Example 4: All parameters with labels
st.subheader("🎨 Example 4: All Parameters with Labels")
st.code("""
cols = expandable_columns(
    spec=[2, 1, 1], 
    gap="large", 
    vertical_alignment="center",
    border=True,
    labels=["🎯 Main Content", "📝 Notes", "🔗 Links"]
)
""")

# Parameter controls
col_params1, col_params2 = st.columns(2)
with col_params1:
    gap = st.selectbox("Gap size:", ["small", "medium", "large"], index=2)
    vertical_alignment = st.selectbox("Vertical alignment:", ["top", "center", "bottom"], index=1)

with col_params2:
    border = st.checkbox("Show borders", value=True)
    custom_labels = st.text_input("Custom labels (comma-separated):", "🎯 Main Content,📝 Notes,🔗 Links")

# Parse custom labels
try:
    labels_list = [label.strip() for label in custom_labels.split(',')]
    if len(labels_list) != 3:
        labels_list = ["🎯 Main Content", "📝 Notes", "🔗 Links"]
except:
    labels_list = ["🎯 Main Content", "📝 Notes", "🔗 Links"]

# Create columns with selected parameters
cols = expandable_columns(
    spec=[2, 1, 1], 
    gap=gap, 
    vertical_alignment=vertical_alignment,
    border=border,
    labels=labels_list,
    key="example4"
)

cols[0].subheader("Main Content Area")
cols[0].write("This is the primary content area with more space allocated.")
cols[0].write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")

cols[1].subheader("Quick Notes")
cols[1].write("Shorter content")
cols[1].button("Action Button", key="btn3")

cols[2].subheader("Links & Info")
cols[2].write("Side info")
cols[2].button("Settings", key="btn4")

st.divider()

# Example 5: Content types example
st.subheader("🏗️ Example 5: Content-Based Layout")
st.code("""
content, media, meta = expandable_columns(
    [3, 2, 1], 
    labels=["📄 Article Content", "🖼️ Media Gallery", "📊 Metadata"],
    gap="medium"
)
""")

content, media, meta = expandable_columns(
    [3, 2, 1], 
    labels=["📄 Article Content", "🖼️ Media Gallery", "📊 Metadata"],
    gap="medium",
    key="example5"
)

with content:
    st.subheader("📄 Article Content")
    st.write("""
    # Sample Article Title
    
    This is the main content area where you would place your article text, 
    blog posts, or primary information. The expandable columns allow you to 
    adjust how much space is dedicated to different types of content.
    
    ## Key Features
    - Custom column labels with emojis
    - Draggable width controls
    - Streamlit theme integration
    - All st.columns parameters supported
    - New `return_widths` parameter for getting current ratios
    """)

with media:
    st.subheader("🖼️ Media Gallery")
    
    # Sample charts as "media"
    tab1, tab2 = st.tabs(["Charts", "Images"])
    
    with tab1:
        st.area_chart(np.random.randn(15, 2))
    
    with tab2:
        st.info("📸 Image gallery would go here")
        st.write("• Image 1.jpg")
        st.write("• Image 2.jpg") 
        st.write("• Image 3.jpg")

with meta:
    st.subheader("📊 Metadata")
    
    st.metric("Word Count", "1,247")
    st.metric("Read Time", "5 min")
    st.metric("Views", "2,431")
    
    with st.expander("Tags"):
        st.write("• streamlit")
        st.write("• columns")
        st.write("• ui")
    
    st.button("Share", use_container_width=True)

st.divider()

# Example 6: Multiple columns with different widths
st.header("🔢 Example 6: Many Columns")
st.write("Testing with 5 columns - great for dashboards with multiple widgets:")

result6 = expandable_columns(
    spec=[3, 2, 1, 2, 1], 
    labels=["📊 Charts", "🎛️ Controls", "📈 Stats", "🗂️ Data", "⚙️ Tools"],
    gap="small",
    return_widths=True,
    key="example6"
)

cols6 = result6['columns']
widths6 = result6['widths']

with cols6[0]:
    st.write("**Main Chart Area**")
    st.info("📊 Primary visualizations go here")
    st.line_chart(np.random.randn(10, 1).cumsum())
    
with cols6[1]:
    st.write("**Control Panel**")
    st.selectbox("Chart Type", ["Line", "Bar", "Scatter"], key="chart_type_6")
    st.slider("Smoothing", 0.1, 1.0, 0.5, key="smoothing_6")
    
with cols6[2]:
    st.write("**Key Metrics**")
    st.metric("Users", "1,234", "+12%")
    st.metric("Sales", "$45K", "+8%")
    
with cols6[3]:
    st.write("**Data Explorer**")
    st.write("🗂️ Browse datasets")
    st.selectbox("Dataset", ["Sales", "Users", "Products"], key="dataset_6")
    
with cols6[4]:
    st.write("**Settings**")
    st.checkbox("Auto-refresh", key="auto_refresh_6")
    st.checkbox("Dark mode", key="dark_mode_6")

st.info(f"**5-column layout widths:** {[f'{w:.2f}' for w in widths6]} - Try compressing columns to test 6% minimum!")

st.divider()

# Instructions
st.subheader("🎯 How to Use")
st.markdown("""
### 🆕 **New Features:**
- **Custom Labels**: Use the `labels` parameter to set descriptive titles for each column
- **Theme Integration**: Automatically matches your Streamlit theme colors
- **Width Information**: Use `return_widths=True` to get current column ratios
- **Better Alignment**: Control bar now perfectly aligns with column boundaries

### 📖 **Basic Usage:**
```python
# With custom labels (default behavior)
cols = expandable_columns(3, labels=["Main", "Sidebar", "Tools"])

# Get width information
result = expandable_columns([2, 1], labels=["Content", "Sidebar"], return_widths=True)
columns = result['columns']
current_widths = result['widths']  # [2.0, 1.0] initially, [1.5, 1.5] after resizing

# With all parameters
cols = expandable_columns(
    spec=[2, 1], 
    labels=["📊 Dashboard", "⚙️ Settings"],
    gap="large",
    vertical_alignment="top",
    border=True,
    return_widths=False  # default
)
```

### 🎮 **How to Resize:**
1. **Look for the control bar** above each set of expandable columns
2. **Hover over the dividers** between segments - they'll highlight  
3. **Click and drag** to resize the columns
4. **Release** to apply the new layout

### ⚙️ **Supported Parameters:**
- `spec`: Number of columns (int) or width ratios (list)
- `labels`: Custom titles for each column (list of strings)  
- `gap`: "small", "medium", or "large"
- `vertical_alignment`: "top", "center", or "bottom"
- `border`: True/False to show column borders
- `return_widths`: True/False to return width information (optional)
- `key`: Unique key for the component (optional)

**Note:** All columns have a minimum width of 6% to ensure usability.
""")

st.success("🎉 The columns now have perfect alignment and the new return_widths feature!")
st.markdown("Made with ❤️ using Streamlit") 