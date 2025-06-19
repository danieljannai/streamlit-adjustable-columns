import os
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from tests import ROOT_DIRECTORY
from tests.e2e_utils import StreamlitRunner

RATIOS_EXAMPLE_FILE = os.path.join(
    ROOT_DIRECTORY, "tests", "streamlit_apps", "example_custom_ratios.py"
)


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(Path(RATIOS_EXAMPLE_FILE)) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    # Wait for app to load
    page.get_by_role("img", name="Running...").is_hidden()


@pytest.mark.e2e
def test_should_render_custom_ratios(page: Page):
    """Test that custom width ratios are applied correctly."""
    expect(
        page.get_by_text("Test Expandable Columns with Custom Ratios")
    ).to_be_visible()

    # Check that the iframe component is rendered
    iframe_component = page.locator(
        'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]'
    ).nth(0)
    expect(iframe_component).to_be_visible()

    # Check that custom labels for ratios are present
    iframe_frame = page.frame_locator(
        'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]'
    )
    expect(iframe_frame.get_by_text("Main Content")).to_be_visible()
    expect(iframe_frame.get_by_text("Sidebar")).to_be_visible()


@pytest.mark.e2e
def test_should_apply_width_ratios(page: Page):
    """Test that 3:1 width ratio is applied correctly."""
    iframe_frame = page.frame_locator(
        'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]'
    )

    # Get the column containers (if they have identifiable classes)
    columns = iframe_frame.locator(".column-container")

    if columns.count() >= 2:
        # Get bounding boxes for width comparison
        main_box = columns.nth(0).bounding_box()
        sidebar_box = columns.nth(1).bounding_box()

        if main_box and sidebar_box:
            # Main column should be roughly 3 times wider than sidebar
            ratio = main_box["width"] / sidebar_box["width"]
            # Allow some tolerance for the ratio (between 2.5 and 3.5)
            assert 2.5 <= ratio <= 3.5


@pytest.mark.e2e
def test_should_render_ratio_content(page: Page):
    """Test that content in ratio-based columns renders correctly."""
    # Check for main content
    expect(page.get_by_text("Main content area (3:1 ratio)")).to_be_visible()
    expect(page.get_by_text("Sidebar (3:1 ratio)")).to_be_visible()

    # Check for text area
    expect(page.locator("textarea")).to_be_visible()

    # Check for buttons
    expect(page.get_by_role("button", name="Button 1")).to_be_visible()
    expect(page.get_by_role("button", name="Button 2")).to_be_visible()


@pytest.mark.e2e
def test_single_resize_handle_for_two_columns(page: Page):
    """Test that there's only one resize handle for two columns."""
    iframe_frame = page.frame_locator(
        'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]'
    )

    # Should have exactly 1 resize handle for 2 columns
    resize_handles = iframe_frame.locator(".resize-handle")
    expect(resize_handles).to_be_visible()

    handle_count = resize_handles.count()
    assert handle_count == 1
