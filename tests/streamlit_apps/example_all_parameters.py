import streamlit as st

from streamlit_expandable_columns import expandable_columns

st.subheader("Test Expandable Columns with All Parameters")

# Columns with all parameters
result = expandable_columns(
    spec=[2, 1, 1],
    gap="large",
    vertical_alignment="center",
    border=True,
    labels=["📊 Main", "📋 Info", "⚙️ Tools"],
    return_widths=True,
    key="all_params_test",
)

columns = result["columns"]
widths = result["widths"]

st.write(f"**Gap:** large, **Alignment:** center, **Border:** True")
st.write(f"**Current widths:** {[f'{w:.2f}' for w in widths]}")

with columns[0]:
    st.write("Main section with large content")
    st.plotly_chart(
        {"data": [{"y": [1, 2, 3], "type": "bar"}]}, use_container_width=True
    )

with columns[1]:
    st.write("Info section")
    st.info("Information box")

with columns[2]:
    st.write("Tools section")
    st.button("Tool 1")
    st.button("Tool 2")
