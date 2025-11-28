"""Base page class containing common methods for all page objects using Playwright."""
import logging
from playwright.sync_api import Page, Locator, expect
from config import DEFAULT_WAIT_TIMEOUT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasePage:
    """Base page class with common methods for interacting with web elements."""

    def __init__(self, page: Page, timeout: int = DEFAULT_WAIT_TIMEOUT):
        self.page = page
        self.timeout = timeout * 1000  # Convert to milliseconds for Playwright

    def _find_element(self, selector: str) -> Locator:
        logger.info(f"Finding element: {selector}")
        return self.page.locator(selector)

    def _find_elements(self, selector: str) -> Locator:
        logger.info(f"Finding elements: {selector}")
        return self.page.locator(selector)

    def _click(self, selector: str) -> None:
        logger.info(f"Clicking element: {selector}")
        self.page.locator(selector).click(timeout=self.timeout)

    def _send_keys(self, selector: str, text: str, clear: bool = True) -> None:
        """Send keys to an element after optionally clearing it.

        Args:
            selector: The CSS selector
            text: The text to send
            clear: Whether to clear the field first (default: True)
        """
        logger.info(f"Sending keys to element: {selector}")
        element = self.page.locator(selector)
        if clear:
            element.clear()
        element.fill(text)

    def _get_text(self, selector: str) -> str:
        
        return self.page.locator(selector).text_content()

    def _is_element_visible(self, selector: str, timeout: int = 5) -> bool:
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout * 1000)
            return True
        except Exception:
            logger.debug(f"Element not visible: {selector}")
            return False

    def _wait_for_element_to_disappear(self, selector: str, timeout: int = 10) -> bool:
        try:
            self.page.locator(selector).wait_for(state="hidden", timeout=timeout * 1000)
            return True
        except Exception:
            logger.warning(f"Element did not disappear: {selector}")
            return False

    def _get_attribute(self, selector: str, attribute: str) -> str:
        """Get an attribute value from an element.

        Args:
            selector: The CSS selector
            attribute: The attribute name

        Returns:
            str: The attribute value
        """
        return self.page.locator(selector).get_attribute(attribute)
