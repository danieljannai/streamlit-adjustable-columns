"""Integration tests for streamlit-expandable-columns component."""

from unittest.mock import MagicMock, patch

import pytest
import streamlit as st

from streamlit_expandable_columns import expandable_columns


@pytest.mark.unit
class TestExpandableColumnsIntegration:
    """Integration tests for the expandable columns component."""

    def test_component_import(self):
        """Test that the component can be imported successfully."""
        from streamlit_expandable_columns import expandable_columns

        assert callable(expandable_columns)

    def test_component_with_session_state(self):
        """Test component behavior with session state."""
        with patch("streamlit_expandable_columns.st.session_state", {}) as mock_session:
            with patch("streamlit_expandable_columns.st.columns") as mock_columns:
                mock_columns.return_value = [MagicMock(), MagicMock()]

                # First call should initialize session state
                result1 = expandable_columns(2, key="integration_test")
                assert len(result1) == 2

                # Second call should use existing session state
                result2 = expandable_columns(2, key="integration_test")
                assert len(result2) == 2

    def test_component_state_persistence(self):
        """Test that component state persists across calls."""
        session_state = {}

        with patch("streamlit_expandable_columns.st.session_state", session_state):
            with patch(
                "streamlit_expandable_columns._component_func"
            ) as mock_component:
                # Mock component returning custom widths
                mock_component.return_value = {"widths": [1.5, 0.5]}

                with patch(
                    "streamlit_expandable_columns.st.columns"
                ) as mock_columns, patch(
                    "streamlit_expandable_columns.st.markdown"
                ), patch(
                    "streamlit_expandable_columns.st.rerun"
                ):

                    mock_columns.return_value = [MagicMock(), MagicMock()]

                    # First call
                    result1 = expandable_columns(
                        2, return_widths=True, key="persist_test"
                    )

                    # State should be updated (note the correct session key format)
                    assert "expandable_columns_widths_persist_test" in session_state

                    # Second call should use persisted state
                    result2 = expandable_columns(
                        2, return_widths=True, key="persist_test"
                    )

                    # Both calls should return the same structure
                    assert "columns" in result1 and "columns" in result2
                    assert "widths" in result1 and "widths" in result2

    def test_different_spec_formats(self):
        """Test different ways to specify columns."""
        with patch("streamlit_expandable_columns.st.columns") as mock_columns:
            mock_columns.return_value = [MagicMock()]

            # Integer spec
            result1 = expandable_columns(1)
            assert len(result1) == 1

            # List spec with single element
            result2 = expandable_columns([1])
            assert len(result2) == 1

            # List spec with multiple elements
            mock_columns.return_value = [
                MagicMock(),
                MagicMock(),
                MagicMock(),
            ]
            result3 = expandable_columns([2, 1, 1])
            assert len(result3) == 3

    def test_labels_integration(self):
        """Test labels integration with the component."""
        with patch("streamlit_expandable_columns._component_func") as mock_component:
            mock_component.return_value = {"widths": [1.0, 1.0]}

            with patch(
                "streamlit_expandable_columns.st.columns"
            ) as mock_columns, patch(
                "streamlit_expandable_columns.st.session_state", {}
            ), patch(
                "streamlit_expandable_columns.st.markdown"
            ):

                mock_columns.return_value = [MagicMock(), MagicMock()]

                labels = ["📊 Dashboard", "⚙️ Settings"]
                result = expandable_columns(2, labels=labels, key="labels_integration")

                # Component should receive the labels
                mock_component.assert_called_once()
                call_kwargs = mock_component.call_args[1]
                # Labels are inside the config parameter
                assert call_kwargs["config"]["labels"] == labels

    def test_parameter_forwarding(self):
        """Test that all st.columns parameters are forwarded correctly."""
        with patch("streamlit_expandable_columns.st.columns") as mock_columns:
            mock_columns.return_value = [MagicMock(), MagicMock()]

            expandable_columns(
                2,
                gap="large",
                vertical_alignment="center",
                border=True,
                key="param_test",
            )

            # Check that st.columns was called with forwarded parameters
            call_args, call_kwargs = mock_columns.call_args
            assert call_kwargs["gap"] == "large"
            assert call_kwargs["vertical_alignment"] == "center"
            assert call_kwargs["border"] is True

    @patch("streamlit_expandable_columns.st.columns")
    @patch("streamlit_expandable_columns._component_func")
    def test_width_calculation_and_application(self, mock_component, mock_columns):
        """Test that widths are calculated and applied correctly."""
        # Mock component returns custom widths
        custom_widths = [2.0, 1.0, 1.0]
        mock_component.return_value = {"widths": custom_widths}

        with patch("streamlit_expandable_columns.st.session_state", {}), patch(
            "streamlit_expandable_columns.st.markdown"
        ), patch("streamlit_expandable_columns.st.rerun"):

            mock_columns.return_value = [
                MagicMock(),
                MagicMock(),
                MagicMock(),
            ]

            result = expandable_columns(3, return_widths=True, key="width_calc_test")

            # Check that the returned widths match the component output
            assert result["widths"] == custom_widths

            # Check that st.columns was called with the custom widths
            call_kwargs = mock_columns.call_args[1]
            assert len(call_kwargs["spec"]) == 3  # Should have 3 width values

    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        with patch("streamlit_expandable_columns.st.columns") as mock_columns:
            mock_columns.return_value = [MagicMock()]

            # These should not raise exceptions
            try:
                expandable_columns(1)
                expandable_columns([1])
                expandable_columns(1, labels=["Test"])
                expandable_columns(1, return_widths=True, key="error_test")
            except Exception as e:
                pytest.fail(f"expandable_columns raised an unexpected exception: {e}")

    def test_key_uniqueness(self):
        """Test that different keys create separate state."""
        session_state = {}

        with patch("streamlit_expandable_columns.st.session_state", session_state):
            with patch(
                "streamlit_expandable_columns._component_func"
            ) as mock_component:
                mock_component.return_value = [1.0, 1.0]

                with patch("streamlit_expandable_columns.st.columns") as mock_columns:
                    mock_columns.return_value = [MagicMock(), MagicMock()]

                    # Create two instances with different keys
                    expandable_columns(2, key="key1")
                    expandable_columns(2, key="key2")

                    # Should create separate session state entries
                    keys = [
                        key
                        for key in session_state.keys()
                        if key.startswith("expandable_columns_")
                    ]
                    assert len(keys) >= 2
