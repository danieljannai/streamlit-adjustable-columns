# flake8: noqa: E501

import os
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from tests import ROOT_DIRECTORY
from tests.e2e_utils import StreamlitRunner

E2E_TEST_APP = os.path.join(
    ROOT_DIRECTORY, "tests", "streamlit_apps", "example_basic_columns.py"
)


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    """Fixture to run the Streamlit app for the test module."""
    with StreamlitRunner(Path(E2E_TEST_APP)) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    """Fixture to navigate to the Streamlit app for each test."""
    page.goto(streamlit_app.server_url)
    # Wait for the app to be fully loaded
    page.get_by_role("img", name="Running...").is_hidden(timeout=60000)
    # Wait for the component iframe to be attached to the DOM
    page.wait_for_selector(
        'iframe[title="streamlit_adjustable_columns.streamlit_adjustable_columns"]',
        state="attached",
        timeout=60000,
    )


def get_column_widths(page: Page) -> list[float]:
    """Helper function to get the current widths of the columns."""
    # The selector needs to be specific enough to get the column containers
    return page.locator(
        'div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] > div'
    ).all_bounding_boxes()


@pytest.mark.e2e
def test_column_resize(page: Page):
    """
    Tests if dragging a resize handle correctly changes the column widths.
    """
    # Locate the component iframe and the first resize handle
    iframe = page.frame_locator(
        'iframe[title="streamlit_adjustable_columns.streamlit_adjustable_columns"]'
    )
    handle = iframe.locator(".resize-handle").first
    expect(handle).to_be_visible()

    # Get initial column widths
    initial_widths = get_column_widths(page)
    expect(len(initial_widths)).to_equal(3)

    # Simulate dragging the resize handle to the right
    handle_bb = handle.bounding_box()
    page.mouse.move(
        handle_bb["x"] + handle_bb["width"] / 2,
        handle_bb["y"] + handle_bb["height"] / 2,
    )
    page.mouse.down()
    page.mouse.move(handle_bb["x"] + 150, handle_bb["y"] + handle_bb["height"] / 2)
    page.mouse.up()

    # Wait for the app to re-run and settle
    page.get_by_role("img", name="Running...").is_hidden(timeout=30000)
    page.wait_for_timeout(1000)  # Additional wait for UI to stabilize

    # Get new column widths
    new_widths = get_column_widths(page)
    expect(len(new_widths)).to_equal(3)

    # Assert that the first column is now wider
    assert new_widths[0]["width"] > initial_widths[0]["width"]
    # Assert that the second column is now narrower
    assert new_widths[1]["width"] < initial_widths[1]["width"]
