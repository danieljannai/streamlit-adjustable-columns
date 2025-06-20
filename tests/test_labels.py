import os
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from tests import ROOT_DIRECTORY
from tests.e2e_utils import StreamlitRunner

LABELS_EXAMPLE_FILE = os.path.join(
    ROOT_DIRECTORY, "tests", "streamlit_apps", "example_with_labels.py"
)


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(Path(LABELS_EXAMPLE_FILE)) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    # Wait for app to load
    page.get_by_role("img", name="Running...").is_hidden()


@pytest.mark.e2e
def test_should_render_custom_labels(page: Page):
    """Test that custom labels are displayed correctly."""
    expect(page.get_by_text("Test Adjustable Columns with Labels")).to_be_visible()

    # Check that the iframe component is rendered
    iframe_component = page.locator(
        'iframe[title="streamlit_adjustable_columns.streamlit_adjustable_columns"]'
    ).nth(0)
    expect(iframe_component).to_be_visible()

    # Check that custom labels are present in the iframe
    iframe_frame = page.frame_locator(
        'iframe[title="streamlit_adjustable_columns.streamlit_adjustable_columns"]'
    )

    # Check for custom labels with emojis
    expect(iframe_frame.get_by_text("📊 Charts")).to_be_visible()
    expect(iframe_frame.get_by_text("📋 Data")).to_be_visible()
    expect(iframe_frame.get_by_text("⚙️ Settings")).to_be_visible()


@pytest.mark.e2e
def test_should_render_labeled_column_content(page: Page):
    """Test that content in labeled columns renders correctly."""
    # Check for section content
    expect(page.get_by_text("Charts section")).to_be_visible()
    expect(page.get_by_text("Data section")).to_be_visible()
    expect(page.get_by_text("Settings section")).to_be_visible()

    # Check that selectbox is present
    expect(page.locator("select")).to_be_visible()


@pytest.mark.e2e
def test_labels_with_resize_handles(page: Page):
    """Test that labels work properly with resize handles."""
    iframe_frame = page.frame_locator(
        'iframe[title="streamlit_adjustable_columns.streamlit_adjustable_columns"]'
    )

    # Check that labels are positioned above resize handles
    labels = iframe_frame.locator(".column-label")
    expect(labels.first).to_be_visible()

    # Should have 3 labels for 3 columns
    label_count = labels.count()
    assert label_count == 3

    # Check that resize handles still work with labels
    resize_handles = iframe_frame.locator(".resize-handle")
    expect(resize_handles.first).to_be_visible()

    # Should have 2 handles for 3 columns
    handle_count = resize_handles.count()
    assert handle_count == 2
