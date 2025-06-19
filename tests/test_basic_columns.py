import os
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from tests import ROOT_DIRECTORY
from tests.e2e_utils import StreamlitRunner

BASIC_EXAMPLE_FILE = os.path.join(
    ROOT_DIRECTORY, "tests", "streamlit_apps", "example_basic_columns.py"
)


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(Path(BASIC_EXAMPLE_FILE)) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    # Wait for app to load
    page.get_by_role("img", name="Running...").is_hidden()


@pytest.mark.e2e
def test_should_render_basic_columns(page: Page):
    """Test that basic expandable columns render correctly."""
    expect(page.get_by_text("Test Basic Expandable Columns")).to_be_visible()

    # Check that the iframe component is rendered
    iframe_component = page.locator(
        'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]'
    ).nth(0)
    expect(iframe_component).to_be_visible()

    # Check iframe dimensions
    iframe_box = iframe_component.bounding_box()
    assert iframe_box["width"] > 0
    assert iframe_box["height"] > 0

    # Check that resize handles are present in the iframe
    iframe_frame = page.frame_locator(
        'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]'
    )
    resize_handles = iframe_frame.locator(".resize-handle")
    expect(resize_handles.first).to_be_visible()

    # Check that multiple handles exist (should be 2 for 3 columns)
    handle_count = resize_handles.count()
    assert handle_count == 2


@pytest.mark.e2e
def test_should_render_column_content(page: Page):
    """Test that column content renders correctly."""
    # Check for metric values in each column
    expect(page.get_by_text("Column 1 Content")).to_be_visible()
    expect(page.get_by_text("Column 2 Content")).to_be_visible()
    expect(page.get_by_text("Column 3 Content")).to_be_visible()

    # Check for metrics
    expect(page.get_by_text("Metric 1")).to_be_visible()
    expect(page.get_by_text("Metric 2")).to_be_visible()
    expect(page.get_by_text("Metric 3")).to_be_visible()

    # Check metric values
    expect(page.get_by_text("100")).to_be_visible()
    expect(page.get_by_text("200")).to_be_visible()
    expect(page.get_by_text("300")).to_be_visible()


@pytest.mark.e2e
def test_resize_handle_interaction(page: Page):
    """Test that resize handles can be interacted with."""
    iframe_component = page.locator(
        'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]'
    ).nth(0)
    expect(iframe_component).to_be_visible()

    iframe_frame = page.frame_locator(
        'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]'
    )

    # Get the first resize handle
    first_handle = iframe_frame.locator(".resize-handle").first
    expect(first_handle).to_be_visible()

    # Check that handle has proper cursor styling
    handle_cursor = first_handle.evaluate("element => getComputedStyle(element).cursor")
    assert handle_cursor in ["col-resize", "ew-resize"]

    # Test hover state
    first_handle.hover()

    # The handle should still be visible after hover
    expect(first_handle).to_be_visible()
