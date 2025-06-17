import os
import streamlit as st
import streamlit.components.v1 as components

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

def expandable_columns(columns_config=None, key=None):
    """Create columns with adjustable widths.
    
    Parameters
    ----------
    columns_config : list or dict, optional
        Configuration for columns. Can be:
        - List of initial widths (e.g., [1, 2, 1] for 3 columns with ratios 1:2:1)
        - Dict with 'widths' key and optional 'min_widths' key
        - None for default 2 equal columns
    key : str, optional
        An optional key that uniquely identifies this component.
        
    Returns
    -------
    dict
        Dictionary containing:
        - 'widths': Current width ratios of columns
        - 'columns': List of column objects for content placement
    """
    
    # Default configuration
    if columns_config is None:
        columns_config = [1, 1]  # Two equal columns
    
    # Normalize configuration
    if isinstance(columns_config, list):
        config = {
            'widths': columns_config,
            'min_widths': [0.1] * len(columns_config)  # Minimum 10% width
        }
    elif isinstance(columns_config, dict):
        config = {
            'widths': columns_config.get('widths', [1, 1]),
            'min_widths': columns_config.get('min_widths', [0.1] * len(columns_config.get('widths', [1, 1])))
        }
    else:
        raise ValueError("columns_config must be a list of widths or a dict with 'widths' key")
    
    # Call the component function
    component_value = _component_func(
        config=config,
        key=key,
        default={'widths': config['widths']}
    )
    
    # Create actual Streamlit columns with current widths
    if component_value and 'widths' in component_value:
        current_widths = component_value['widths']
    else:
        current_widths = config['widths']
    
    # Create Streamlit columns - handle collapsed columns (width ≈ 0)
    # Streamlit doesn't accept 0 or negative widths, so we use a tiny positive value
    MIN_COLUMN_WIDTH = 0.001
    streamlit_widths = [max(w, MIN_COLUMN_WIDTH) for w in current_widths]
    st_columns = st.columns(streamlit_widths)
    
    return {
        'widths': current_widths,
        'columns': st_columns,
        'component_value': component_value
    }

# For backward compatibility
def st_expandable_columns(*args, **kwargs):
    """Backward compatibility alias for expandable_columns."""
    return expandable_columns(*args, **kwargs) 