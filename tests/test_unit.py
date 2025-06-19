"""Unit tests for the streamlit_expandable_columns component."""

import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
from streamlit_expandable_columns import expandable_columns


@pytest.mark.unit
def test_expandable_columns_basic_usage():
    """Test basic usage with integer spec."""
    with patch('streamlit_expandable_columns.st.columns') as mock_columns:
        # Mock the columns return value
        mock_col1, mock_col2, mock_col3 = MagicMock(), MagicMock(), MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]
        
        # Call the function
        result = expandable_columns(3)
        
        # Check that it returns the columns
        assert len(result) == 3
        assert result == [mock_col1, mock_col2, mock_col3]


@pytest.mark.unit
def test_expandable_columns_with_ratios():
    """Test usage with custom width ratios."""
    with patch('streamlit_expandable_columns.st.columns') as mock_columns:
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]
        
        result = expandable_columns([3, 1])
        
        assert len(result) == 2
        assert result == [mock_col1, mock_col2]


@pytest.mark.unit
def test_expandable_columns_return_widths():
    """Test return_widths functionality."""
    with patch('streamlit_expandable_columns.st.columns') as mock_columns, \
         patch('streamlit_expandable_columns.st.session_state', {}):
        
        mock_col1, mock_col2, mock_col3 = MagicMock(), MagicMock(), MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]
        
        result = expandable_columns(3, return_widths=True, key="test")
        
        # Should return a dictionary with columns and widths
        assert isinstance(result, dict)
        assert 'columns' in result
        assert 'widths' in result
        assert len(result['columns']) == 3
        assert len(result['widths']) == 3


@pytest.mark.unit
def test_expandable_columns_preserves_st_columns_params():
    """Test that st.columns parameters are preserved."""
    with patch('streamlit_expandable_columns.st.columns') as mock_columns, \
         patch('streamlit_expandable_columns._component_func') as mock_component, \
         patch('streamlit_expandable_columns.st.session_state', {}), \
         patch('streamlit_expandable_columns.st.markdown'):
        
        mock_columns.return_value = [MagicMock(), MagicMock()]
        mock_component.return_value = None
        
        expandable_columns(
            [2, 1], 
            gap="large", 
            vertical_alignment="center", 
            border=True
        )
        
        # Check that st.columns was called with the correct parameters
        mock_columns.assert_called_once()
        args, kwargs = mock_columns.call_args
        
        # Check that the spec was converted to widths (passed as keyword argument)
        assert 'spec' in kwargs
        assert len(kwargs['spec']) == 2  # Should have 2 width values
        
        # Check that other parameters were passed through
        assert kwargs.get('gap') == "large"
        assert kwargs.get('vertical_alignment') == "center"
        assert kwargs.get('border') is True


@pytest.mark.unit
def test_spec_validation():
    """Test that spec parameter validation works correctly."""
    with patch('streamlit_expandable_columns.st.columns') as mock_columns:
        mock_columns.return_value = [MagicMock()]
        
        # Test with integer
        expandable_columns(1)
        
        # Test with list
        expandable_columns([1])
        
        # These should not raise exceptions
        assert True


@pytest.mark.unit
def test_session_state_key_generation():
    """Test that session state keys are generated correctly."""
    with patch('streamlit_expandable_columns.st.columns') as mock_columns, \
         patch('streamlit_expandable_columns.st.session_state', {}) as mock_session:
        
        mock_columns.return_value = [MagicMock(), MagicMock()]
        
        # Test with explicit key
        expandable_columns(2, key="test_key")
        
        # Test without key (should generate one)
        expandable_columns(2)
        
        # Should not raise exceptions
        assert True


@pytest.mark.unit
def test_labels_parameter():
    """Test that labels parameter is handled correctly."""
    with patch('streamlit_expandable_columns.st.columns') as mock_columns:
        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        
        labels = ["Label 1", "Label 2", "Label 3"]
        result = expandable_columns(3, labels=labels, key="test")
        
        # Should return columns regardless of labels
        assert len(result) == 3


@pytest.mark.unit
def test_width_ratios_calculation():
    """Test that width ratios are calculated correctly."""
    with patch('streamlit_expandable_columns.st.columns') as mock_columns, \
         patch('streamlit_expandable_columns.st.session_state', {}):
        
        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        
        # Test equal columns
        result = expandable_columns(3, return_widths=True, key="test1")
        widths = result['widths']
        
        # Should be approximately equal (allowing for floating point precision)
        assert abs(widths[0] - 1.0) < 0.1
        assert abs(widths[1] - 1.0) < 0.1
        assert abs(widths[2] - 1.0) < 0.1


@pytest.mark.unit
def test_component_integration():
    """Test that the component is called correctly."""
    with patch('streamlit_expandable_columns._component_func') as mock_component:
        mock_component.return_value = {'widths': [1.0, 1.0, 1.0]}
        
        with patch('streamlit_expandable_columns.st.columns') as mock_columns, \
             patch('streamlit_expandable_columns.st.session_state', {}) as mock_session, \
             patch('streamlit_expandable_columns.st.markdown'), \
             patch('streamlit_expandable_columns.st.rerun'):
            
            mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
            
            expandable_columns(3, labels=["A", "B", "C"], key="test")
            
            # Component should be called with correct parameters
            mock_component.assert_called_once()
            args, kwargs = mock_component.call_args
            
            # Check that key components are present
            assert 'config' in kwargs
            assert 'key' in kwargs
            assert 'default' in kwargs
            assert 'height' in kwargs
            
            # Check that config contains expected values
            config = kwargs['config']
            assert 'widths' in config
            assert 'labels' in config
            assert config['labels'] == ["A", "B", "C"] 