"""Page Object Model for Customer management in OrangeHRM."""
import logging
import enum
from playwright.sync_api import Page
from pages.base import BasePage
from config import BASE_URL

logger = logging.getLogger(__name__)

# Enum for Error Messages
class CustomerErrorMessages(enum.Enum):
    REQUIRED = 1
    EXCEEDS_LIMIT = 2
    DUPLICATE = 3

class CustomerPage(BasePage):
    """Page object for managing Customers in Time module."""

    # URL
    CUSTOMER_LIST_URL = "time/viewCustomers"

    # Locators - Add Customer Button
    ADD_CUSTOMER_BUTTON = "button:has-text('Add')"

    # Locators - Add/Edit Customer Form
    CUSTOMER_NAME_INPUT = "//label[text()='Name']/parent::div/following-sibling::div//input"
    DESCRIPTION_TEXTAREA = "//label[text()='Description']/parent::div/following-sibling::div//textarea"
    SAVE_BUTTON = "button[type='submit']"
    CANCEL_BUTTON = "button:has-text('Cancel')"

    # Locators - Validation Messages
    REQUIRED_ERROR_MESSAGE = ".oxd-input-field-error-message"
    ERROR_MESSAGE_REQUIRED = "//span[contains(@class, 'oxd-input-field-error-message') and text()='Required']"
    ERROR_MESSAGE_EXCEEDS_LIMIT = "//span[contains(@class, 'oxd-input-field-error-message') and text()='Should not exceed 50 characters']"
    ERROR_MESSAGE_DUPLICATE = "//span[contains(@class, 'oxd-input-field-error-message') and text()='Already exists']"

    # Locators - Success Message
    SUCCESS_MESSAGE = ".oxd-toast-content--success"
    SUCCESS_MESSAGE_TEXT = "//p[contains(@class, 'oxd-text--toast-message') and text()='Successfully Saved']"

    # Locators - Customer List Table
    CUSTOMER_TABLE = ".oxd-table"
    CUSTOMER_TABLE_ROWS = ".oxd-table-body .oxd-table-card"
    NO_RECORDS_MESSAGE = "//div[contains(@class, 'orangehrm-horizontal-padding')]//span[text()='No Records Found']"

    # Locators - Search
    SEARCH_CUSTOMER_INPUT = "//label[text()='Customer Name']/parent::div/following-sibling::div//input"
    SEARCH_BUTTON = "button[type='submit']"

    def __init__(self, page: Page):
        """Initialize CustomerPage.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        logger.info("CustomerPage initialized")

    def navigate_to_customer_page(self):
        """Navigate to Customer management page."""
        logger.info("Navigating to Customer page")
        full_url = BASE_URL + self.CUSTOMER_LIST_URL
        self.page.goto(full_url)
        self.page.wait_for_load_state('networkidle')

    def click_add_customer(self):
        """Click the Add Customer button."""
        logger.info("Clicking Add Customer button")
        self._click(self.ADD_CUSTOMER_BUTTON)
        self.page.wait_for_timeout(1000)

    def enter_customer_name(self, name: str):
        """Enter customer name in the input field.

        Args:
            name: Customer name to enter
        """
        logger.info(f"Entering customer name: {name}")
        self._send_keys(self.CUSTOMER_NAME_INPUT, name)

    def enter_description(self, description: str):
        """Enter description in the textarea.

        Args:
            description: Description text to enter
        """
        logger.info(f"Entering description: {description}")
        self._send_keys(self.DESCRIPTION_TEXTAREA, description)

    def click_save(self):
        """Click the Save button."""
        logger.info("Clicking Save button")
        self._click(self.SAVE_BUTTON)
        self.page.wait_for_timeout(2000)

    def click_cancel(self):
        """Click the Cancel button."""
        logger.info("Clicking Cancel button")
        self._click(self.CANCEL_BUTTON)

    def add_customer(self, name: str, description: str = ""):
        """Add a new customer with name and optional description.

        Args:
            name: Customer name
            description: Optional description (default: empty)
        """
        logger.info(f"Adding customer: {name}")
        self.click_add_customer()

        self.enter_customer_name(name)
        if description:
            self.enter_description(description)
        self.click_save()

    def is_success_message_visible(self) -> bool:
        """Check if success message is displayed.

        Returns:
            bool: True if success message is visible
        """
        return self._is_element_visible(self.SUCCESS_MESSAGE, timeout=5)

    def get_required_error_messages(self) -> list:
        """Get all 'Required' field error messages.

        Returns:
            list: List of error message texts
        """
        logger.info("Getting required error messages")
        self.page.wait_for_timeout(1000)
        error_elements = self._find_elements(self.REQUIRED_ERROR_MESSAGE)
        count = error_elements.count()
        return [error_elements.nth(i).text_content() for i in range(count)]

    def is_required_error_message(self, error_type: CustomerErrorMessages) -> bool:
        if error_type == CustomerErrorMessages.REQUIRED:
            return self._is_element_visible(self.ERROR_MESSAGE_REQUIRED, timeout=3)
        elif error_type == CustomerErrorMessages.DUPLICATE:
            return self._is_element_visible(self.ERROR_MESSAGE_DUPLICATE, timeout=3)
        elif error_type == CustomerErrorMessages.EXCEEDS_LIMIT:
            return self._is_element_visible(self.ERROR_MESSAGE_EXCEEDS_LIMIT, timeout=3)
        return False

    def is_duplicate_error_visible(self) -> bool:
        """Check if 'Already exists' error message is visible.

        Returns:
            bool: True if duplicate error is visible
        """
        return self._is_element_visible(self.ERROR_MESSAGE_DUPLICATE, timeout=3)

    def get_error_message_text(self) -> str:
        """Get the text of the first error message.

        Returns:
            str: Error message text
        """
        if self._is_element_visible(self.REQUIRED_ERROR_MESSAGE, timeout=2):
            return self._get_text(self.REQUIRED_ERROR_MESSAGE)
        return ""

    def search_customer(self, customer_name: str):
        """Search for a customer by name.

        Args:
            customer_name: Customer_name to search for
        """
        logger.info(f"Searching for customer: {customer_name}")
        # Wait for page to be fully loaded
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(5000)

        # Enter search term
        rows = self._find_elements(self.CUSTOMER_TABLE_ROWS)
        if rows.count() > 0:
            for i in range(rows.count()):
                row = rows.nth(i)
                name_cell = row.locator(".oxd-table-cell").nth(1)
                name_text = name_cell.text_content().strip()
                if name_text == customer_name:
                    logger.info(f"Customer '{customer_name}' found in table")
                    return True

        return False

    def is_customer_in_table(self, customer_name: str) -> bool:
        """Check if customer exists in the table.

        Args:
            customer_name: Customer name to look for

        Returns:
            bool: True if customer is found in table
        """
        logger.info(f"Checking if customer '{customer_name}' is in table")
        self.page.wait_for_timeout(1000)

        # Check if "No Records Found" message is visible
        if self._is_element_visible(self.NO_RECORDS_MESSAGE, timeout=2):
            return False

        # Search for customer name in table
        customer_cell = f"//div[contains(@class, 'oxd-table-cell') and text()='{customer_name}']"
        return self._is_element_visible(customer_cell, timeout=2)

    def get_customer_name_input_value(self) -> str:
        """Get the current value in the customer name input field.

        Returns:
            str: Current input value
        """
        return self.page.locator(self.CUSTOMER_NAME_INPUT).input_value()
