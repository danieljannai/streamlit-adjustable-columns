import os
import streamlit as st
import streamlit.components.v1 as components
from typing import List, Union, Optional, Dict, Any
import uuid

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_expandable_columns",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "streamlit_expandable_columns", 
        path=build_dir
    )

def expandable_columns(spec=None, *, gap="small", vertical_alignment="top", border=False, labels=None, return_widths=False, key=None):
    """Create columns with adjustable widths using resizable boundaries.
    
    This function creates columns that work exactly like st.columns, but with 
    draggable resize handles above them to adjust their widths dynamically.
    Each column has a minimum width of 6% to ensure usability.
    
    Parameters
    ----------
    spec : int or Iterable of numbers, optional
        Controls the number and width of columns to insert. Can be one of:
        - An integer that specifies the number of columns. All columns have equal width.
        - An Iterable of numbers (int or float) that specify the relative width of each column.
        Default is 2 for two equal columns.
    gap : {"small", "medium", "large"}, default "small"
        The size of the gap between the columns.
    vertical_alignment : {"top", "center", "bottom"}, default "top"
        The vertical alignment of the content inside the columns.
    border : bool, default False
        Whether to show a border around the column containers.
    labels : list of str, optional
        Custom labels for each column shown in the resize handles.
        If None, defaults to "Col 1", "Col 2", etc.
    return_widths : bool, default False
        If True, returns a dict with 'columns' and 'widths' keys.
        If False, returns just the list of column containers (like st.columns).
    key : str, optional
        An optional key that uniquely identifies this component.
        
    Returns
    -------
    list of containers or dict
        If return_widths=False: A list of column container objects, just like st.columns.
        If return_widths=True: A dict with keys:
            - 'columns': List of column container objects
            - 'widths': Current width ratios of the columns
        
    Examples
    --------
    Basic usage (returns just columns):
    >>> col1, col2, col3 = expandable_columns(3, labels=["Main", "Side", "Tools"])
    >>> with col1:
    ...     st.write("Column 1")
    >>> col2.write("Column 2") 
    >>> col3.write("Column 3")
    
    With width information:
    >>> result = expandable_columns([3, 1], labels=["Content", "Sidebar"], return_widths=True)
    >>> col1, col2 = result['columns']
    >>> current_widths = result['widths']  # e.g., [2.5, 1.5] after resizing
    >>> st.write(f"Current ratios: {current_widths}")
    
    With all parameters:
    >>> result = expandable_columns(
    ...     spec=[2, 1, 1], 
    ...     gap="large", 
    ...     vertical_alignment="center",
    ...     border=True,
    ...     labels=["Charts", "Controls", "Info"],
    ...     return_widths=True
    ... )
    >>> cols = result['columns']
    >>> widths = result['widths']
    """
    
    # Handle spec parameter (same logic as st.columns)
    if spec is None:
        spec = 2  # Default to 2 equal columns
    
    if isinstance(spec, int):
        # Equal width columns
        widths = [1] * spec
    elif hasattr(spec, '__iter__'):
        # Custom width ratios
        widths = list(spec)
    else:
        raise ValueError("spec must be an integer or an iterable of numbers")
    
    # Validate widths
    if not widths:
        raise ValueError("spec must specify at least one column")
    
    if any(w <= 0 for w in widths):
        raise ValueError("Column widths must be positive numbers")
    
    # Set default labels
    if labels is None:
        labels = [f"Col {i+1}" for i in range(len(widths))]
    elif len(labels) != len(widths):
        raise ValueError("labels must have the same length as the number of columns")
    
    # Create unique identifier for this set of columns
    if key is None:
        unique_id = str(uuid.uuid4())[:8]
    else:
        unique_id = key
    
    # Create session state key for storing current widths
    session_key = f"expandable_columns_widths_{unique_id}"
    
    # Initialize or get current widths from session state
    if session_key not in st.session_state:
        st.session_state[session_key] = widths.copy()
    
    current_widths = st.session_state[session_key]
    
    # Ensure we have the right number of widths (in case spec changed)
    if len(current_widths) != len(widths):
        current_widths = widths.copy()
        st.session_state[session_key] = current_widths
    
    # Prepare configuration for the resizer component
    config = {
        'widths': current_widths,
        'labels': labels,
        'gap': gap,
        'border': border
    }
    
    # Create the resize handles component
    component_value = _component_func(
        config=config,
        key=f"resizer_{unique_id}",
        default={'widths': current_widths},
        height=60  # Compact height for just the resize handles
    )
    
    # Update current widths from component if it has been resized
    if component_value and 'widths' in component_value:
        new_widths = component_value['widths']
        # Only update session state if widths actually changed to avoid unnecessary reruns
        if new_widths != current_widths:
            st.session_state[session_key] = new_widths
            current_widths = new_widths
            # Force a rerun to update the column layout
            st.rerun()
    
    # Create the actual Streamlit columns with current widths
    # Ensure each column is at least 6% of total width
    MIN_WIDTH_RATIO = 0.06
    total_width = sum(current_widths)
    min_width_absolute = MIN_WIDTH_RATIO * total_width
    
    streamlit_widths = [max(width, min_width_absolute) for width in current_widths]
    
    # Create the actual st.columns with all supported parameters
    st_columns = st.columns(
        spec=streamlit_widths,
        gap=gap,
        vertical_alignment=vertical_alignment,
        border=border
    )
    
    # Return based on return_widths parameter
    if return_widths:
        return {
            'columns': st_columns,
            'widths': current_widths
        }
    else:
        return st_columns

# For backward compatibility - maintain the old function signature
def st_expandable_columns(*args, **kwargs):
    """Backward compatibility alias for expandable_columns."""
    return expandable_columns(*args, **kwargs) 