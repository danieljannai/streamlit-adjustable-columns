import streamlit as st
from streamlit_expandable_columns import expandable_columns

st.set_page_config(page_title="Simple Test", layout="wide")

st.title("🧪 Simple Resizable Columns Test")

st.markdown("**Drag the resize handles above the columns to adjust their widths!**")

# Test 1: Basic 3 columns
st.subheader("Test 1: Three Equal Columns")
col1, col2, col3 = expandable_columns(3, labels=["Left", "Center", "Right"], key="test1")

with col1:
    st.write("**Left Column**")
    st.info("This is the left column content")
    st.button("Left Button", key="left_btn")

with col2:
    st.write("**Center Column**")
    st.success("This is the center column content")
    st.slider("Center Slider", 0, 100, 50, key="center_slider")

with col3:
    st.write("**Right Column**")
    st.warning("This is the right column content")
    st.selectbox("Right Select", ["A", "B", "C"], key="right_select")

st.divider()

# Test 2: Different proportions with width tracking
st.subheader("Test 2: Different Proportions with Width Tracking")
result = expandable_columns([2, 1], labels=["Main", "Sidebar"], return_widths=True, key="test2")
main_col, side_col = result['columns']
current_widths = result['widths']

st.info(f"Current width ratios: {[round(w, 2) for w in current_widths]}")

with main_col:
    st.write("**Main Content Area**")
    st.write("This area gets more space initially but can be resized.")
    st.text_area("Enter some text:", "Sample content here...", key="main_text")

with side_col:
    st.write("**Sidebar**")
    st.write("Smaller sidebar area")
    st.checkbox("Option 1", key="opt1")
    st.checkbox("Option 2", key="opt2")

st.divider()

# Test 3: With borders
st.subheader("Test 3: With Borders")
col_a, col_b = expandable_columns(2, labels=["Column A", "Column B"], border=True, gap="large", key="test3")

col_a.metric("Metric A", "1,234", "12%")
col_b.metric("Metric B", "5,678", "-3%")

st.success("✅ If you can see resize handles above each set of columns and can drag them to adjust column widths, the implementation is working!") 