import streamlit as st

from streamlit_adjustable_columns import adjustable_columns

st.subheader("Test Adjustable Columns with Custom Ratios")

# Columns with custom width ratios
col1, col2 = adjustable_columns(
    [3, 1], labels=["Main Content", "Sidebar"], key="ratios_test"
)

with col1:
    st.write("Main content area (3:1 ratio)")
    st.text_area("Large text area", "This is the main content area with more space")

with col2:
    st.write("Sidebar (3:1 ratio)")
    st.button("Button 1")
    st.button("Button 2")
