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
    ACTIVITY_DROPDOWN = "//div[contains(@class, 'oxd-select-text oxd-select-text--active')]"
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
    ROW_TOTAL = "//tr[contains(@class, 'orangehrm-timesheet-table-body-row')]//td[last()]"
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
    ERROR_MESSAGE_HOURS = "//span[contains(@class, 'oxd-input-field-error-message') and contains(normalize-space(), 'Should Be Less Than 24')]"
    ERROR_MESSAGE_EXCEED_24 = "//span[contains(text(), 'Should not exceed 24')]"

    # Locators - Success/Warning Messages
    SUCCESS_MESSAGE = ".oxd-toast-content--success"
    WARNING_MESSAGE = ".oxd-toast-content--warn"
    ERROR_TOAST = ".oxd-toast-content--error"

    # Locators - Week Selection
    WEEK_SELECTOR = "//input[@placeholder='yyyy-mm-dd']"
    NEXT_WEEK_BUTTON = "//button[@class='oxd-icon-button orangehrm-timeperiod-icon --next']"

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

    def select_activity(self, activity_name: str, row_index: int = 0):
        """Select an activity from dropdown in specific timesheet row.

        Args:
            activity_name: Activity name to select
            row_index: Index of the timesheet row (0-based, default: 0)
        """
        logger.info(f"Selecting activity: {activity_name} at row {row_index}")

        # ✅ SELECTOR MỚI - CHỈ LẤY ACTIVITY DROPDOWN TRONG TIMESHEET ROWS
        activity_dropdown_selector = (
            "//tr[contains(@class, 'orangehrm-timesheet-table-body-row')]"  # Chỉ trong timesheet rows
            "//div[contains(@class, 'oxd-select-text')]"  # Activity dropdown
        )

        # Get all activity dropdowns WITHIN timesheet rows only
        activity_dropdowns = self.page.locator(self.ACTIVITY_DROPDOWN).all()
        logger.info(f"Found {len(activity_dropdowns)} activity dropdowns in timesheet rows")

        # Click the dropdown for the specific row
        if row_index < len(activity_dropdowns):
            logger.info(f"Clicking activity dropdown at index {row_index}")
            activity_dropdowns[row_index].click()
            self.page.wait_for_timeout(500)

            # Select from the listbox that appears
            option_locator = f"//div[@role='listbox']//span[contains(text(), '{activity_name}')]"
            if self._is_element_visible(option_locator, timeout=3):
                self._click(option_locator)
                self.page.wait_for_timeout(500)
                logger.info(f"✓ Successfully selected activity: {activity_name}")
            else:
                logger.warning(f"Activity option '{activity_name}' not found in dropdown")
        else:
            logger.error(f"Row index {row_index} is out of range. Available dropdowns: {len(activity_dropdowns)}")

    def fill_hours(self, day: str, hours: str, row_index: int = 0, check_validation: bool = False):
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
            # self.page.wait_for_timeout(1000)
            logger.info(f"✓ Filled {hours} hours for {day}")
        else:
            logger.error(f"Cell index {cell_index} out of range (total: {len(time_inputs)})")

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

    def get_row_total(self, row_index: int = 0) -> str:
        """Get row total hours.

        Args:
            row_index: Index of the row (0-based)

        Returns:
            str: Row total hours
        """
        # wait for totals to be visible
        self.page.wait_for_timeout(3000)
        row_totals = self.page.locator(self.ROW_TOTAL).all()
        logger.debug(f"Row totals: {row_totals}")
        if row_index < len(row_totals):
            total = row_totals[row_index].text_content().strip()
            logger.debug(f"Row total: {total}")
            return total
        return "0"

    def is_hours_error_visible(self) -> bool:
        """Check if 'Should Be Less Than 24 and in HH:MM or Decimal Format' error is visible.

        Returns:
            bool: True if positive number error is visible
        """
        return self._is_element_visible(self.ERROR_MESSAGE_HOURS, timeout=5)

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

    def is_save_successful(self):

        return self.page.locator(self.SUCCESS_MESSAGE).is_visible(timeout=3000)

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
        """View timesheet for a specific employee."""
        logger.info(f"Viewing timesheet")
        # Click View button
        self._click(self.VIEW_BUTTON)
        self.page.wait_for_load_state('networkidle')

    def go_to_next_week(self):
        """Navigate to the next week in the timesheet view."""
        logger.info("Navigating to next week")
        self._click(self.NEXT_WEEK_BUTTON)
        self.page.wait_for_timeout(2000)

    def is_create_timesheet_button_disabled(self):
        """Check if Create Timesheet button is disabled.

        Returns:
            bool: True if Create Timesheet button is disabled
        """
        button = self.page.locator(self.CREATE_TIMESHEET_BUTTON)
        disabled = button.get_attribute("disabled")
        return disabled is not None

    def is_edit_button_visible(self):
        """Check if Edit button is visible."""
        return self._is_element_visible(self.EDIT_BUTTON, timeout=3)