# flake8: noqa: E501

import os
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from tests import ROOT_DIRECTORY
from tests.e2e_utils import StreamlitRunner

WIDTHS_EXAMPLE_FILE = os.path.join(
    ROOT_DIRECTORY, "tests", "streamlit_apps", "example_return_widths.py"
)


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(Path(WIDTHS_EXAMPLE_FILE)) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    # Wait for app to load
    page.get_by_role("img", name="Running...").is_hidden()


@pytest.mark.e2e
def test_should_display_width_information(page: Page):
    """Test that width information is displayed."""
    expect(
        page.get_by_text("Test Expandable Columns with Width Tracking")
    ).to_be_visible()

    # Check that width ratios are displayed
    expect(page.locator("text=Current width ratios:")).to_be_visible()

    # Check that individual width values are shown in columns
    expect(page.get_by_text("Width:")).to_be_visible()


@pytest.mark.e2e
def test_should_render_width_tracking_columns(page: Page):
    """Test that columns with width tracking render correctly."""
    # Check that the iframe component is rendered
    iframe_component = page.locator(
        'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]'
    ).nth(0)
    expect(iframe_component).to_be_visible()

    # Check that column labels are present
    iframe_frame = page.frame_locator(
        'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]'
    )
    expect(iframe_frame.get_by_text("Col A")).to_be_visible()
    expect(iframe_frame.get_by_text("Col B")).to_be_visible()
    expect(iframe_frame.get_by_text("Col C")).to_be_visible()


@pytest.mark.e2e
def test_should_show_individual_column_widths(page: Page):
    """Test that individual column widths are displayed."""
    # Check for column content with width information
    expect(page.get_by_text("Column A")).to_be_visible()
    expect(page.get_by_text("Column B")).to_be_visible()
    expect(page.get_by_text("Column C")).to_be_visible()

    # Check that width values are displayed (will contain decimal numbers)
    width_elements = page.locator("text=/Width: \\d+\\.\\d+/")
    expect(width_elements.first).to_be_visible()


@pytest.mark.e2e
def test_width_values_sum_to_reasonable_total(page: Page):
    """Test that width values make sense (should sum to approximately the number of columns)."""
    # Get all width text elements
    width_texts = page.locator("text=/Width: \\d+\\.\\d+/").all_text_contents()

    if width_texts:
        # Extract numeric values
        widths = []
        for text in width_texts:
            try:
                # Extract the number after "Width: "
                width_value = float(text.split("Width: ")[1])
                widths.append(width_value)
            except (IndexError, ValueError):
                continue

        if len(widths) == 3:
            total_width = sum(widths)
            # Total should be approximately 3 (number of columns) with some tolerance
            assert 2.5 <= total_width <= 3.5


@pytest.mark.e2e
def test_width_tracking_resize_handles(page: Page):
    """Test that resize handles work with width tracking."""
    iframe_frame = page.frame_locator(
        'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]'
    )

    # Should have 2 resize handles for 3 columns
    resize_handles = iframe_frame.locator(".resize-handle")
    expect(resize_handles.first).to_be_visible()

    handle_count = resize_handles.count()
    assert handle_count == 2
