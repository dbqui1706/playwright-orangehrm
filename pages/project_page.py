"""Page Object Model for Project management in OrangeHRM."""
import logging
from playwright.sync_api import Page

from config import BASE_URL
from pages.base import BasePage

logger = logging.getLogger(__name__)


class ProjectPage(BasePage):
    """Page object for managing Projects in Time module."""

    # URL
    PROJECT_LIST_URL = "time/viewProjects"

    # Locators - Add Project Button
    ADD_PROJECT_BUTTON = "button:has-text('Add')"

    # Locators - Add/Edit Project Form
    PROJECT_NAME_INPUT = "//label[text()='Name']/parent::div/following-sibling::div//input"
    CUSTOMER_NAME_INPUT = "//label[text()='Customer Name']/parent::div/following-sibling::div//input"
    CUSTOMER_OPTIONS =  "//div[@role='listbox']//div[@role='option']//span[contains(text(), '{}')]"
    
    PROJECT_ADMIN_INPUT = "//label[text()='Project Admin']/parent::div/following-sibling::div//input"
    PROJECT_ADMIN_DROPDOWN_OPTIONS = "//div[@role='listbox']//div[@role='option']"
    DESCRIPTION_TEXTAREA = "//label[text()='Description']/parent::div/following-sibling::div//textarea"
    SAVE_BUTTON = "button[type='submit']"
    CANCEL_BUTTON = "button:has-text('Cancel')"

    # Locators - Validation Messages
    REQUIRED_ERROR_MESSAGE = ".oxd-input-field-error-message"
    ERROR_MESSAGE_REQUIRED = "//span[contains(@class, 'oxd-input-field-error-message') and text()='Required']"
    ERROR_MESSAGE_DUPLICATE = "//span[contains(@class, 'oxd-input-field-error-message') and text()='Already exists']"

    # Locators - Success Message
    SUCCESS_MESSAGE = ".oxd-toast-content--success"
    SUCCESS_MESSAGE_TEXT = "//p[contains(@class, 'oxd-text--toast-message') and text()='Successfully Saved']"

    # Locators - Project List Table
    PROJECT_TABLE = ".oxd-table"
    PROJECT_TABLE_ROWS = ".oxd-table-body .oxd-table-card"
    NO_RECORDS_MESSAGE = "//div[contains(@class, 'orangehrm-horizontal-padding')]//span[text()='No Records Found']"

    # Locators - Search
    SEARCH_PROJECT_INPUT = "//label[text()='Project']/parent::div/following-sibling::div//input"
    SEARCH_PROJECT_DROPDOWN_OPTIONS = "//div[@role='listbox']//div[@role='option']//span[contains(text(), '{}')]"
    
    SEARCH_BUTTON = "button[type='submit']"

    # Locators - Project Admins (for multiple admins)
    REMOVE_ADMIN_BUTTON = "//i[contains(@class, 'bi-trash')]"

    def __init__(self, page: Page):
        """Initialize ProjectPage.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        logger.info("ProjectPage initialized")

    def navigate_to_project_page(self):
        """Navigate to Project management page."""
        logger.info("Navigating to Project page")
        full_url = BASE_URL + self.PROJECT_LIST_URL
        self.page.goto(full_url)
        self.page.wait_for_load_state('networkidle')

    def click_add_project(self):
        """Click the Add Project button."""
        logger.info("Clicking Add Project button")
        self._click(self.ADD_PROJECT_BUTTON)
        self.page.wait_for_timeout(1000)

    def enter_project_name(self, name: str):
        """Enter project name in the input field.

        Args:
            name: Project name to enter
        """
        logger.info(f"Entering project name: {name}")
        self._send_keys(self.PROJECT_NAME_INPUT, name)

    def enter_customer_name(self, customer_name: str):
        """Select a customer from the dropdown.

        Args:
            customer_name: Customer name to select
        """
        logger.info(f"Selecting customer: {customer_name}")
        # Click dropdown to open
        self._send_keys(self.CUSTOMER_NAME_INPUT, customer_name[:3])  # Type first 3 chars
        self.page.wait_for_timeout(1000)
        # Select from dropdown options
        option_locator = self.CUSTOMER_OPTIONS.format(customer_name)
        if self._is_element_visible(option_locator, timeout=3):
            self._click(option_locator)
        else:
            logger.warning(f"Customer '{customer_name}' not found in dropdown")

    def select_project_admin(self, admin_name: str):
        """Select a project admin from the autocomplete dropdown.

        Args:
            admin_name: Admin name to select (first few characters trigger autocomplete)
        """
        logger.info(f"Selecting project admin: {admin_name}")
        # Type in the input to trigger autocomplete
        input_project_admin = self.page.locator(self.PROJECT_ADMIN_INPUT)
        input_project_admin.fill("")  # Clear existing input
        input_project_admin.type(admin_name)  # Type first 3 chars
        self.page.wait_for_timeout(1500)
        # Sử dụng keyboard: Arrow Down để chọn option đầu tiên, rồi Enter
        input_project_admin.press("ArrowDown")
        self.page.wait_for_timeout(300)
        input_project_admin.press("Enter")

        logger.info(f"Successfully selected project: {admin_name}")
        self.page.wait_for_timeout(500)

        # # Select from dropdown options
        # option_locator = f"//div[@role='listbox']//div[@role='option']//span[contains(text(), '{admin_name}')]"
        # if self._is_element_visible(option_locator, timeout=3):
        #     self._click(option_locator)
        # else:
        #     logger.warning(f"Admin '{admin_name}' not found in dropdown")

    def add_multiple_project_admins(self, admin_names: list):
        """Add multiple project admins.

        Args:
            admin_names: List of admin names to add
        """
        logger.info(f"Adding multiple project admins: {admin_names}")
        for admin_name in admin_names:
            self.select_project_admin(admin_name)
            self.page.wait_for_timeout(500)

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

    def add_project(self, name: str, customer_name: str, admin_name: str = "", description: str = ""):
        """Add a new project.

        Args:
            name: Project name
            customer_name: Customer name to select
            admin_name: Optional project admin name (default: empty)
            description: Optional description (default: empty)
        """
        logger.info(f"Adding project: {name} for customer: {customer_name}")
        self.click_add_project()
        self.enter_project_name(name)
        self.enter_customer_name(customer_name)
        if admin_name:
            self.select_project_admin(admin_name)
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

    def get_error_message_text(self) -> str:
        """Get the text of the first error message.

        Returns:
            str: Error message text
        """
        if self._is_element_visible(self.REQUIRED_ERROR_MESSAGE, timeout=2):
            return self._get_text(self.REQUIRED_ERROR_MESSAGE)
        return ""

    def search_project(self, project_name: str):
        """Search for a project by name.

        Args:
            project_name: Project name to search for
        """
        logger.info(f"Searching for project: {project_name}")
        self._send_keys(self.SEARCH_PROJECT_INPUT, project_name)  # Type all but last 3 chars
        
        # Select from dropdown options
        option_locator = self.SEARCH_PROJECT_DROPDOWN_OPTIONS.format(project_name)
        if self._is_element_visible(option_locator, timeout=3):
            self._click(option_locator)
        else:
            logger.warning(f"Project '{project_name}' not found in search dropdown")
        
        self._click(self.SEARCH_BUTTON)
        self.page.wait_for_timeout(2000)

    def is_project_in_table(self, project_name: str) -> bool:
        """Check if project exists in the table.

        Args:
            project_name: Project name to look for

        Returns:
            bool: True if project is found in table
        """
        self.page.wait_for_timeout(1000)
        # Check if "No Records Found" message is visible
        if self._is_element_visible(self.NO_RECORDS_MESSAGE, timeout=2):
            return False
        
        # Search for project name in table
        rows = self._find_elements(self.PROJECT_TABLE_ROWS)
        for i in range(rows.count()):
            if project_name in rows.nth(i).text_content():
                return True
        
        return False

    def get_project_name_input_value(self) -> str:
        """Get the current value in the project name input field.

        Returns:
            str: Current input value
        """
        return self.page.locator(self.PROJECT_NAME_INPUT).input_value()

    def get_number_of_error_messages(self) -> int:
        """Count the number of error messages displayed.

        Returns:
            int: Number of error messages
        """
        error_elements = self._find_elements(self.REQUIRED_ERROR_MESSAGE)
        return error_elements.count()

    # ==================== EDIT PROJECT ====================

    def click_edit_project(self, project_name: str):
        """Click edit button for a specific project.

        Args:
            project_name: Project name to edit
        """
        logger.info(f"Clicking edit for project: {project_name}")
        # Find project row and click edit button
        project_row = f"//div[contains(@class, 'oxd-table-card')]//div[text()='{project_name}']"
        if self._is_element_visible(project_row, timeout=3):
            edit_button = f"{project_row}/ancestor::div[contains(@class, 'oxd-table-card')]//button//i[contains(@class, 'bi-pencil')]"
            self._click(edit_button)
            self.page.wait_for_timeout(1000)

    def edit_project_name(self, old_name: str, new_name: str):
        """Edit project name.

        Args:
            old_name: Current project name
            new_name: New project name
        """
        logger.info(f"Editing project '{old_name}' to '{new_name}'")
        self.click_edit_project(old_name)
        self._send_keys(self.PROJECT_NAME_INPUT, new_name)
        self.click_save()

    def edit_project_customer(self, project_name: str, new_customer: str):
        """Edit project customer.

        Args:
            project_name: Project name to edit
            new_customer: New customer name
        """
        logger.info(f"Editing project '{project_name}' customer to '{new_customer}'")
        self.click_edit_project(project_name)
        self.enter_customer_name(new_customer)
        self.click_save()

    # ==================== SEARCH/FILTER ====================

    SEARCH_CUSTOMER_INPUT = "//label[text()='Customer Name']/parent::div/following-sibling::div//input"
    SEARCH_CUSTOMER_DROPDOWN_OPTIONS = "//div[@role='listbox']//div[@role='option']//span[contains(text(), '{}')]"

    SEARCH_PROJECT_ADMIN_INPUT = "//label[text()='Project Admin']/parent::div/following-sibling::div//input"
    SEARCH_ADMIN_DROPDOWN_OPTIONS = "//div[@role='listbox']//div[@role='option']//span[contains(text(), '{}')]"

    def search_by_customer(self, customer_name: str):
        """Search/filter projects by customer.

        Args:
            customer_name: Customer name to filter by
        """
        logger.info(f"Filtering projects by customer: {customer_name}")
        self._send_keys(self.SEARCH_CUSTOMER_INPUT, customer_name[:3])
        self.page.wait_for_timeout(1000)

        option_locator = self.SEARCH_CUSTOMER_DROPDOWN_OPTIONS.format(customer_name)
        if self._is_element_visible(option_locator, timeout=3):
            self._click(option_locator)

        self._click(self.SEARCH_BUTTON)
        self.page.wait_for_timeout(2000)

    def search_by_project_admin(self, admin_name: str):
        """Search/filter projects by project admin.

        Args:
            admin_name: Project admin name to filter by
        """
        logger.info(f"Filtering projects by admin: {admin_name}")
        self._send_keys(self.SEARCH_PROJECT_ADMIN_INPUT, admin_name[:3])
        self.page.wait_for_timeout(1000)

        option_locator = self.SEARCH_ADMIN_DROPDOWN_OPTIONS.format(admin_name)
        if self._is_element_visible(option_locator, timeout=3):
            self._click(option_locator)

        self._click(self.SEARCH_BUTTON)
        self.page.wait_for_timeout(2000)

    def get_table_row_count(self) -> int:
        """Get number of rows in project table.

        Returns:
            int: Number of project rows
        """
        if self._is_element_visible(self.NO_RECORDS_MESSAGE, timeout=2):
            return 0
        rows = self._find_elements(self.PROJECT_TABLE_ROWS)
        return rows.count()

    # ==================== DELETE PROJECT ====================

    DELETE_PROJECT_BUTTON = "//button[@class='oxd-icon-button oxd-table-cell-action-space']//i[contains(@class, 'bi-trash')]"
    CONFIRM_DELETE_BUTTON = "//button[contains(@class, 'oxd-button--label-danger')]"
    DELETE_WARNING_MESSAGE = "//p[contains(text(), 'timesheet')]"

    def delete_project(self, project_name: str):
        """Delete a project.

        Args:
            project_name: Project name to delete
        """
        logger.info(f"Deleting project: {project_name}")
        # Find project row and click delete button
        project_row = f"//div[contains(@class, 'oxd-table-card')]//div[text()='{project_name}']"
        if self._is_element_visible(project_row, timeout=3):
            delete_button = f"{project_row}/ancestor::div[contains(@class, 'oxd-table-card')]//button//i[contains(@class, 'bi-trash')]"
            self._click(delete_button)
            self.page.wait_for_timeout(1000)

            # Confirm deletion
            if self._is_element_visible(self.CONFIRM_DELETE_BUTTON, timeout=2):
                self._click(self.CONFIRM_DELETE_BUTTON)
                self.page.wait_for_timeout(2000)

    def is_delete_warning_visible(self) -> bool:
        """Check if delete warning message is visible (for projects with timesheet data).

        Returns:
            bool: True if warning is visible
        """
        return self._is_element_visible(self.DELETE_WARNING_MESSAGE, timeout=3)

    # ==================== GUI VERIFICATION ====================

    def get_customer_dropdown_options(self) -> list:
        """Get all customer options from dropdown.

        Returns:
            list: List of customer names
        """
        logger.info("Getting customer dropdown options")
        self.click_add_project()
        self._click(self.CUSTOMER_NAME_INPUT)
        self.page.wait_for_timeout(1000)

        # Get all options
        options = self._find_elements("//div[@role='listbox']//div[@role='option']")
        customer_names = []
        for i in range(options.count()):
            text = options.nth(i).text_content()
            if text:
                customer_names.append(text.strip())

        self.click_cancel()
        return customer_names

    def verify_project_admin_multiselect(self) -> bool:
        """Verify that project admin field supports multi-select.

        Returns:
            bool: True if multi-select works
        """
        logger.info("Verifying project admin multi-select")
        self.click_add_project()

        # Try to add multiple admins
        self.select_project_admin("Admin")
        self.page.wait_for_timeout(500)

        # Check if we can add another admin (field should still be available)
        admin_input_visible = self._is_element_visible(self.PROJECT_ADMIN_INPUT, timeout=2)

        self.click_cancel()
        return admin_input_visible
