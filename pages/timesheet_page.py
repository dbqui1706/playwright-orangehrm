"""Page Object Model for Timesheet management in OrangeHRM."""
import logging
from datetime import datetime, timedelta
from playwright.sync_api import Page

from config import BASE_URL
from pages.base import BasePage

logger = logging.getLogger(__name__)


class TimesheetPage(BasePage):
    """Page object for managing Timesheets in Time module."""

    # URL
    MY_TIMESHEET_URL = "time/viewMyTimesheet"
    EMPLOYEE_TIMESHEET_URL = "time/viewEmployeeTimesheet"

    # Locators - Navigation
    CREATE_TIMESHEET_BUTTON = "button:has-text('Create Timesheet')"
    EDIT_BUTTON = "button:has-text('Edit')"
    SAVE_BUTTON = "button:has-text('Save')"
    SUBMIT_BUTTON = "button:has-text('Submit')"
    APPROVE_BUTTON = "button:has-text(' Approve ')"
    REJECT_BUTTON = "button:has-text('Reject')"
    RESET_BUTTON = "button:has-text('Reset')"

    # Locators - Timesheet Form
    ADD_ROW_BUTTON = "//button[contains(@class, 'oxd-icon-button') and .//i[contains(@class, 'oxd-icon bi-plus')]]"
    PROJECT_INPUT = "//label[text()='Project']/parent::div/following-sibling::div//input"

    # Activity dropdown - more specific locator
    # Activity is in a select dropdown, not an input field
    ACTIVITY_DROPDOWN = "//div[contains(@class, 'oxd-select-text-input')]"
    ACTIVITY_DROPDOWN_TRIGGER = "//div[contains(@class, 'oxd-select-text')]"

    # Timesheet rows
    TIMESHEET_ROWS = "//div[contains(@class, 'orangehrm-timesheet-table-body-row')]"

    # Locators - Within a row (relative locators)
    PROJECT_INPUT_IN_ROW = ".//input[@placeholder='Type for hints...']"
    ACTIVITY_DROPDOWN_IN_ROW = ".//div[contains(@class, 'oxd-select-text')]"
    TIME_CELLS_IN_ROW = ".//input[@placeholder='0.00']"

    # Locators - Time Entry Cells (dynamic based on day)
    TIME_CELL_TEMPLATE = "//input[@placeholder='0.00']"

    # Locators - Totals
    ROW_TOTAL = "//div[contains(@class, 'timesheet-row-total')]"
    COLUMN_TOTAL = "//div[contains(@class, 'timesheet-column-total')]"
    GRAND_TOTAL = "//div[contains(@class, 'timesheet-grand-total')]"

    # Locators - Status
    TIMESHEET_STATUS = "//div[contains(@class, 'timesheet-status')]"
    STATUS_NOT_SUBMITTED = "//p[contains(normalize-space(), 'Status: Not Submitted')]"
    STATUS_SUBMITTED = "//p[contains(normalize-space(), 'Status: Submitted')]"
    STATUS_APPROVED = "//p[contains(normalize-space(), 'Status: Approved')]"
    STATUS_REJECTED = "//p[contains(normalize-space(), 'Status: Rejected')]"

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

    # Locator - Employee Name
    EMPLOYEE_NAME_LOCATOR = "//p[contains(@class, 'oxd-userdropdown-name')]"

    # Locator - Employee Timesheet Search
    EMPLOYEE_SEARCH_INPUT = "//input[@placeholder='Type for hints...']"
    VIEW_BUTTON = "//button[contains(@class, 'oxd-button oxd-button--medium oxd-button--secondary orangehrm-left-space')]"


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
        full_url = BASE_URL + self.MY_TIMESHEET_URL
        self.page.goto(full_url)
        self.page.wait_for_load_state('networkidle')

    def navigate_to_employee_timesheet(self):
        """Navigate to Employee Timesheet page (for supervisor)."""
        logger.info("Navigating to Employee Timesheet page")
        full_url = BASE_URL + self.EMPLOYEE_TIMESHEET_URL
        self.page.goto(full_url)
        self.page.wait_for_load_state('networkidle')

    def is_create_timesheet_button_visible(self) -> bool:
        """Check if Create Timesheet button is visible.

        Returns:
            bool: True if Create Timesheet button is visible
        """
        return self._is_element_visible(self.CREATE_TIMESHEET_BUTTON, timeout=3)

    def click_create_timesheet(self):
        """Click the Create Timesheet button."""
        logger.info("Clicking Create Timesheet button")
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
        # xpath = "//*[@id='app']/div[2]/div[2]/div[2]/div/form/div[2]/table/tbody/tr[1]/td[1]/div/div[2]/div/div/input"
        # logger.info("Inputs project: {projects}", projects= self.page.locator(xpath).all())
        project_inputs = self.page.locator(self.PROJECT_INPUT).all()
        if row_index < len(project_inputs):
            input_element = project_inputs[row_index]
            # Clear và fill
            input_element.clear()
            input_element.fill(project_name)

            # Đợi dropdown load
            self.page.wait_for_timeout(1500)

            # Sử dụng keyboard: Arrow Down để chọn option đầu tiên, rồi Enter
            input_element.press("ArrowDown")
            self.page.wait_for_timeout(300)
            input_element.press("Enter")

            logger.info(f"Successfully selected project: {project_name}")
            self.page.wait_for_timeout(500)

    def select_activity(self, activity_name: str, row_index: int = -1):
        """Select an activity from dropdown.

        Args:
            activity_name: Activity name to select
            row_index: Index of the row (0-based)
        """
        logger.info(f"Selecting activity: {activity_name} at row {row_index}")

        # Get all activity dropdown triggers on the page
        activity_dropdowns = self.page.locator(self.ACTIVITY_DROPDOWN_TRIGGER).all()
        logger.info(f"Found {len(activity_dropdowns)} activity dropdowns")

        # Click the dropdown for the specific row
        if row_index < len(activity_dropdowns):
            activity_dropdowns[row_index].click()
            self.page.wait_for_timeout(500)

            # Select from the listbox that appears
            option_locator = f"//div[@role='listbox']//span[contains(text(), '{activity_name}')]"
            if self._is_element_visible(option_locator, timeout=3):
                self._click(option_locator)
                self.page.wait_for_timeout(500)
        else:
            logger.warning(f"Row index {row_index} is out of range. Available dropdowns: {len(activity_dropdowns)}")

    def fill_hours(self, day: str, hours: str, row_index: int = 0):
        """Fill hours for a specific day.

        Args:
            day: Day of week (monday, tuesday, etc.)
            hours: Hours to fill
            row_index: Index of the row (0-based)
        """
        logger.info(f"Filling {hours} hours for {day} at row {row_index}")

        # Locator mới - lấy tất cả input trong duration cells
        time_inputs = self.page.locator("//td[contains(@class, '--duration-input')]//input").all()

        # Calculate cell index based on row and day
        # Each row has 7 cells (Mon-Sun)
        day_index = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }.get(day.lower(), 0)

        cell_index = row_index * 7 + day_index

        logger.info(f"Total time inputs found: {len(time_inputs)}, using index: {cell_index}")

        if cell_index < len(time_inputs):
            time_inputs[cell_index].clear()  # Clear trước
            time_inputs[cell_index].fill(hours)
            time_inputs[cell_index].press('Tab')  # Trigger save
            self.page.wait_for_timeout(500)
            logger.info(f"✓ Filled {hours} hours for {day}")
        else:
            logger.error(f"Cell index {cell_index} out of range (total: {len(time_inputs)})")

    def add_timesheet_row(self, project: str, activity: str, hours_data: dict = None, row_index: int = 0):
        """Add a complete timesheet row with project, activity, and hours.

        This method now works with the last row (newly added row) to avoid issues
        when multiple rows exist.

        Args:
            project: Project name
            activity: Activity name
            hours_data: Dictionary with days and hours (e.g., {'monday': '8', 'tuesday': '7.5'})
            row_index: Deprecated - kept for backward compatibility but not used
        """
        logger.info(f"Adding timesheet row: {project} - {activity}")

        # Step 1: Click Add Row button
        self.click_add_row()

        # Step 2: Get the last (newly added) row
        last_row = self.get_last_timesheet_row()
        if not last_row:
            logger.error("Failed to get last timesheet row after clicking Add Row")
            return

        # Step 3: Select project in the last row
        self.select_project_in_row(last_row, project)

        # Step 4: Select activity in the last row
        self.select_activity_in_row(last_row, activity)

        # Step 5: Fill hours in the last row
        if hours_data:
            self.fill_hours_in_row(last_row, hours_data)

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

    def count_timesheet_rows(self):
        """Count the number of timesheet rows present."""
        logger.info("Counting timesheet rows")
        rows = self.page.locator(self.TIMESHEET_ROWS).all()
        logger.info(f"Total timesheet rows found: {len(rows)}")
        return len(rows)

    def get_last_timesheet_row(self):
        """Get the last (most recently added) timesheet row element.

        Returns:
            Locator: The last row element or None if no rows exist
        """
        rows = self.page.locator(self.TIMESHEET_ROWS).all()
        if rows:
            logger.info(f"Found {len(rows)} rows, returning last row")
            return rows[-1]
        logger.warning("No timesheet rows found")
        return None

    def select_project_in_row(self, row_element, project_name: str):
        """Select a project within a specific row.

        Args:
            row_element: The row locator element
            project_name: Project name to select
        """
        logger.info(f"Selecting project '{project_name}' in specific row")

        # Find project input within this row
        project_input = row_element.locator(self.PROJECT_INPUT_IN_ROW).first
        project_input.fill(project_name[:3])
        self.page.wait_for_timeout(1000)

        # Select from dropdown that appears
        option_locator = f"//div[@role='listbox']//span[contains(text(), '{project_name}')]"
        if self._is_element_visible(option_locator, timeout=3):
            self._click(option_locator)
            self.page.wait_for_timeout(500)
            logger.info(f"Successfully selected project: {project_name}")
        else:
            logger.warning(f"Project option '{project_name}' not found in dropdown")

    def select_activity_in_row(self, row_element, activity_name: str):
        """Select an activity within a specific row.

        Args:
            row_element: The row locator element
            activity_name: Activity name to select
        """
        logger.info(f"Selecting activity '{activity_name}' in specific row")

        # Find and click activity dropdown within this row
        activity_dropdown = row_element.locator(self.ACTIVITY_DROPDOWN_IN_ROW).first
        activity_dropdown.click()
        self.page.wait_for_timeout(500)

        # Select from listbox that appears
        option_locator = f"//div[@role='listbox']//span[contains(text(), '{activity_name}')]"
        if self._is_element_visible(option_locator, timeout=3):
            self._click(option_locator)
            self.page.wait_for_timeout(500)
            logger.info(f"Successfully selected activity: {activity_name}")
        else:
            logger.warning(f"Activity option '{activity_name}' not found in dropdown")

    def fill_hours_in_row(self, row_element, hours_data: dict):
        """Fill hours for multiple days within a specific row.

        Args:
            row_element: The row locator element
            hours_data: Dictionary with days and hours (e.g., {'monday': '8', 'tuesday': '7.5'})
        """
        logger.info(f"Filling hours in specific row: {hours_data}")

        # Get all time cells in this row (should be 7 cells for Mon-Sun)
        time_cells = row_element.locator(self.TIME_CELLS_IN_ROW).all()

        # Map day names to cell indices
        day_to_index = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }

        # Fill hours for each day
        for day, hours in hours_data.items():
            if hours:  # Only fill if hours is not empty
                day_lower = day.lower()
                if day_lower in day_to_index:
                    cell_index = day_to_index[day_lower]
                    if cell_index < len(time_cells):
                        time_cells[cell_index].fill(hours)
                        time_cells[cell_index].press('Tab')
                        logger.info(f"Filled {hours} hours for {day}")
                        self.page.wait_for_timeout(300)
                    else:
                        logger.warning(f"Cell index {cell_index} out of range for day {day}")
                else:
                    logger.warning(f"Invalid day name: {day}")

    def is_row_empty(self, row_index: int = 0) -> bool:
        """Check if row is empty (no project selected).

        Returns:
            bool: True if row is empty
        """
        project_inputs = self.page.locator(self.PROJECT_INPUT).all()

        if row_index >= len(project_inputs):
            logger.warning(f"Row index {row_index} out of range for project inputs")
            return True

        project_value = project_inputs[row_index].input_value()
        logger.info(f"Row index {row_index}: {project_value}")
        return not project_value or project_value.strip() == ""

    def is_save_successful(self):

        return self.page.locator(self.SUCCESS_MESSAGE).is_visible()

    def save_timesheet(self):
        """Click the Save button."""
        logger.info("Clicking Save button")
        self._click(self.SAVE_BUTTON)
        self.page.wait_for_timeout(2000)

    def get_employee_name(self) -> str:
        """Get the employee name displayed on the timesheet page.

        Returns:
            str: Employee name
        """
        return self._get_text(self.EMPLOYEE_NAME_LOCATOR).strip() or ""

    def search_employee_timesheet(self, employee_name):
        """Search for an employee's timesheet.

        Args:
            employee_name: Name of the employee
        """
        logger.info(f"Searching timesheet for employee: {employee_name}")
        # Fill employee name in search input
        input_element = self.page.locator(self.EMPLOYEE_SEARCH_INPUT)
        input_element.clear()
        input_element.fill(employee_name)
        self.page.wait_for_timeout(1500)

        # Sử dụng keyboard: Arrow Down để chọn option đầu tiên, rồi Enter
        input_element.press("ArrowDown")
        self.page.wait_for_timeout(300)
        input_element.press("Enter")
        self.page.wait_for_timeout(500)

    def view_employee_timesheet(self):
        """View timesheet for a specific employee.

        Args:
            employee_name: Name of the employee
        """
        logger.info(f"Viewing timesheet")
        # Click View button
        self._click(self.VIEW_BUTTON)
        self.page.wait_for_load_state('networkidle')