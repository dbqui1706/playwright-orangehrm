"""PIM page object containing employee search and management actions."""
from playwright.sync_api import Page
from pages.base import BasePage
from config import SEARCH_RESULT_WAIT
import logging

logger = logging.getLogger(__name__)


class PIMPage(BasePage):
    """Page object for the PIM (Personal Information Management) page."""
    
    # Selectors
    ADD_EMPLOYEE_BUTTON = 'a:has-text("Add Employee")'
    EMPLOYEE_LIST_LINK = 'a:has-text("Employee List")'
    EMPLOYEE_NAME_INPUT = '//label[text()="Employee Name"]/../following-sibling::div//input'
    SEARCH_BUTTON = 'button[type="submit"]'
    NO_RECORDS_FOUND_MESSAGE = '//*[text()="No Records Found"]'
    FIRST_ROW_CELL = '.oxd-table-card .oxd-table-row .oxd-table-cell'
    ROWS_ITEMS = '.oxd-table-card'
    AUTOCOMPLETE_OPTIONS = '.oxd-autocomplete-option'
    LOADING_SPINNER = '.oxd-loading-spinner'

    def __init__(self, page: Page):
        """Initialize the PIM page.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)

    def search_for_employee_by_name(self, employee_name: str) -> None:
        """Search for an employee by their name, handling autocomplete.

        Args:
            employee_name: The name of the employee to search for
        """
        logger.info(f"Searching for employee: {employee_name}")
        self._send_keys(self.EMPLOYEE_NAME_INPUT, employee_name, clear=True)
       
        # Wait for and select autocomplete option if available
        try:
            self.page.wait_for_selector(self.AUTOCOMPLETE_OPTIONS, timeout=SEARCH_RESULT_WAIT * 1000)
            options = self.page.locator(self.AUTOCOMPLETE_OPTIONS).all()
            
            if options:
                for option in options:
                    option_text = option.text_content()
                    if employee_name.lower() in option_text.lower():
                        logger.info(f"Selecting autocomplete option: {option_text}")
                        option.click()
                        break
        except Exception:
            logger.info("No autocomplete options found, proceeding with search")

        self._click(self.SEARCH_BUTTON)

        # Wait for loading spinner to disappear (if present)
        self._wait_for_loading_to_complete()
        

    def _wait_for_loading_to_complete(self, timeout: int = SEARCH_RESULT_WAIT) -> None:
        """Wait for the loading spinner to disappear.

        Args:
            timeout: Maximum time to wait in seconds
        """
        try:
            self.page.locator(self.LOADING_SPINNER).wait_for(state="hidden", timeout=timeout * 1000)
        except Exception:
            logger.debug("No loading spinner detected or already completed")

    def is_no_records_found_message_visible(self) -> bool:
        """Check if the 'No Records Found' message is displayed.

        Returns:
            bool: True if message is visible, False otherwise
        """
        toast_visible = self._is_element_visible(self.NO_RECORDS_FOUND_MESSAGE) 
        items = self.page.locator(self.ROWS_ITEMS).all()
        toast = self._get_text(self.NO_RECORDS_FOUND_MESSAGE) if toast_visible else ""
        
        logger.info(f"'No Records Found' message visibility: {toast_visible}, text: '{toast}'")
        logger.info(f"Number of search result items found: {len(items)}")
        
        return toast_visible or len(items) == 0

    def get_first_row_text(self) -> str:
        """Get the text content of the first result row.

        Returns:
            str: Text from the first row cell
        """
        return self._get_text(self.FIRST_ROW_CELL)

    def are_search_results_visible(self) -> bool:
        """Check if search results are visible.

        Returns:
            bool: True if results are visible, False otherwise
        """
        return self._is_element_visible(self.FIRST_ROW_CELL)

    def click_add_employee(self) -> None:
        """Navigate to Add Employee page by clicking the Add Employee button."""
        logger.info("Navigating to Add Employee page")
        self._click(self.ADD_EMPLOYEE_BUTTON)
