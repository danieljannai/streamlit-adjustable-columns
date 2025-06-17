#!/usr/bin/env python3
"""
Simple test script for the expandable columns component.
Run this to verify basic functionality.
"""

import streamlit as st
from streamlit_expandable_columns import expandable_columns

def test_basic_functionality():
    """Test basic component functionality."""
    st.title("🧪 Expandable Columns Test")
    
    st.markdown("---")
    
    # Test 1: Basic two-column layout
    st.header("Test 1: Basic Two Columns")
    result1 = expandable_columns([1, 1], key="test1")
    
    if result1:
        st.success("✅ Basic two-column layout created successfully")
        st.write(f"Column widths: {result1['widths']}")
        
        col1, col2 = result1['columns']
        with col1:
            st.write("Column 1 content")
        with col2:
            st.write("Column 2 content")
    else:
        st.error("❌ Failed to create basic two-column layout")
    
    st.markdown("---")
    
    # Test 2: Three-column layout
    st.header("Test 2: Three Columns")
    result2 = expandable_columns([1, 2, 1], key="test2")
    
    if result2:
        st.success("✅ Three-column layout created successfully")
        st.write(f"Column widths: {result2['widths']}")
        
        col1, col2, col3 = result2['columns']
        with col1:
            st.write("Column 1")
        with col2:
            st.write("Column 2 (wider)")
        with col3:
            st.write("Column 3")
    else:
        st.error("❌ Failed to create three-column layout")
    
    st.markdown("---")
    
    # Test 3: Advanced configuration
    st.header("Test 3: Advanced Configuration")
    config = {
        'widths': [2, 3, 1],
        'min_widths': [0.2, 0.2, 0.2]
    }
    result3 = expandable_columns(config, key="test3")
    
    if result3:
        st.success("✅ Advanced configuration created successfully")
        st.write(f"Column widths: {result3['widths']}")
        
        col1, col2, col3 = result3['columns']
        with col1:
            st.write("Column 1 (min 20%)")
        with col2:
            st.write("Column 2 (min 20%)")
        with col3:
            st.write("Column 3 (min 20%)")
    else:
        st.error("❌ Failed to create advanced configuration")
    
    st.markdown("---")
    
    # Test 4: Error handling
    st.header("Test 4: Error Handling")
    try:
        # This should raise an error
        result4 = expandable_columns("invalid config", key="test4")
        st.error("❌ Error handling failed - should have raised ValueError")
    except ValueError as e:
        st.success("✅ Error handling works correctly")
        st.write(f"Caught expected error: {e}")
    except Exception as e:
        st.warning(f"⚠️ Unexpected error type: {e}")
    
    st.markdown("---")
    
    # Summary
    st.header("Test Summary")
    st.info("All tests completed. Check the results above.")
    
    st.markdown("### How to Test Interactivity:")
    st.markdown("""
    1. **Drag the column separators** to resize columns
    2. **Refresh the page** - column widths should persist
    3. **Interact with other elements** - columns should maintain their proportions
    4. **Try on different screen sizes** - should be responsive
    """)

if __name__ == "__main__":
    test_basic_functionality() 