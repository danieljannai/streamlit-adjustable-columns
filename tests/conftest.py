"""Pytest configuration and fixtures for streamlit-expandable-columns tests."""

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments."""
    return {
        **browser_type_launch_args,
        "headless": True,  # Run in headless mode for CI/CD
    }


@pytest.fixture(autouse=True)
def wait_for_iframe(page, request):
    """Wait for the component iframe to load before each e2e test."""
    if "e2e" in request.keywords:
        # Wait up to 30 seconds for the iframe to be attached to the DOM
        page.wait_for_selector(
            'iframe[title="streamlit_expandable_columns.streamlit_expandable_columns"]',
            timeout=30000,
            state="attached",
        )


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    )
    config.addinivalue_line("markers", "e2e: marks tests as end-to-end tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
