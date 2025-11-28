"""Page Object Model for Timesheet management in OrangeHRM."""
import logging
from datetime import datetime, timedelta
from playwright.sync_api import Page
from pages.base import BasePage

logger = logging.getLogger(__name__)


class TimesheetPage(BasePage):
    """Page object for managing Timesheets in Time module."""

    # URL
    MY_TIMESHEET_URL = "/web/index.php/time/viewMyTimesheet"
    EMPLOYEE_TIMESHEET_URL = "/web/index.php/time/viewEmployeeTimesheet"

    # Locators - Navigation
    CREATE_TIMESHEET_BUTTON = "button:has-text('Create Timesheet')"
    EDIT_BUTTON = "button:has-text('Edit')"
    SUBMIT_BUTTON = "button:has-text('Submit')"
    APPROVE_BUTTON = "button:has-text('Approve')"
    REJECT_BUTTON = "button:has-text('Reject')"
    RESET_BUTTON = "button:has-text('Reset')"

    # Locators - Timesheet Form
    ADD_ROW_BUTTON = "//button[contains(., 'Add Row')]"
    PROJECT_DROPDOWN = "//div[contains(@class, 'oxd-select-text')]"
    PROJECT_INPUT = "//label[text()='Project']/parent::div/following-sibling::div//input"
    ACTIVITY_INPUT = "//label[text()='Activity']/parent::div/following-sibling::div//input"

    # Locators - Time Entry Cells (dynamic based on day)
    TIME_CELL_TEMPLATE = "//input[@placeholder='0.00']"

    # Locators - Totals
    ROW_TOTAL = "//div[contains(@class, 'timesheet-row-total')]"
    COLUMN_TOTAL = "//div[contains(@class, 'timesheet-column-total')]"
    GRAND_TOTAL = "//div[contains(@class, 'timesheet-grand-total')]"

    # Locators - Status
    TIMESHEET_STATUS = "//p[contains(@class, 'timesheet-status')]"
    STATUS_NOT_SUBMITTED = "//p[contains(text(), 'Not Submitted')]"
    STATUS_SUBMITTED = "//p[contains(normalize-space(), 'Status: Submitted')]"
    STATUS_APPROVED = "//p[contains(text(), 'Approved')]"
    STATUS_REJECTED = "//p[contains(text(), 'Rejected')]"

    # Locators - Comments
    COMMENT_TEXTAREA = "//textarea[contains(@class, 'oxd-textarea')]"
    REJECTION_COMMENT = "//div[contains(@class, 'rejection-comment')]"

    # Locators - Validation Messages
    REQUIRED_ERROR_MESSAGE = ".oxd-input-field-error-message"
    ERROR_MESSAGE_REQUIRED = "//span[contains(@class, 'oxd-input-field-error-message') and text()='Required']"
    ERROR_MESSAGE_INVALID = "//span[contains(text(), 'Invalid')]"
    ERROR_MESSAGE_POSITIVE = "//span[contains(text(), 'Should be a positive number')]"
    ERROR_MESSAGE_EXCEED_24 = "//span[contains(text(), 'Should not exceed 24')]"

    # Locators - Success/Warning Messages
    SUCCESS_MESSAGE = ".oxd-toast-content--success"
    WARNING_MESSAGE = ".oxd-toast-content--warn"
    ERROR_TOAST = ".oxd-toast-content--error"

    # Locators - Week Selection
    WEEK_SELECTOR = "//input[@placeholder='yyyy-mm-dd']"
    NEXT_WEEK_BUTTON = "//button[@class='oxd-icon-button']//i[contains(@class, 'chevron-right')]"
    PREV_WEEK_BUTTON = "//button[@class='oxd-icon-button']//i[contains(@class, 'chevron-left')]"

    # Locators - Grid Columns
    MONDAY_COLUMN = "//th[contains(text(), 'Mon')]"
    TUESDAY_COLUMN = "//th[contains(text(), 'Tue')]"
    WEDNESDAY_COLUMN = "//th[contains(text(), 'Wed')]"
    THURSDAY_COLUMN = "//th[contains(text(), 'Thu')]"
    FRIDAY_COLUMN = "//th[contains(text(), 'Fri')]"
    SATURDAY_COLUMN = "//th[contains(text(), 'Sat')]"
    SUNDAY_COLUMN = "//th[contains(text(), 'Sun')]"

    def __init__(self, page: Page):
        """Initialize TimesheetPage.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        logger.info("TimesheetPage initialized")

    def navigate_to_my_timesheet(self):
        """Navigate to My Timesheet page."""
        logger.info("Navigating to My Timesheet page")
        full_url = self.page.url.split('/web')[0] + self.MY_TIMESHEET_URL
        self.page.goto(full_url)
        self.page.wait_for_load_state('networkidle')

    def navigate_to_employee_timesheet(self):
        """Navigate to Employee Timesheet page (for supervisor)."""
        logger.info("Navigating to Employee Timesheet page")
        full_url = self.page.url.split('/web')[0] + self.EMPLOYEE_TIMESHEET_URL
        self.page.goto(full_url)
        self.page.wait_for_load_state('networkidle')

    def click_create_timesheet(self):
        """Click the Create Timesheet button."""
        logger.info("Clicking Create Timesheet button")
        if self._is_element_visible(self.CREATE_TIMESHEET_BUTTON, timeout=3):
            self._click(self.CREATE_TIMESHEET_BUTTON)
            self.page.wait_for_timeout(2000)

    def click_edit(self):
        """Click the Edit button."""
        logger.info("Clicking Edit button")
        self._click(self.EDIT_BUTTON)
        self.page.wait_for_timeout(1000)

    def click_add_row(self):
        """Click the Add Row button to add new timesheet entry."""
        logger.info("Clicking Add Row button")
        self._click(self.ADD_ROW_BUTTON)
        self.page.wait_for_timeout(1000)

    def select_project(self, project_name: str, row_index: int = 0):
        """Select a project from dropdown.

        Args:
            project_name: Project name to select
            row_index: Index of the row (0-based)
        """
        logger.info(f"Selecting project: {project_name} at row {row_index}")
        # Type in project input to trigger autocomplete
        project_inputs = self.page.locator(self.PROJECT_INPUT).all()
        if row_index < len(project_inputs):
            project_inputs[row_index].fill(project_name[:3])
            self.page.wait_for_timeout(1000)
            # Select from dropdown
            option_locator = f"//div[@role='listbox']//span[contains(text(), '{project_name}')]"
            if self._is_element_visible(option_locator, timeout=3):
                self._click(option_locator)
                self.page.wait_for_timeout(500)

    def select_activity(self, activity_name: str, row_index: int = 0):
        """Select an activity from dropdown.

        Args:
            activity_name: Activity name to select
            row_index: Index of the row (0-based)
        """
        logger.info(f"Selecting activity: {activity_name} at row {row_index}")
        activity_inputs = self.page.locator(self.ACTIVITY_INPUT).all()
        if row_index < len(activity_inputs):
            activity_inputs[row_index].fill(activity_name[:3])
            self.page.wait_for_timeout(1000)
            option_locator = f"//div[@role='listbox']//span[contains(text(), '{activity_name}')]"
            if self._is_element_visible(option_locator, timeout=3):
                self._click(option_locator)
                self.page.wait_for_timeout(500)

    def fill_hours(self, day: str, hours: str, row_index: int = 0):
        """Fill hours for a specific day.

        Args:
            day: Day of week (monday, tuesday, etc.)
            hours: Hours to fill
            row_index: Index of the row (0-based)
        """
        logger.info(f"Filling {hours} hours for {day} at row {row_index}")
        # Find time input cells
        time_inputs = self.page.locator(self.TIME_CELL_TEMPLATE).all()

        # Calculate cell index based on row and day
        # Each row has 7 cells (Mon-Sun)
        day_index = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }.get(day.lower(), 0)

        cell_index = row_index * 7 + day_index

        if cell_index < len(time_inputs):
            time_inputs[cell_index].fill(hours)
            # Press Tab to trigger save
            time_inputs[cell_index].press('Tab')
            self.page.wait_for_timeout(500)

    def add_timesheet_row(self, project: str, activity: str, hours_data: dict = None, row_index: int = 0):
        """Add a complete timesheet row with project, activity, and hours.

        Args:
            project: Project name
            activity: Activity name
            hours_data: Dictionary with days and hours (e.g., {'monday': '8', 'tuesday': '7.5'})
            row_index: Index of the row (0-based)
        """
        logger.info(f"Adding timesheet row: {project} - {activity}")
        self.click_add_row()
        self.select_project(project, row_index)
        self.select_activity(activity, row_index)

        if hours_data:
            for day, hours in hours_data.items():
                if hours:  # Only fill if hours is not empty
                    self.fill_hours(day, hours, row_index)

    def click_submit(self):
        """Click the Submit button."""
        logger.info("Clicking Submit button")
        self._click(self.SUBMIT_BUTTON)
        self.page.wait_for_timeout(2000)

    def click_approve(self):
        """Click the Approve button (supervisor action)."""
        logger.info("Clicking Approve button")
        self._click(self.APPROVE_BUTTON)
        self.page.wait_for_timeout(2000)

    def click_reject(self, comment: str = ""):
        """Click the Reject button and enter comment.

        Args:
            comment: Rejection comment
        """
        logger.info(f"Clicking Reject button with comment: {comment}")
        self._click(self.REJECT_BUTTON)
        self.page.wait_for_timeout(1000)
        if comment and self._is_element_visible(self.COMMENT_TEXTAREA, timeout=2):
            self._send_keys(self.COMMENT_TEXTAREA, comment)
        # Confirm rejection
        confirm_button = "//button[contains(@class, 'oxd-button--label-danger')]"
        if self._is_element_visible(confirm_button, timeout=2):
            self._click(confirm_button)
            self.page.wait_for_timeout(2000)

    def click_reset(self):
        """Click the Reset button to withdraw timesheet."""
        logger.info("Clicking Reset button")
        self._click(self.RESET_BUTTON)
        self.page.wait_for_timeout(2000)

    def get_timesheet_status(self) -> str:
        """Get current timesheet status.

        Returns:
            str: Timesheet status
        """
        if self._is_element_visible(self.STATUS_NOT_SUBMITTED, timeout=2):
            return "Not Submitted"
        elif self._is_element_visible(self.STATUS_SUBMITTED, timeout=2):
            return "Submitted"
        elif self._is_element_visible(self.STATUS_APPROVED, timeout=2):
            return "Approved"
        elif self._is_element_visible(self.STATUS_REJECTED, timeout=2):
            return "Rejected"
        return "Unknown"

    def verify_grid_columns(self) -> list:
        """Verify timesheet grid displays all 7 day columns.

        Returns:
            list: List of visible column names
        """
        logger.info("Verifying timesheet grid columns")
        columns = []
        column_locators = [
            self.MONDAY_COLUMN, self.TUESDAY_COLUMN, self.WEDNESDAY_COLUMN,
            self.THURSDAY_COLUMN, self.FRIDAY_COLUMN, self.SATURDAY_COLUMN,
            self.SUNDAY_COLUMN
        ]

        for locator in column_locators:
            if self._is_element_visible(locator, timeout=2):
                text = self._get_text(locator)
                columns.append(text)

        return columns

    def get_row_total(self, row_index: int = 0) -> str:
        """Get row total hours.

        Args:
            row_index: Index of the row (0-based)

        Returns:
            str: Row total hours
        """
        row_totals = self.page.locator(self.ROW_TOTAL).all()
        if row_index < len(row_totals):
            return row_totals[row_index].text_content().strip()
        return "0"

    def get_grand_total(self) -> str:
        """Get grand total hours for the week.

        Returns:
            str: Grand total hours
        """
        if self._is_element_visible(self.GRAND_TOTAL, timeout=2):
            return self._get_text(self.GRAND_TOTAL)
        return "0"

    def is_success_message_visible(self) -> bool:
        """Check if success message is displayed.

        Returns:
            bool: True if success message is visible
        """
        return self._is_element_visible(self.SUCCESS_MESSAGE, timeout=5)

    def is_warning_message_visible(self) -> bool:
        """Check if warning message is displayed.

        Returns:
            bool: True if warning message is visible
        """
        return self._is_element_visible(self.WARNING_MESSAGE, timeout=3)

    def is_error_toast_visible(self) -> bool:
        """Check if error toast message is displayed.

        Returns:
            bool: True if error toast is visible
        """
        return self._is_element_visible(self.ERROR_TOAST, timeout=3)

    def is_required_error_visible(self) -> bool:
        """Check if 'Required' error message is visible.

        Returns:
            bool: True if Required error is visible
        """
        return self._is_element_visible(self.ERROR_MESSAGE_REQUIRED, timeout=3)

    def is_invalid_error_visible(self) -> bool:
        """Check if 'Invalid' error message is visible.

        Returns:
            bool: True if Invalid error is visible
        """
        return self._is_element_visible(self.ERROR_MESSAGE_INVALID, timeout=3)

    def is_positive_number_error_visible(self) -> bool:
        """Check if 'Should be a positive number' error is visible.

        Returns:
            bool: True if positive number error is visible
        """
        return self._is_element_visible(self.ERROR_MESSAGE_POSITIVE, timeout=3)

    def is_exceed_24_error_visible(self) -> bool:
        """Check if 'Should not exceed 24' error is visible.

        Returns:
            bool: True if exceed 24 error is visible
        """
        return self._is_element_visible(self.ERROR_MESSAGE_EXCEED_24, timeout=3)

    def get_rejection_comment(self) -> str:
        """Get rejection comment text.

        Returns:
            str: Rejection comment
        """
        if self._is_element_visible(self.REJECTION_COMMENT, timeout=2):
            return self._get_text(self.REJECTION_COMMENT)
        return ""

    def is_timesheet_editable(self) -> bool:
        """Check if timesheet is editable (Edit button visible).

        Returns:
            bool: True if Edit button is visible
        """
        return self._is_element_visible(self.EDIT_BUTTON, timeout=2)

    def is_timesheet_locked(self) -> bool:
        """Check if timesheet is locked (cannot edit).

        Returns:
            bool: True if timesheet is locked
        """
        return not self.is_timesheet_editable()

    def select_week(self, week_type: str = "current", weeks_ahead: int = 0):
        """Select a specific week.

        Args:
            week_type: Type of week ("current", "future", "past")
            weeks_ahead: Number of weeks ahead (for future weeks)
        """
        logger.info(f"Selecting week: {week_type}, weeks_ahead: {weeks_ahead}")
        if week_type == "future":
            for _ in range(weeks_ahead):
                if self._is_element_visible(self.NEXT_WEEK_BUTTON, timeout=2):
                    self._click(self.NEXT_WEEK_BUTTON)
                    self.page.wait_for_timeout(1000)
        elif week_type == "past":
            for _ in range(abs(weeks_ahead)):
                if self._is_element_visible(self.PREV_WEEK_BUTTON, timeout=2):
                    self._click(self.PREV_WEEK_BUTTON)
                    self.page.wait_for_timeout(1000)