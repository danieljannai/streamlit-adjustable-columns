import streamlit as st

from streamlit_adjustable_columns import adjustable_columns

st.subheader("Test Basic Adjustable Columns")

# Basic 3-column layout
col1, col2, col3 = adjustable_columns(3, key="basic_test")

with col1:
    st.write("Column 1 Content")
    st.metric("Metric 1", "100")

with col2:
    st.write("Column 2 Content")
    st.metric("Metric 2", "200")

with col3:
    st.write("Column 3 Content")
    st.metric("Metric 3", "300")
