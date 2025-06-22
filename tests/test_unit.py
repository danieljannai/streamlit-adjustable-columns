"""Unit tests for the streamlit_adjustable_columns component."""

from unittest.mock import MagicMock, patch

import pytest

from streamlit_adjustable_columns import HidableContainer, adjustable_columns


@pytest.mark.unit
def test_adjustable_columns_basic():
    """Test basic adjustable_columns functionality."""
    import streamlit as st

    # Mock the component function
    def mock_component(*args, **kwargs):
        return {"widths": [1, 1]}

    # Patch the component function
    import streamlit_adjustable_columns

    original_component = streamlit_adjustable_columns._component_func
    streamlit_adjustable_columns._component_func = mock_component

    try:
        # Test basic usage
        cols = adjustable_columns(2)
        assert len(cols) == 2
        assert all(isinstance(col, HidableContainer) for col in cols)

        # Test with return_widths
        result = adjustable_columns(2, return_widths=True)
        assert "columns" in result
        assert "widths" in result
        assert "hidden" in result
        assert len(result["columns"]) == 2
        assert len(result["widths"]) == 2
        assert len(result["hidden"]) == 2

    finally:
        # Restore original component function
        streamlit_adjustable_columns._component_func = original_component


@pytest.mark.unit
def test_adjustable_columns_config():
    """Test that the component receives the correct configuration."""
    import streamlit as st

    config_received = None

    def mock_component(config=None, **kwargs):
        nonlocal config_received
        config_received = config
        return {"widths": [1, 1, 1]}

    # Patch the component function
    import streamlit_adjustable_columns

    original_component = streamlit_adjustable_columns._component_func
    streamlit_adjustable_columns._component_func = mock_component

    try:
        adjustable_columns([1, 1, 1], labels=["A", "B", "C"])
        assert config_received is not None
        assert "widths" in config_received
        assert "labels" in config_received
        assert config_received["labels"] == ["A", "B", "C"]

    finally:
        # Restore original component function
        streamlit_adjustable_columns._component_func = original_component


@pytest.mark.unit
def test_adjustable_columns_hidden(monkeypatch):
    import streamlit as st

    from streamlit_adjustable_columns import (HidableContainer,
                                              adjustable_columns)

    # Patch session_state to simulate Streamlit
    state = {}
    monkeypatch.setattr(st, "session_state", state)

    # Simulate initial call
    result = adjustable_columns(
        [1, 1, 1], labels=["A", "B", "C"], return_widths=True, key="test_hidden"
    )
    assert "hidden" in result
    assert result["hidden"] == [False, False, False]
    assert all(isinstance(c, HidableContainer) for c in result["columns"])

    # Simulate hiding the second column
    state["adjustable_columns_hidden_test_hidden"] = [False, True, False]
    result2 = adjustable_columns(
        [1, 1, 1], labels=["A", "B", "C"], return_widths=True, key="test_hidden"
    )
    assert result2["hidden"] == [False, True, False]
    assert result2["columns"][1].is_hidden
    assert not result2["columns"][0].is_hidden
    assert not result2["columns"][2].is_hidden


@pytest.mark.unit
def test_adjustable_columns_initial_hidden(monkeypatch):
    """Test initial_hidden parameter functionality."""
    import streamlit as st

    from streamlit_adjustable_columns import (HidableContainer,
                                              adjustable_columns)

    # Patch session_state to simulate Streamlit
    state = {}
    monkeypatch.setattr(st, "session_state", state)

    # Test with initial_hidden parameter
    result = adjustable_columns(
        [1, 1, 1],
        labels=["A", "B", "C"],
        initial_hidden=[False, True, False],
        return_widths=True,
        key="test_initial_hidden",
    )

    assert result["hidden"] == [False, True, False]
    assert not result["columns"][0].is_hidden
    assert result["columns"][1].is_hidden
    assert not result["columns"][2].is_hidden

    # Test that session state was initialized correctly
    assert state["adjustable_columns_hidden_test_initial_hidden"] == [
        False,
        True,
        False,
    ]


@pytest.mark.unit
def test_adjustable_columns_initial_hidden_validation():
    """Test validation of initial_hidden parameter."""
    import streamlit as st

    # Test wrong length
    with pytest.raises(ValueError, match="initial_hidden must have the same length"):
        adjustable_columns([1, 1], initial_hidden=[True])

    # Test non-boolean values
    with pytest.raises(
        ValueError, match="initial_hidden must contain only boolean values"
    ):
        adjustable_columns([1, 1], initial_hidden=[True, "False"])


@pytest.mark.unit
def test_hidable_container_api():
    """Test that HidableContainer maintains the same API as the wrapped container."""
    import streamlit as st

    from streamlit_adjustable_columns import HidableContainer

    # Create a mock container with common Streamlit methods
    class MockContainer:
        def write(self, text):
            return f"write: {text}"

        def metric(self, label, value):
            return f"metric: {label} = {value}"

        def button(self, text):
            return f"button: {text}"

        def empty(self):
            return self

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    mock_container = MockContainer()
    hidable = HidableContainer(mock_container, is_hidden=False)

    # Test that methods work when visible
    assert hasattr(hidable, "write")
    assert hasattr(hidable, "metric")
    assert hasattr(hidable, "button")
    assert callable(hidable.write)
    assert callable(hidable.metric)
    assert callable(hidable.button)

    # Test that methods work when hidden (should not raise AttributeError)
    hidable.is_hidden = True
    assert hasattr(hidable, "write")
    assert hasattr(hidable, "metric")
    assert hasattr(hidable, "button")
    assert callable(hidable.write)
    assert callable(hidable.metric)
    assert callable(hidable.button)


@pytest.mark.unit
def test_adjustable_columns_basic_usage():
    """Test basic usage with integer spec."""
    with patch("streamlit_adjustable_columns.st.columns") as mock_columns:
        # Mock the columns return value
        mock_col1, mock_col2, mock_col3 = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]

        # Call the function
        result = adjustable_columns(3)

        # Check that it returns the columns (now wrapped in HidableContainer)
        assert len(result) == 3
        assert all(isinstance(col, HidableContainer) for col in result)
        # Check that the containers wrap the original mock columns
        assert result[0].container == mock_col1
        assert result[1].container == mock_col2
        assert result[2].container == mock_col3


@pytest.mark.unit
def test_adjustable_columns_with_ratios():
    """Test usage with custom width ratios."""
    with patch("streamlit_adjustable_columns.st.columns") as mock_columns:
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]

        result = adjustable_columns([3, 1])

        assert len(result) == 2
        assert all(isinstance(col, HidableContainer) for col in result)
        # Check that the containers wrap the original mock columns
        assert result[0].container == mock_col1
        assert result[1].container == mock_col2


@pytest.mark.unit
def test_adjustable_columns_return_widths():
    """Test return_widths functionality."""
    with patch("streamlit_adjustable_columns.st.columns") as mock_columns, patch(
        "streamlit_adjustable_columns.st.session_state", {}
    ):

        mock_col1, mock_col2, mock_col3 = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]

        result = adjustable_columns(3, return_widths=True, key="test")

        # Should return a dictionary with columns and widths
        assert isinstance(result, dict)
        assert "columns" in result
        assert "widths" in result
        assert len(result["columns"]) == 3
        assert len(result["widths"]) == 3


@pytest.mark.unit
def test_adjustable_columns_preserves_st_columns_params():
    """Test that st.columns parameters are preserved."""
    with patch("streamlit_adjustable_columns.st.columns") as mock_columns, patch(
        "streamlit_adjustable_columns._component_func"
    ) as mock_component, patch(
        "streamlit_adjustable_columns.st.session_state", {}
    ), patch(
        "streamlit_adjustable_columns.st.markdown"
    ):

        mock_columns.return_value = [MagicMock(), MagicMock()]
        mock_component.return_value = None

        adjustable_columns(
            [2, 1], gap="large", vertical_alignment="center", border=True
        )

        # Check that st.columns was called with the correct parameters
        mock_columns.assert_called_once()
        args, kwargs = mock_columns.call_args

        # Check that the spec was converted to widths (passed as keyword argument)
        assert "spec" in kwargs
        assert len(kwargs["spec"]) == 2  # Should have 2 width values

        # Check that other parameters were passed through
        assert kwargs.get("gap") == "large"
        assert kwargs.get("vertical_alignment") == "center"
        assert kwargs.get("border") is True


@pytest.mark.unit
def test_spec_validation():
    """Test that spec parameter validation works correctly."""
    with patch("streamlit_adjustable_columns.st.columns") as mock_columns:
        mock_columns.return_value = [MagicMock()]

        # Test with integer
        adjustable_columns(1)

        # Test with list
        adjustable_columns([1])

        # These should not raise exceptions
        assert True


@pytest.mark.unit
def test_session_state_key_generation():
    """Test that session state keys are generated correctly."""
    with patch("streamlit_adjustable_columns.st.columns") as mock_columns, patch(
        "streamlit_adjustable_columns.st.session_state", {}
    ):

        mock_columns.return_value = [MagicMock(), MagicMock()]

        # Test with explicit key
        adjustable_columns(2, key="test_key")

        # Test without key (should generate one)
        adjustable_columns(2)

        # Should not raise exceptions
        assert True


@pytest.mark.unit
def test_labels_parameter():
    """Test that labels parameter is handled correctly."""
    with patch("streamlit_adjustable_columns.st.columns") as mock_columns:
        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        labels = ["Label 1", "Label 2", "Label 3"]
        result = adjustable_columns(3, labels=labels, key="test")

        # Should return columns regardless of labels
        assert len(result) == 3


@pytest.mark.unit
def test_width_ratios_calculation():
    """Test that width ratios are calculated correctly."""
    with patch("streamlit_adjustable_columns.st.columns") as mock_columns, patch(
        "streamlit_adjustable_columns.st.session_state", {}
    ):

        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        # Test equal columns
        result = adjustable_columns(3, return_widths=True, key="test1")
        widths = result["widths"]

        # Should be approximately equal (allowing for floating point precision)
        assert abs(widths[0] - 1.0) < 0.1
        assert abs(widths[1] - 1.0) < 0.1
        assert abs(widths[2] - 1.0) < 0.1


@pytest.mark.unit
def test_component_integration():
    """Test that the component is called correctly."""
    with patch("streamlit_adjustable_columns._component_func") as mock_component:
        mock_component.return_value = {"widths": [1.0, 1.0, 1.0]}

        with patch("streamlit_adjustable_columns.st.columns") as mock_columns, patch(
            "streamlit_adjustable_columns.st.session_state", {}
        ), patch("streamlit_adjustable_columns.st.markdown"), patch(
            "streamlit_adjustable_columns.st.rerun"
        ):

            mock_columns.return_value = [
                MagicMock(),
                MagicMock(),
                MagicMock(),
            ]

            adjustable_columns(3, labels=["A", "B", "C"], key="test")

            # Component should be called with correct parameters
            mock_component.assert_called_once()
            args, kwargs = mock_component.call_args

            # Check that key components are present
            assert "config" in kwargs
            assert "key" in kwargs
            assert "default" in kwargs
            assert "height" in kwargs

            # Check that config contains expected values
            config = kwargs["config"]
            assert "widths" in config
            assert "labels" in config
            assert config["labels"] == ["A", "B", "C"]
