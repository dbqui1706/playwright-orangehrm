"""Add Employee page object for creating new employees in OrangeHRM."""
import logging
import os
import time
from playwright.sync_api import Page

from pages.base import BasePage

logger = logging.getLogger(__name__)


class AddEmployeePage(BasePage):
    """Page object for the Add Employee page."""
    # Logout selectors
    USER_DROPDOWN = '.oxd-userdropdown-tab'
    LOGOUT_LINK = 'a:has-text("Logout")'

    # Selectors for Personal Details Section
    FIRST_NAME_INPUT = 'input[name="firstName"]'
    MIDDLE_NAME_INPUT = 'input[name="middleName"]'
    LAST_NAME_INPUT = 'input[name="lastName"]'
    EMPLOYEE_ID_INPUT = '//label[text()="Employee Id"]/../following-sibling::div//input'

    # Photo Upload
    PHOTO_INPUT = 'input[type="file"]'
    PHOTO_PREVIEW = '.employee-image'

    # Create Login Details Section
    CREATE_LOGIN_TOGGLE = '.oxd-switch-input'
    USERNAME_INPUT = '//label[text()="Username"]/../following-sibling::div//input'
    PASSWORD_INPUT = '//label[text()="Password"]/../following-sibling::div//input'
    CONFIRM_PASSWORD_INPUT = '//label[text()="Confirm Password"]/../following-sibling::div//input'
    STATUS_ENABLED_RADIO = "//label[normalize-space()='Enabled']"
    STATUS_DISABLED_RADIO = "//label[normalize-space()='Disabled']"

    # Buttons
    SAVE_BUTTON = 'button[type="submit"]'
    CANCEL_BUTTON = '//button[normalize-space()="Cancel"]'

    # Success/Error Messages
    SUCCESS_MESSAGE = '.oxd-toast-content--success'
    ERROR_MESSAGE = '.oxd-toast-content--error'
    REQUIRED_ERROR = '//*[contains(@class, "oxd-input-field-error-message")]'

    # Personal Details Page (after save)
    PERSONAL_DETAILS_HEADING = '//h6[text()="Personal Details"]'

    def __init__(self, page: Page):
        """Initialize the Add Employee page.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)

    def enter_first_name(self, first_name: str) -> None:
        """Enter employee's first name.

        Args:
            first_name: The first name to enter
        """
        logger.info(f"Entering first name: {first_name}")
        self._send_keys(self.FIRST_NAME_INPUT, first_name)

    def enter_middle_name(self, middle_name: str) -> None:
        """Enter employee's middle name (optional).

        Args:
            middle_name: The middle name to enter
        """
        logger.info(f"Entering middle name: {middle_name}")
        self._send_keys(self.MIDDLE_NAME_INPUT, middle_name)

    def enter_last_name(self, last_name: str) -> None:
        """Enter employee's last name.

        Args:
            last_name: The last name to enter
        """
        logger.info(f"Entering last name: {last_name}")
        self._send_keys(self.LAST_NAME_INPUT, last_name)

    def get_employee_id(self) -> str:
        """Get the auto-generated or current employee ID.

        Returns:
            str: The current employee ID value
        """
        employee_id = self._get_attribute(self.EMPLOYEE_ID_INPUT, 'value')
        logger.info(f"Current employee ID: {employee_id}")
        return employee_id

    def enter_employee_id(self, employee_id: str) -> None:
        """Enter custom employee ID (overrides auto-generated).

        Args:
            employee_id: The employee ID to enter
        """
        logger.info(f"Entering custom employee ID: {employee_id}")
        self._send_keys(self.EMPLOYEE_ID_INPUT, employee_id)

    def upload_photo(self, photo_path: str) -> bool:
        """Upload employee photo.

        Args:
            photo_path: Absolute path to the photo file

        Returns:
            bool: True if upload successful, False otherwise
        """
        try:
            if not os.path.exists(photo_path):
                logger.error(f"Photo file not found: {photo_path}")
                return False

            # Get file size in MB
            file_size_mb = os.path.getsize(photo_path) / (1024 * 1024)
            logger.info(f"Uploading photo: {photo_path} (Size: {file_size_mb:.2f}MB)")

            # Upload file using Playwright's set_input_files
            self.page.locator(self.PHOTO_INPUT).set_input_files(photo_path)

            logger.info("Photo uploaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to upload photo: {str(e)}")
            return False

    def is_photo_uploaded(self) -> bool:
        """Check if photo preview is displayed.

        Returns:
            bool: True if photo is displayed, False otherwise
        """
        return self._is_element_visible(self.PHOTO_PREVIEW, timeout=3)

    def enable_create_login_details(self) -> None:
        """Toggle the 'Create Login Details' switch to ON."""
        logger.info("Enabling Create Login Details")
        try:
            time.sleep(1)  # Wait for page to load completely

            # Find the toggle switch
            toggle = self.page.locator(self.CREATE_LOGIN_TOGGLE)

            # Check if already checked
            is_checked = toggle.is_checked()

            if not is_checked:
                # Click the toggle
                toggle.click()
                time.sleep(1)  # Wait for form to expand
                logger.info("Create Login Details enabled")
            else:
                logger.info("Create Login Details already enabled")

        except Exception as e:
            logger.error(f"Failed to enable Create Login Details: {str(e)}")
            raise

    def enter_username(self, username: str) -> None:
        """Enter username for login credentials.

        Args:
            username: The username to enter
        """
        logger.info(f"Entering username: {username}")
        self._send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """Enter password for login credentials.

        Args:
            password: The password to enter
        """
        logger.info("Entering password")
        self._send_keys(self.PASSWORD_INPUT, password)

    def enter_confirm_password(self, confirm_password: str) -> None:
        """Enter confirm password.

        Args:
            confirm_password: The password to confirm
        """
        logger.info("Entering confirm password")
        self._send_keys(self.CONFIRM_PASSWORD_INPUT, confirm_password)

    def set_status_enabled(self, enabled: bool = True) -> None:
        """Set the login status to Enabled or Disabled.

        Args:
            enabled: True for Enabled, False for Disabled (default: True)
        """
        logger.info(f"Setting status to: {'Enabled' if enabled else 'Disabled'}")
        try:
            status_radio = self.STATUS_ENABLED_RADIO if enabled else self.STATUS_DISABLED_RADIO
            self._click(status_radio)
        except Exception as e:
            logger.error(f"Failed to set status: {str(e)}")
            raise

    def click_save(self) -> None:
        """Click the Save button."""
        logger.info("Clicking Save button")
        self._click(self.SAVE_BUTTON)
        import time
        time.sleep(2)  # Wait for save action to complete

    def click_cancel(self) -> None:
        """Click the Cancel button."""
        logger.info("Clicking Cancel button")
        self._click(self.CANCEL_BUTTON)

    def is_success_message_visible(self, timeout: int = 10) -> bool:
        """Check if success message is displayed.

        Args:
            timeout: Maximum time to wait for message (default: 10)

        Returns:
            bool: True if success message is visible, False otherwise
        """
        is_visible = self._is_element_visible(self.SUCCESS_MESSAGE, timeout=timeout)
        if is_visible:
            message = self._get_text(self.SUCCESS_MESSAGE)
            logger.info(f"Success message displayed: {message}")
        return is_visible

    def is_error_message_visible(self, timeout: int = 5) -> bool:
        """Check if error message is displayed.

        Args:
            timeout: Maximum time to wait for message (default: 5)

        Returns:
            bool: True if error message is visible, False otherwise
        """
        is_visible = self._is_element_visible(self.ERROR_MESSAGE, timeout=timeout)
        if is_visible:
            message = self._get_text(self.ERROR_MESSAGE)
            logger.info(f"Error message displayed: {message}")
        return is_visible

    def get_required_error_messages(self) -> list:
        """Get all required field error messages.

        Returns:
            list: List of error message texts
        """
        try:
            error_elements = self.page.locator(self.REQUIRED_ERROR).all()
            messages = [elem.text_content() for elem in error_elements if elem.text_content()]
            logger.info(f"Required error messages: {messages}")
            return messages
        except Exception:
            return []

    def is_on_personal_details_page(self, timeout: int = 10) -> bool:
        """Check if redirected to Personal Details page after save.

        Args:
            timeout: Maximum time to wait (default: 10)

        Returns:
            bool: True if on Personal Details page, False otherwise
        """
        is_visible = self._is_element_visible(self.PERSONAL_DETAILS_HEADING, timeout=timeout)
        if is_visible:
            logger.info("Redirected to Personal Details page")
        return is_visible

    def add_employee_basic(self, first_name: str, last_name: str,
                          middle_name: str = "", employee_id: str = None) -> None:
        """Add employee with basic information only (no login, no photo).

        Args:
            first_name: Employee's first name
            last_name: Employee's last name
            middle_name: Employee's middle name (optional)
            employee_id: Custom employee ID (optional, auto-generated if None)
        """
        logger.info(f"Adding employee: {first_name} {middle_name} {last_name}")

        self.enter_first_name(first_name)
        if middle_name:
            self.enter_middle_name(middle_name)
        self.enter_last_name(last_name)

        if employee_id:
            self.enter_employee_id(employee_id)

        self.click_save()

    def add_employee_with_login(self, first_name: str, last_name: str,
                                username: str, password: str,
                                middle_name: str = "", employee_id: str = None,
                                status_enabled: bool = True) -> None:
        """Add employee with login credentials.

        Args:
            first_name: Employee's first name
            last_name: Employee's last name
            username: Username for login
            password: Password for login
            middle_name: Employee's middle name (optional)
            employee_id: Custom employee ID (optional)
            status_enabled: Login status enabled/disabled (default: True, already default in UI)
        """
        logger.info(f"Adding employee with login: {first_name} {last_name}, username: {username}")

        # Fill basic info
        self.enter_first_name(first_name)
        if middle_name:
            self.enter_middle_name(middle_name)
        self.enter_last_name(last_name)

        if employee_id:
            self.enter_employee_id(employee_id)

        # Enable login details
        self.enable_create_login_details()

        # Fill login credentials
        self.enter_username(username)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.set_status_enabled(status_enabled)
        self.click_save()

        self.page.wait_for_load_state('networkidle')

    def add_employee_full(self, first_name: str, last_name: str,
                         username: str, password: str,
                         photo_path: str = None,
                         middle_name: str = "", employee_id: str = None,
                         status_enabled: bool = True) -> None:
        """Add employee with full information including photo and login.

        Args:
            first_name: Employee's first name
            last_name: Employee's last name
            username: Username for login
            password: Password for login
            photo_path: Path to employee photo (optional)
            middle_name: Employee's middle name (optional)
            employee_id: Custom employee ID (optional)
            status_enabled: Login status enabled/disabled (default: True)
        """
        logger.info(f"Adding employee (full): {first_name} {last_name}")

        # Fill basic info
        self.enter_first_name(first_name)
        if middle_name:
            self.enter_middle_name(middle_name)
        self.enter_last_name(last_name)

        if employee_id:
            self.enter_employee_id(employee_id)

        # Upload photo if provided
        if photo_path:
            self.upload_photo(photo_path)

        # Enable login details
        self.enable_create_login_details()

        # Fill login credentials
        self.enter_username(username)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.set_status_enabled(status_enabled)

        self.click_save()

    def navigate_to_add_employee_page(self):
        """Navigate to the Add Employee page."""
        from config import BASE_URL
        full_url = BASE_URL + "pim/addEmployee"
        logger.info(f"Navigating to Add Employee page: {full_url}")
        self.page.goto(full_url)
        self.page.wait_for_load_state('networkidle')

    def logout(self):
        """Perform the logout action."""
        self._click(self.USER_DROPDOWN)
        self._click(self.LOGOUT_LINK)

