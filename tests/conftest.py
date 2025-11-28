"""Pytest configuration file containing fixtures and hooks for Playwright."""
import pytest
import os
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from config import SCREENSHOTS_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def browser():
    """Create a Firefox browser instance for the entire test session.

    Yields:
        Browser: Playwright Firefox Browser instance
    """
    logger.info("Launching Firefox browser")
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(
            headless=False,  # Set True for headless mode
            slow_mo=100  # Slow down by 100ms for better visibility (optional)
        )
        yield browser
        logger.info("Closing Firefox browser")
        browser.close()

@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    """Create a new browser page for each test.

    Args:
        browser: Playwright Browser instance

    Yields:
        Page: Configured Playwright Page instance
    """
    logger.info("Creating new browser context and page")

    # Create a new context with viewport settings fully responsive

    context: BrowserContext = browser.new_context(
        viewport={'width': 1280, 'height': 1024}
    )

    # Create a new page
    page = context.new_page()

    # Set default timeout
    page.set_default_timeout(10000)  # 10 seconds

    logger.info("Page initialized successfully")
    yield page

    logger.info("Closing page and context")
    page.close()
    context.close()


@pytest.fixture(scope="function")
def driver_init(page: Page, request):
    """Initialize page object and attach to test class for compatibility.

    Args:
        page: Playwright Page instance
        request: Pytest request object

    Yields:
        Page: Configured Playwright Page instance
    """
    # Attach page to test class (maintaining compatibility with existing tests)
    request.cls.driver = page
    request.cls.page = page

    yield page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots on test failure.

    Args:
        item: The test item
        call: The test call
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        logger.warning(f"Test failed: {item.name}")

        try:
            # Get page from test class
            page = item.cls.page if hasattr(item.cls, 'page') else item.cls.driver

            # Create screenshots directory if it doesn't exist
            if not os.path.exists(SCREENSHOTS_DIR):
                os.makedirs(SCREENSHOTS_DIR)
                logger.info(f"Created screenshots directory: {SCREENSHOTS_DIR}")

            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"{item.name}_{timestamp}_failure.png"
            screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_filename)

            # Save screenshot
            page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"Screenshot saved: {screenshot_path}")

            # Add screenshot to HTML report if pytest-html is installed
            if hasattr(report, 'extra'):
                try:
                    import pytest_html
                    report.extra.append(pytest_html.extras.image(screenshot_path))
                except ImportError:
                    logger.debug("pytest-html not installed, skipping report attachment")

        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")