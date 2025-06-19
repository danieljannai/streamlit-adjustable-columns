import streamlit as st

from streamlit_expandable_columns import expandable_columns

st.subheader("Test Expandable Columns with Width Tracking")

# Columns with width tracking
result = expandable_columns(
    3,
    labels=["Col A", "Col B", "Col C"],
    return_widths=True,
    key="widths_test",
)

columns = result["columns"]
widths = result["widths"]

st.info(f"Current width ratios: {[f'{w:.2f}' for w in widths]}")

with columns[0]:
    st.write("Column A")
    st.write(f"Width: {widths[0]:.2f}")

with columns[1]:
    st.write("Column B")
    st.write(f"Width: {widths[1]:.2f}")

with columns[2]:
    st.write("Column C")
    st.write(f"Width: {widths[2]:.2f}")
