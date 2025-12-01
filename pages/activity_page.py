"""Page Object Model for Activity management in OrangeHRM."""
import logging
from playwright.sync_api import Page
from pages.base import BasePage
from config import BASE_URL
logger = logging.getLogger(__name__)


class ActivityPage(BasePage):
    """Page object for managing Activities in Time module."""

    # URL
    PROJECT_LIST_URL = "time/viewProjects"

    # Locators - Project Actions
    EDIT_PROJECT_BUTTON = "//button[@class='oxd-icon-button oxd-table-cell-action-space']//i[contains(@class, 'bi-pencil')]"

    # Locators - Add Activity Button (in project edit page)
    # More specific selector - looks for Add button in Activities section
    ADD_ACTIVITY_BUTTON = "//h6[text()='Activities']/following::button[contains(., 'Add')][1]"

    # Locators - Add/Edit Activity Form
    ACTIVITY_NAME_INPUT = "//*[@id='app']/div[2]/div[2]/div[2]/div/div[2]/div[5]/div/div/div/form/div[1]/div/div[2]/input"
    SAVE_BUTTON = "//*[@id='app']/div[2]/div[2]/div[2]/div/div[2]/div[5]/div/div/div/form/div[2]/button[2]"
    CANCEL_BUTTON = "button:has-text('Cancel')"

    # Locators - Validation Messages
    REQUIRED_ERROR_MESSAGE = ".oxd-input-field-error-message"
    ERROR_MESSAGE_REQUIRED = "//span[contains(@class, 'oxd-input-field-error-message') and text()='Required']"
    ERROR_MESSAGE_DUPLICATE = "//span[contains(@class, 'oxd-input-field-error-message') and text()='Already exists']"
    ERROR_MESSAGE_EXCEEDS_LIMIT = "//span[contains(@class, 'oxd-input-field-error-message') and contains(text(), 'Should not exceed')]"
    # ERROR_MESSAGE_ACTIVITY_EXCEEDS_LIMIT = "//span[contains(@class, 'oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message') and contains(text(), 'Should not exceed 100 characters')]"
    ERROR_MESSAGE_ACTIVITY_EXCEEDS_LIMIT = "//*[@id='app']/div[2]/div[2]/div[2]/div/div[2]/div[5]/div/div/div/form/div[1]/div/span"
    # Locators - Success Message
    SUCCESS_MESSAGE = ".oxd-toast-content--success"
    SUCCESS_MESSAGE_TEXT = "//p[contains(@class, 'oxd-text--toast-message') and text()='Successfully Saved']"

    # Locators - Activity List Table
    ACTIVITY_TABLE = ".oxd-table"
    ACTIVITY_TABLE_ROWS = ".oxd-table-body .oxd-table-card"
    NO_RECORDS_MESSAGE = "//div[contains(@class, 'orangehrm-horizontal-padding')]//span[text()='No Records Found']"

    # Locators - Delete Activity
    DELETE_ACTIVITY_BUTTON = "//button[@class='oxd-icon-button oxd-table-cell-action-space']//i[contains(@class, 'bi-trash')]"
    CONFIRM_DELETE_BUTTON = "//button[contains(@class, 'oxd-button--label-danger')]"

    def __init__(self, page: Page):
        """Initialize ActivityPage.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        logger.info("ActivityPage initialized")

    def navigate_to_project_list(self):
        """Navigate to Project list page."""
        logger.info("Navigating to Project list page")
        full_url = BASE_URL + self.PROJECT_LIST_URL
        self.page.goto(full_url)
        self.page.wait_for_load_state('networkidle')

    def search_and_edit_project(self, project_name: str):
        """Search for a project and click edit button.

        Args:
            project_name: Project name to search and edit
        """
        logger.info(f"Searching and editing project: {project_name}")
        # Search for project in table
        project_row = f"//div[contains(@class, 'oxd-table-card')]//div[text()='{project_name}']"
        if self._is_element_visible(project_row, timeout=3):
            # Click edit button in the same row
            edit_button = f"{project_row}/ancestor::div[contains(@class, 'oxd-table-card')]//button//i[contains(@class, 'bi-pencil')]"
            self._click(edit_button)
            self.page.wait_for_timeout(1000)
        else:
            logger.warning(f"Project '{project_name}' not found")

    def click_add_activity(self):
        """Click the Add Activity button."""
        logger.info("Clicking Add Activity button")
        self._click(self.ADD_ACTIVITY_BUTTON)
        # Wait for the new row/form to appear
        self.page.wait_for_timeout(2000)
        # Wait for input field to be visible
        self.page.wait_for_selector(self.ACTIVITY_NAME_INPUT, state="visible", timeout=5000)

    def enter_activity_name(self, name: str):
        """Enter activity name in the input field.

        Args:
            name: Activity name to enter
        """
        logger.info(f"Entering activity name: {name}")
        # Clear any existing value first
        input_field = self.page.locator(self.ACTIVITY_NAME_INPUT)
        input_field.clear()
        self.page.wait_for_timeout(500)
        # Enter new value
        self._send_keys(self.ACTIVITY_NAME_INPUT, name)

    def click_save(self):
        """Click the Save button."""
        logger.info("Clicking Save button")
        self._click(self.SAVE_BUTTON)
        self.page.wait_for_timeout(2000)

    def click_cancel(self):
        """Click the Cancel button."""
        logger.info("Clicking Cancel button")
        self._click(self.CANCEL_BUTTON)

    def add_activity(self, project_name: str, activity_name: str):
        """Add a new activity to a project.

        Args:
            project_name: Project name to add activity to
            activity_name: Activity name
        """
        logger.info(f"Adding activity '{activity_name}' to project '{project_name}'")
        self.click_add_activity()
        self.enter_activity_name(activity_name)
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

    def is_required_error_visible(self) -> bool:
        """Check if 'Required' error message is visible.

        Returns:
            bool: True if Required error is visible
        """
        return self._is_element_visible(self.ERROR_MESSAGE_REQUIRED, timeout=3)

    def is_duplicate_error_visible(self) -> bool:
        """Check if 'Already exists' error message is visible.

        Returns:
            bool: True if duplicate error is visible
        """
        return self._is_element_visible(self.ERROR_MESSAGE_DUPLICATE, timeout=3)

    def is_exceeds_limit_error_visible(self) -> bool:
        """Check if 'Should not exceed' error message is visible.

        Returns:
            bool: True if exceeds limit error is visible
        """
        return self._is_element_visible(self.ERROR_MESSAGE_EXCEEDS_LIMIT, timeout=3)

    def is_activity_exceeds_limit_error_visible(self) -> bool:
        """Check if 'Should not exceed 100 characters' error message is visible.

        Returns:
            bool: True if activity exceeds limit error is visible
        """
        return self._is_element_visible(self.ERROR_MESSAGE_ACTIVITY_EXCEEDS_LIMIT, timeout=3)

    def get_activity_name_input_value(self) -> str:
        """Get the current value in the activity name input field.

        Returns:
            str: Current input value
        """
        return self.page.locator(self.ACTIVITY_NAME_INPUT).input_value()

    def is_activity_in_table(self, activity_name: str) -> bool:
        """Check if activity exists in the table.

        Args:
            activity_name: Activity name to look for

        Returns:
            bool: True if activity is found in table
        """
        logger.info(f"Checking if activity '{activity_name}' is in table")
        self.page.wait_for_timeout(1000)

        # Check if "No Records Found" message is visible
        if self._is_element_visible(self.NO_RECORDS_MESSAGE, timeout=2):
            return False

        # Search for activity name in table (text is in a nested div)
        activity_cell = f"//div[contains(@class, 'oxd-table-cell')]//div[text()='{activity_name}']"
        return self._is_element_visible(activity_cell, timeout=2)

    def delete_activity(self, activity_name: str):
        """Delete an activity from the table.

        Args:
            activity_name: Activity name to delete
        """
        logger.info(f"Deleting activity: {activity_name}")
        # Find the activity row and click delete button
        activity_row = f"//div[contains(@class, 'oxd-table-card')]//div[text()='{activity_name}']"
        if self._is_element_visible(activity_row, timeout=3):
            delete_button = f"{activity_row}/ancestor::div[contains(@class, 'oxd-table-card')]//button//i[contains(@class, 'bi-trash')]"
            self._click(delete_button)
            self.page.wait_for_timeout(1000)
            # Confirm deletion
            if self._is_element_visible(self.CONFIRM_DELETE_BUTTON, timeout=2):
                self._click(self.CONFIRM_DELETE_BUTTON)
                self.page.wait_for_timeout(2000)

    def scroll_to_activity_list(self):
        """Scroll to the activity list section."""
        logger.info("Scrolling to activity list section")
        self.page.wait_for_timeout(1000)
        self.page.evaluate("window.scrollBy(0, 500);")
        self.page.wait_for_timeout(1000)
