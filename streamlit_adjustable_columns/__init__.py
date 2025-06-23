# flake8: noqa: E501 C901

import hashlib
import inspect
import os

import streamlit as st
import streamlit.components.v1 as components

__version__ = "0.2.1"

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_adjustable_columns",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")

    # Check if build directory and required files exist
    index_html = os.path.join(build_dir, "index.html")
    main_js = os.path.join(build_dir, "main.js")

    # Check if build directory exists
    if not os.path.exists(index_html) or not os.path.exists(main_js):
        raise RuntimeError(
            f"Compiled frontend assets not found in: {build_dir}\n"
            "This usually means the frontend wasn't built during installation.\n"
            "If installing from a source checkout, ensure Node.js and npm are installed, then run:\n"
            "pip install .\n"
            "Alternatively install from PyPI where prebuilt assets are included."
        )

    _component_func = components.declare_component(
        "streamlit_adjustable_columns", path=build_dir
    )


class HidableContainer:
    """A container that can be hidden/shown and acts like the wrapped container when visible."""

    def __init__(
        self, container: st.delta_generator.DeltaGenerator, is_hidden: bool = False
    ):
        self.container = container
        self.is_hidden = is_hidden
        self.empty_container = container.empty()

    def __enter__(self):
        if self.is_hidden:
            return self.empty_container.__enter__()
        else:
            return self.container.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_hidden:
            self.empty_container.empty()
            return self.empty_container.__exit__(exc_type, exc_val, exc_tb)
        else:
            return self.container.__exit__(exc_type, exc_val, exc_tb)

    def __getattr__(self, name):
        # Get the attribute from the actual container (not empty)
        # This ensures we have access to all methods like metric(), write(), etc.
        attr = getattr(self.container, name)

        if callable(attr):
            # If it's a callable method, wrap it to handle hidden state
            def wrapped_method(*args, **kwargs):
                if self.is_hidden:
                    # When hidden, call the method on the original container
                    # This ensures the method exists and works as expected
                    # attr(*args, **kwargs)
                    return self.empty_container.empty()  # Clear it immediately
                else:
                    # When visible, call the method normally
                    return attr(*args, **kwargs)

            return wrapped_method
        else:
            # For non-callable attributes, return them directly
            return attr


def adjustable_columns(
    spec=None,
    *,
    gap="small",
    vertical_alignment="top",
    border=False,
    labels=None,
    return_widths=False,
    initial_hidden=None,
    key=None,
):
    """Create columns with adjustable widths using resizable boundaries.

    This function creates columns that work exactly like st.columns, but with
    draggable resize handles above them to adjust their widths dynamically.
    Each column has a minimum width of 6% to ensure usability.

    Double-click on a column header to hide/show that column.

    Parameters
    ----------
    spec : int or Iterable of numbers.
        Controls the number and width of columns to insert. Can be one of:
        - An integer that specifies the number of columns. All columns have equal width.
        - An Iterable of numbers (int or float) that specify the relative width of each column.
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
    initial_hidden : list of bool, optional
        List of boolean values indicating which columns should start hidden.
        Must have the same length as the number of columns.
        If None, all columns start visible.
    key : str, optional
        An optional key that uniquely identifies this component.

    Returns
    -------
    list of containers or dict
        If return_widths=False: A list of column container objects, just like st.columns.
        If return_widths=True: A dict with keys:
            - 'columns': List of column container objects
            - 'widths': Current width ratios of the columns
            - 'hidden': List of boolean values indicating which columns are hidden

    Examples
    --------
    Basic usage (returns just columns):
    >>> col1, col2, col3 = adjustable_columns(3, labels=["Main", "Side", "Tools"])
    >>> with col1:
    ...     st.write("Column 1")
    >>> col2.write("Column 2")
    >>> col3.write("Column 3")

    With width information:
    >>> result = adjustable_columns([3, 1], labels=["Content", "Sidebar"], return_widths=True)
    >>> col1, col2 = result['columns']
    >>> current_widths = result['widths']  # e.g., [2.5, 1.5] after resizing
    >>> hidden_columns = result['hidden']  # e.g., [False, True] if second column is hidden
    >>> st.write(f"Current ratios: {current_widths}")

    With initial hidden columns:
    >>> result = adjustable_columns(
    ...     spec=[2, 1, 1],
    ...     labels=["Charts", "Controls", "Info"],
    ...     initial_hidden=[False, True, False],  # Second column starts hidden
    ...     return_widths=True
    ... )
    >>> cols = result['columns']
    >>> widths = result['widths']
    >>> hidden = result['hidden']
    """

    # Handle spec parameter (same logic as st.columns)
    if spec is None:
        spec = 2  # Default to 2 equal columns

    if isinstance(spec, int):
        # Equal width columns
        widths = [1] * spec
    elif hasattr(spec, "__iter__"):
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

    # Validate initial_hidden parameter
    if initial_hidden is not None:
        if len(initial_hidden) != len(widths):
            raise ValueError(
                "initial_hidden must have the same length as the number of columns"
            )
        if not all(isinstance(x, bool) for x in initial_hidden):
            raise ValueError("initial_hidden must contain only boolean values")
    else:
        initial_hidden = [False] * len(widths)

    # Create unique identifier for this set of columns
    if key is None:
        caller = inspect.currentframe().f_back
        try:
            src = f"{caller.f_code.co_filename}:{caller.f_lineno}"
        finally:
            del caller
        unique_id = hashlib.md5(src.encode()).hexdigest()[:8]
    else:
        unique_id = key

    # Create session state keys for storing current widths and hidden state
    session_key = f"adjustable_columns_widths_{unique_id}"
    hidden_key = f"adjustable_columns_hidden_{unique_id}"

    # Initialize or get current widths from session state
    if session_key not in st.session_state:
        st.session_state[session_key] = widths.copy()

    current_widths = st.session_state[session_key]

    # Initialize or get hidden state from session state
    if hidden_key not in st.session_state:
        st.session_state[hidden_key] = initial_hidden.copy()

    hidden_columns = st.session_state[hidden_key]

    # Ensure we have the right number of widths and hidden states (in case spec changed)
    if len(current_widths) != len(widths):
        current_widths = widths.copy()
        st.session_state[session_key] = current_widths

    if len(hidden_columns) != len(widths):
        hidden_columns = initial_hidden.copy()
        st.session_state[hidden_key] = hidden_columns

    # Prepare configuration for the resizer component
    config = {
        "widths": current_widths,
        "labels": labels,
        "gap": gap,
        "border": border,
        "hidden": hidden_columns,
    }

    # Create the resize handles component
    component_value = _component_func(
        config=config,
        key=f"resizer_{unique_id}",
        default={"widths": current_widths, "hidden": hidden_columns},
        height=60,  # Compact height for just the resize handles
    )

    # Update current widths and hidden state from component if it has been modified
    if component_value:
        needs_update = False

        if "widths" in component_value:
            new_widths = component_value["widths"]
            if new_widths != current_widths:
                st.session_state[session_key] = new_widths
                current_widths = new_widths
                needs_update = True

        if "hidden" in component_value:
            new_hidden = component_value["hidden"]
            if new_hidden != hidden_columns:
                st.session_state[hidden_key] = new_hidden
                hidden_columns = new_hidden
                needs_update = True

        if needs_update:
            # Force a rerun to update the column layout
            st.rerun()

    # Add CSS to ensure perfect alignment between resize handles and columns
    alignment_css = """
    <style>
    /* Ensure the resize handles iframe has no extra spacing */
    iframe[title="streamlit_adjustable_columns.streamlit_adjustable_columns"] {
        border: none !important;
        background: transparent !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Remove any extra margins from the element container holding the iframe */
    .element-container:has(iframe[title="streamlit_adjustable_columns.streamlit_adjustable_columns"]) {
        margin-bottom: 0 !important;
    }

    /* Ensure the following columns have proper spacing */
    .element-container:has(iframe[title="streamlit_adjustable_columns.streamlit_adjustable_columns"]) + div[data-testid="column"] {
        margin-top: 0 !important;
    }

    .element-container:has(iframe[title="streamlit_adjustable_columns.streamlit_adjustable_columns"]) + div[data-testid="column"] ~ div[data-testid="column"] {
        margin-top: 0 !important;
    }
    </style>
    """

    st.markdown(alignment_css, unsafe_allow_html=True)

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
        border=border,
    )

    # Wrap columns with HidableContainer based on hidden state
    wrapped_columns = [
        HidableContainer(col, is_hidden=hidden)
        for col, hidden in zip(st_columns, hidden_columns)
    ]

    # Return based on return_widths parameter
    if return_widths:
        return {
            "columns": wrapped_columns,
            "widths": current_widths,
            "hidden": hidden_columns,
        }
    else:
        return wrapped_columns
