import streamlit as st
from streamlit_expandable_columns import expandable_columns

st.subheader("Test Expandable Columns with Labels")

# Columns with custom labels
col1, col2, col3 = expandable_columns(
    3, 
    labels=["📊 Charts", "📋 Data", "⚙️ Settings"],
    key="labels_test"
)

with col1:
    st.write("Charts section")
    st.bar_chart({"a": [1, 2, 3], "b": [2, 3, 1]})

with col2:
    st.write("Data section")
    st.dataframe({"col1": [1, 2, 3], "col2": [4, 5, 6]})

with col3:
    st.write("Settings section")
    st.selectbox("Option", ["A", "B", "C"]) 