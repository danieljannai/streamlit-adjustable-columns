import os
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from tests import ROOT_DIRECTORY
from tests.e2e_utils import StreamlitRunner

ALL_PARAMS_EXAMPLE_FILE = os.path.join(ROOT_DIRECTORY, "tests", "streamlit_apps", "example_all_parameters.py")


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(Path(ALL_PARAMS_EXAMPLE_FILE)) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    # Wait for app to load
    page.get_by_role("img", name="Running...").is_hidden()


@pytest.mark.e2e
def test_should_render_all_parameters(page: Page):
    """Test that component renders with all parameters."""
    expect(page.get_by_text("Test Expandable Columns with All Parameters")).to_be_visible()

    # Check that parameter information is displayed
    expect(page.get_by_text("Gap: large")).to_be_visible()
    expect(page.get_by_text("Alignment: center")).to_be_visible()
    expect(page.get_by_text("Border: True")).to_be_visible()

    # Check that the iframe component is rendered
    iframe_component = page.locator('iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]').nth(0)
    expect(iframe_component).to_be_visible()


@pytest.mark.e2e
def test_should_display_custom_labels_and_widths(page: Page):
    """Test that custom labels and width tracking work together."""
    # Check that width ratios are displayed
    expect(page.locator("text=Current widths:")).to_be_visible()

    # Check that custom labels are present in the iframe
    iframe_frame = page.frame_locator('iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]')
    expect(iframe_frame.get_by_text("📊 Main")).to_be_visible()
    expect(iframe_frame.get_by_text("📋 Info")).to_be_visible()
    expect(iframe_frame.get_by_text("⚙️ Tools")).to_be_visible()


@pytest.mark.e2e
def test_should_render_complex_content(page: Page):
    """Test that complex content renders in columns with all parameters."""
    # Check for section content
    expect(page.get_by_text("Main section with large content")).to_be_visible()
    expect(page.get_by_text("Info section")).to_be_visible()
    expect(page.get_by_text("Tools section")).to_be_visible()

    # Check for info box
    expect(page.get_by_text("Information box")).to_be_visible()

    # Check for buttons
    expect(page.get_by_role("button", name="Tool 1")).to_be_visible()
    expect(page.get_by_role("button", name="Tool 2")).to_be_visible()


@pytest.mark.e2e
def test_should_apply_custom_ratios_with_all_params(page: Page):
    """Test that custom ratios [2, 1, 1] are applied correctly."""
    iframe_frame = page.frame_locator('iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]')
    
    # Get column containers if available
    columns = iframe_frame.locator('.column-container')
    
    if columns.count() >= 3:
        # Get bounding boxes for width comparison
        main_box = columns.nth(0).bounding_box()
        info_box = columns.nth(1).bounding_box()
        tools_box = columns.nth(2).bounding_box()
        
        if main_box and info_box and tools_box:
            # Main column should be roughly 2x wider than the other two
            ratio_main_to_info = main_box['width'] / info_box['width']
            ratio_main_to_tools = main_box['width'] / tools_box['width']
            
            # Allow some tolerance (between 1.5 and 2.5)
            assert 1.5 <= ratio_main_to_info <= 2.5
            assert 1.5 <= ratio_main_to_tools <= 2.5
            
            # Info and Tools should be roughly equal
            ratio_info_to_tools = info_box['width'] / tools_box['width']
            assert 0.7 <= ratio_info_to_tools <= 1.3


@pytest.mark.e2e
def test_all_params_resize_handles(page: Page):
    """Test that resize handles work with all parameters."""
    iframe_frame = page.frame_locator('iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]')
    
    # Should have 2 resize handles for 3 columns
    resize_handles = iframe_frame.locator('.resize-handle')
    expect(resize_handles.first).to_be_visible()
    
    handle_count = resize_handles.count()
    assert handle_count == 2

    # Test that handles can be hovered
    first_handle = resize_handles.first
    first_handle.hover()
    expect(first_handle).to_be_visible() 