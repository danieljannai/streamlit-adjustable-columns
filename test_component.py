#!/usr/bin/env python3
"""
Test script for the streamlit-expandable-columns component.
This validates all the new functionality and API compatibility.
"""

import streamlit as st
import pandas as pd
import numpy as np
from streamlit_expandable_columns import expandable_columns

st.set_page_config(page_title="Component Tests", layout="wide")

st.title("🧪 Streamlit Expandable Columns - Test Suite")
st.markdown("This page tests all the functionality of the expandable columns component.")

st.divider()

# Test 1: Basic integer spec
st.subheader("Test 1: Integer Spec")
st.write("Testing `expandable_columns(3)` - should create 3 equal columns")

try:
    cols = expandable_columns(3, key="test1")
    st.success(f"✅ Created {len(cols)} columns successfully")
    
    for i, col in enumerate(cols):
        col.write(f"Column {i+1}")
        col.metric(f"Metric {i+1}", f"{100*(i+1)}", f"{i+1}%")
        
except Exception as e:
    st.error(f"❌ Test 1 failed: {e}")

st.divider()

# Test 2: List spec  
st.subheader("Test 2: List Spec")
st.write("Testing `expandable_columns([2, 1, 3])` - should create columns with 2:1:3 ratio")

try:
    cols = expandable_columns([2, 1, 3], key="test2")
    st.success(f"✅ Created {len(cols)} columns successfully")
    
    expected_widths = [2, 1, 3]
    for i, col in enumerate(cols):
        col.write(f"Column {i+1} (width: {expected_widths[i]})")
        col.progress((expected_widths[i] / sum(expected_widths)))
        
except Exception as e:
    st.error(f"❌ Test 2 failed: {e}")

st.divider()

# Test 3: All st.columns parameters
st.subheader("Test 3: All Parameters")
st.write("Testing all st.columns parameters")

try:
    cols = expandable_columns(
        spec=[1, 1, 1],
        gap="large",
        vertical_alignment="center", 
        border=True,
        labels=["Short", "Medium", "Long Content"],
        key="test3"
    )
    st.success("✅ All parameters accepted successfully")
    
    for i, col in enumerate(cols):
        with col:
            st.write(f"**Column {i+1}**")
            if i == 0:
                st.write("Short")
            elif i == 1:
                st.write("Medium length content here")
            else:
                st.write("This is longer content to test vertical alignment properly")
                
except Exception as e:
    st.error(f"❌ Test 3 failed: {e}")

st.divider()

# Test 4: Context manager usage
st.subheader("Test 4: Context Manager Usage")
st.write("Testing `with col:` syntax")

try:
    col1, col2 = expandable_columns(2, key="test4")
    
    with col1:
        st.write("✅ Inside context manager 1")
        st.button("Button 1", key="ctx_btn1")
        
    with col2:
        st.write("✅ Inside context manager 2") 
        st.button("Button 2", key="ctx_btn2")
        
    st.success("✅ Context managers working correctly")
    
except Exception as e:
    st.error(f"❌ Test 4 failed: {e}")

st.divider()

# Test 5: Direct method calls
st.subheader("Test 5: Direct Method Calls")
st.write("Testing direct method calls on column objects")

try:
    col1, col2, col3 = expandable_columns(3, key="test5")
    
    col1.write("✅ Direct write call")
    col1.metric("Direct Metric", "123", "5%")
    
    col2.subheader("Direct subheader")
    col2.info("Direct info message")
    
    col3.success("Direct success message")
    col3.checkbox("Direct checkbox", key="direct_check")
    
    st.success("✅ Direct method calls working correctly")
    
except Exception as e:
    st.error(f"❌ Test 5 failed: {e}")

st.divider()

# Test 6: Complex content
st.subheader("Test 6: Complex Content")
st.write("Testing complex Streamlit components inside expandable columns")

try:
    main, sidebar = expandable_columns([3, 1], gap="medium", key="test6")
    
    with main:
        st.subheader("Charts and Data")
        
        # Create sample data
        df = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['A', 'B', 'C']
        )
        
        # Tabs inside expandable columns
        tab1, tab2 = st.tabs(["Line Chart", "Data"])
        
        with tab1:
            st.line_chart(df)
            
        with tab2:
            st.dataframe(df, use_container_width=True)
    
    with sidebar:
        st.subheader("Controls")
        
        # Various widgets
        option = st.selectbox("Select:", ["A", "B", "C"], key="complex_select")
        value = st.slider("Value:", 0, 100, 50, key="complex_slider")
        
        if st.button("Generate New Data", key="complex_btn"):
            st.success("✅ Button clicked!")
        
        # Expander inside expandable column
        with st.expander("More Options"):
            st.write("Nested content works!")
            st.radio("Radio:", ["X", "Y", "Z"], key="complex_radio")
    
    st.success("✅ Complex content rendering correctly")
    
except Exception as e:
    st.error(f"❌ Test 6 failed: {e}")

st.divider()

# Test 7: Error handling
st.subheader("Test 7: Error Handling")
st.write("Testing error conditions")

# Test invalid spec
try:
    cols = expandable_columns(-1)
    st.error("❌ Should have failed with negative spec")
except Exception as e:
    st.success(f"✅ Correctly caught error: {type(e).__name__}")

# Test empty spec
try:
    cols = expandable_columns([])
    st.error("❌ Should have failed with empty spec")
except Exception as e:
    st.success(f"✅ Correctly caught error: {type(e).__name__}")

# Test mismatched labels
try:
    cols = expandable_columns([1, 1], labels=["OnlyOne"], key="error_test")
    st.error("❌ Should have failed with mismatched labels length")
except Exception as e:
    st.success(f"✅ Correctly caught error: {type(e).__name__}")

st.divider()

# Test 8: Backward compatibility
st.subheader("Test 8: Backward Compatibility")
st.write("Testing the old API still works")

try:
    from streamlit_expandable_columns import st_expandable_columns
    
    cols = st_expandable_columns([1, 1], key="backward_compat")
    cols[0].write("✅ Backward compatibility column 1")
    cols[1].write("✅ Backward compatibility column 2")
    
    st.success("✅ Backward compatibility maintained")
    
except Exception as e:
    st.error(f"❌ Test 8 failed: {e}")

st.divider()

# Summary
st.subheader("🎯 Test Summary")
st.write("""
**All tests completed!** The component should:

1. ✅ Support integer spec (number of equal columns)
2. ✅ Support list spec (custom width ratios)  
3. ✅ Support all st.columns parameters (gap, vertical_alignment, border)
4. ✅ Work with context managers (`with col:`)
5. ✅ Work with direct method calls (`col.write()`)
6. ✅ Handle complex nested content (tabs, expanders, charts)
7. ✅ Provide proper error handling
8. ✅ Maintain backward compatibility

**Usage Instructions:**
- Drag the boundaries between columns to resize them
- All standard Streamlit components work inside the columns
- The API is identical to `st.columns` but with resize capability
""")

st.info("💡 **Pro Tip**: Try dragging the column boundaries above to test the resize functionality!") 