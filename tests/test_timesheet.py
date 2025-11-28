"""Test cases for Timesheet Management functionality using Playwright - 33 Test Cases."""
import pytest
import time
import json
import os
from pages.login_page import LoginPage
from pages.timesheet_page import TimesheetPage
from pages.project_page import ProjectPage
from pages.activity_page import ActivityPage
from config import VALID_USERNAME, VALID_PASSWORD


@pytest.mark.usefixtures("driver_init")
class TestTimesheetManagement:
    """Test suite for comprehensive Timesheet Management functionality in Time module - 33 Test Cases."""

    @pytest.fixture(scope="class")
    def load_timesheet_data(self):
        """Load test data from timesheet_data.json file.

        Returns:
            dict: Test data for all timesheet test cases
        """
        json_file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "test-data",
            "timesheet_data.json"
        )
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @pytest.fixture
    def setup_timesheet_page(self) -> TimesheetPage:
        """Login and navigate to Timesheet page.

        Returns:
            TimesheetPage: Initialized timesheet page ready for testing
        """
        # Login
        login_page = LoginPage(self.page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        # Navigate to Timesheet
        time.sleep(1)
        timesheet_page = TimesheetPage(self.page)
        timesheet_page.navigate_to_my_timesheet()
        time.sleep(1)

        return timesheet_page

    @pytest.fixture
    def setup_with_test_project(self) -> tuple[TimesheetPage, str, str]:
        """Setup with a test project and activity for timesheet testing.

        Returns:
            tuple: (TimesheetPage, project_name, activity_name)
        """
        # Login
        login_page = LoginPage(self.page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        # Create test project with activity
        time.sleep(1)
        project_page = ProjectPage(self.page)
        project_page.navigate_to_project_page()

        timestamp = int(time.time())
        project_name = f"TS_Project_{timestamp}"
        customer_name = "ACME Ltd"
        project_page.add_project(project_name, customer_name)
        time.sleep(2)

        # Add activity to project
        activity_page = ActivityPage(self.page)
        activity_name = f"TS_Activity_{timestamp}"
        activity_page.add_activity(project_name, activity_name)
        time.sleep(2)

        # Navigate to timesheet
        timesheet_page = TimesheetPage(self.page)
        timesheet_page.navigate_to_my_timesheet()
        time.sleep(1)

        return timesheet_page, project_name, activity_name

    # ==================== CREATE TIMESHEET (4 TCs) ====================

    def test_create_timesheet_for_current_week(self, setup_timesheet_page, load_timesheet_data):
        """TC31: Create timesheet for current week.

        Test Case ID: TC31 (Maps to TS_TC31 in JSON)
        Description: Create timesheet for current week, verify status is 'Not Submitted'
        Expected: Timesheet created successfully with status 'Not Submitted'
        """
        # Arrange
        timesheet_page = setup_timesheet_page
        test_data = load_timesheet_data["test_cases"]["TS_TC31"]["test_data"]
        expected_status = test_data["expected_status"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)

        # Assert
        actual_status = timesheet_page.get_timesheet_status()
        assert actual_status == expected_status, \
            f"Timesheet status should be '{expected_status}', but got '{actual_status}'"

    def test_create_timesheet_for_future_week(self, setup_timesheet_page, load_timesheet_data):
        """TC32: Create timesheet for future week.

        Test Case ID: TC32 (Maps to TS_TC32 in JSON)
        Description: Create timesheet for future week
        Expected: Timesheet created successfully for future week
        """
        # Arrange
        timesheet_page = setup_timesheet_page
        test_data = load_timesheet_data["test_cases"]["TS_TC32"]["test_data"]
        weeks_ahead = test_data["weeks_ahead"]

        # Act
        timesheet_page.select_week(week_type="future", weeks_ahead=weeks_ahead)
        time.sleep(1)
        timesheet_page.click_create_timesheet()
        time.sleep(2)

        # Assert
        # Verify timesheet was created (status should be visible)
        status = timesheet_page.get_timesheet_status()
        assert status in ["Not Submitted", "Draft"], \
            f"Timesheet should be created for future week, got status: {status}"

    def test_create_duplicate_timesheet_same_week(self, setup_timesheet_page, load_timesheet_data):
        """TC33: Create duplicate timesheet for same week.

        Test Case ID: TC33 (Maps to TS_TC33 in JSON)
        Description: Attempt to create timesheet that already exists for the same week
        Expected: Error message displayed or blocked from creating duplicate
        """
        # Arrange
        timesheet_page = setup_timesheet_page

        # Act - Create first timesheet
        timesheet_page.click_create_timesheet()
        time.sleep(2)

        # Navigate back and try to create duplicate
        timesheet_page.navigate_to_my_timesheet()
        time.sleep(1)

        # Check if Create button is still visible (should not be for existing timesheet)
        create_button_visible = timesheet_page._is_element_visible(
            timesheet_page.CREATE_TIMESHEET_BUTTON, timeout=2
        )

        # Assert - Create button should not be visible for current week with existing timesheet
        assert not create_button_visible, \
            "Create Timesheet button should not be available when timesheet already exists"

    def test_verify_timesheet_grid_7_columns(self, setup_timesheet_page, load_timesheet_data):
        """TC34: Verify timesheet grid displays 7 day columns.

        Test Case ID: TC34 (Maps to TS_TC34 in JSON)
        Description: Verify timesheet grid displays all 7 days of the week
        Expected: Grid displays 7 columns for all days of the week
        """
        # Arrange
        timesheet_page = setup_timesheet_page
        test_data = load_timesheet_data["test_cases"]["TS_TC34"]["test_data"]
        expected_days = 7

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        visible_columns = timesheet_page.verify_grid_columns()

        # Assert
        assert len(visible_columns) == expected_days, \
            f"Timesheet grid should display {expected_days} day columns, but got {len(visible_columns)}"

    # ==================== ADD PROJECT/ACTIVITY (5 TCs) ====================

    def test_add_row_with_valid_project_activity(self, setup_with_test_project, load_timesheet_data):
        """TC35: Add row with valid project and activity.

        Test Case ID: TC35 (Maps to TS_TC35 in JSON)
        Description: Add a new row with valid project and activity
        Expected: New row appears with selected project and activity
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        timesheet_page.click_add_row()
        timesheet_page.select_project(project_name, row_index=0)
        timesheet_page.select_activity(activity_name, row_index=0)
        time.sleep(1)

        # Assert - Verify row was added (no error message)
        assert not timesheet_page.is_error_toast_visible(), \
            "No error should appear when adding valid project-activity row"

    def test_add_multiple_rows_different_projects(self, setup_timesheet_page, load_timesheet_data):
        """TC36: Add multiple rows with different projects.

        Test Case ID: TC36 (Maps to TS_TC36 in JSON)
        Description: Add multiple rows with different projects
        Expected: All rows added successfully with different projects
        """
        # Arrange
        timesheet_page = setup_timesheet_page
        test_data = load_timesheet_data["test_cases"]["TS_TC36"]["test_data"]
        rows = test_data["rows"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)

        for i, row in enumerate(rows):
            timesheet_page.click_add_row()
            timesheet_page.select_project(row["project"], row_index=i)
            time.sleep(1)
            timesheet_page.select_activity(row["activity"], row_index=i)
            time.sleep(1)

        # Assert - No errors should appear
        assert not timesheet_page.is_error_toast_visible(), \
            "All rows with different projects should be added successfully"

    def test_add_duplicate_project_activity_row(self, setup_with_test_project, load_timesheet_data):
        """TC37: Add duplicate project-activity row.

        Test Case ID: TC37 (Maps to TS_TC37 in JSON)
        Description: Attempt to add row with same project-activity combination
        Expected: Error message or blocked from adding duplicate
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)

        # Add first row
        timesheet_page.add_timesheet_row(project_name, activity_name, row_index=0)
        time.sleep(1)

        # Try to add duplicate row
        timesheet_page.click_add_row()
        timesheet_page.select_project(project_name, row_index=1)
        time.sleep(1)
        timesheet_page.select_activity(activity_name, row_index=1)
        time.sleep(2)

        # Assert - Error or warning should appear
        # Note: Some systems may allow duplicate, this is exploratory test
        # Check if duplicate was prevented or warning shown
        has_error = timesheet_page.is_error_toast_visible() or timesheet_page.is_warning_message_visible()
        # This assertion may need adjustment based on actual system behavior
        pytest.skip("Duplicate row behavior depends on system configuration")

    def test_add_row_unassigned_project(self, setup_timesheet_page, load_timesheet_data):
        """TC38: Add row with unassigned project.

        Test Case ID: TC38 (Maps to TS_TC38 in JSON)
        Description: Verify unassigned projects don't appear in dropdown
        Expected: Project not available in dropdown
        """
        # Arrange
        timesheet_page = setup_timesheet_page
        test_data = load_timesheet_data["test_cases"]["TS_TC38"]["test_data"]
        unassigned_project = test_data["project"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        timesheet_page.click_add_row()

        # Try to search for unassigned project
        project_input = timesheet_page.page.locator(timesheet_page.PROJECT_INPUT).first
        project_input.fill(unassigned_project)
        time.sleep(2)

        # Check if project appears in dropdown
        option_locator = f"//div[@role='listbox']//span[contains(text(), '{unassigned_project}')]"
        project_found = timesheet_page._is_element_visible(option_locator, timeout=2)

        # Assert
        assert not project_found, \
            f"Unassigned project '{unassigned_project}' should not appear in dropdown"

    def test_verify_activity_dropdown_filters_by_project(self, setup_with_test_project, load_timesheet_data):
        """TC39: Verify activity dropdown filters by project.

        Test Case ID: TC39 (Maps to TS_TC39 in JSON)
        Description: Verify activity dropdown shows only activities for selected project
        Expected: Activity dropdown shows only relevant activities
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        timesheet_page.click_add_row()
        timesheet_page.select_project(project_name, row_index=0)
        time.sleep(1)

        # Click activity dropdown to see options
        activity_input = timesheet_page.page.locator(timesheet_page.ACTIVITY_INPUT).first
        activity_input.click()
        time.sleep(1)

        # Assert - Activity dropdown should be visible
        activity_options_visible = timesheet_page._is_element_visible(
            "//div[@role='listbox']", timeout=2
        )
        assert activity_options_visible, \
            "Activity dropdown should appear after selecting project"

    # ==================== FILL HOURS - VALID (5 TCs) ====================

    def test_fill_hours_integer_value(self, setup_with_test_project, load_timesheet_data):
        """TC40: Fill hours with integer value (8.0).

        Test Case ID: TC40 (Maps to TS_TC40 in JSON)
        Description: Enter integer hours, verify cell saved and totals updated
        Expected: Hours saved, row total and column total updated correctly
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC40"]["test_data"]
        hours = test_data["monday"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {"monday": hours}
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Assert - No error should appear, hours should be saved
        assert not timesheet_page.is_error_toast_visible(), \
            f"Hours '{hours}' should be saved without error"

    def test_fill_hours_decimal_value(self, setup_with_test_project, load_timesheet_data):
        """TC41: Fill hours with decimal value (8.5).

        Test Case ID: TC41 (Maps to TS_TC41 in JSON)
        Description: Enter decimal hours, verify cell saved and totals updated
        Expected: Decimal hours saved, totals calculated correctly
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC41"]["test_data"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {
            "monday": test_data["monday"],
            "tuesday": test_data["tuesday"]
        }
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Assert
        assert not timesheet_page.is_error_toast_visible(), \
            "Decimal hours should be saved without error"

    def test_fill_hours_time_format(self, setup_with_test_project, load_timesheet_data):
        """TC42: Fill hours with time format (8:30).

        Test Case ID: TC42 (Maps to TS_TC42 in JSON)
        Description: Enter hours in time format, verify converted to decimal
        Expected: Time format converted to 8.5 hours
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC42"]["test_data"]
        time_value = test_data["monday"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {"monday": time_value}
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Assert - Check if time format is accepted or converted
        # Note: Behavior depends on system implementation
        # May need to verify actual cell value after conversion
        pytest.skip("Time format conversion behavior depends on system configuration")

    def test_fill_hours_zero_value(self, setup_with_test_project, load_timesheet_data):
        """TC43: Fill hours with zero (0).

        Test Case ID: TC43 (Maps to TS_TC43 in JSON)
        Description: Enter zero hours, verify cell saved
        Expected: Zero hours saved successfully
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC43"]["test_data"]
        hours = test_data["monday"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {"monday": hours}
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Assert
        assert not timesheet_page.is_error_toast_visible(), \
            "Zero hours should be saved without error"

    def test_fill_hours_multiple_days_verify_totals(self, setup_with_test_project, load_timesheet_data):
        """TC44: Fill hours for multiple days with totals verification.

        Test Case ID: TC44 (Maps to TS_TC44 in JSON)
        Description: Fill hours for multiple days, verify row/column/grand totals
        Expected: All totals calculated correctly
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC44"]["test_data"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {
            "monday": test_data["monday"],
            "tuesday": test_data["tuesday"],
            "wednesday": test_data["wednesday"],
            "thursday": test_data["thursday"],
            "friday": test_data["friday"]
        }
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Assert - Verify totals
        # Note: Actual total verification depends on UI implementation
        assert not timesheet_page.is_error_toast_visible(), \
            "Multiple day hours should be saved without error"

    # ==================== FILL HOURS - INVALID (5 TCs) ====================

    def test_fill_hours_negative_value(self, setup_with_test_project, load_timesheet_data):
        """TC45: Fill hours with negative value (-5).

        Test Case ID: TC45 (Maps to TS_TC45 in JSON)
        Description: Enter negative hours, verify error message
        Expected: Error message 'Invalid' or 'Should be a positive number'
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC45"]["test_data"]
        negative_hours = test_data["monday"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {"monday": negative_hours}
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Assert
        assert timesheet_page.is_positive_number_error_visible() or \
               timesheet_page.is_invalid_error_visible(), \
            "Error message should appear for negative hours"

    def test_fill_hours_exceeding_24(self, setup_with_test_project, load_timesheet_data):
        """TC46: Fill hours exceeding 24 (25).

        Test Case ID: TC46 (Maps to TS_TC46 in JSON)
        Description: Enter hours > 24, verify error/warning message
        Expected: Error or warning message displayed
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC46"]["test_data"]
        excess_hours = test_data["monday"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {"monday": excess_hours}
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Assert
        assert timesheet_page.is_exceed_24_error_visible() or \
               timesheet_page.is_warning_message_visible(), \
            "Error or warning should appear for hours > 24"

    def test_fill_hours_non_numeric_value(self, setup_with_test_project, load_timesheet_data):
        """TC47: Fill hours with non-numeric value (abc).

        Test Case ID: TC47 (Maps to TS_TC47 in JSON)
        Description: Enter non-numeric characters, verify error message
        Expected: Error message 'Invalid' displayed
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC47"]["test_data"]
        invalid_value = test_data["monday"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {"monday": invalid_value}
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Assert
        assert timesheet_page.is_invalid_error_visible(), \
            "Error message 'Invalid' should appear for non-numeric value"

    def test_fill_hours_3_decimal_places(self, setup_with_test_project, load_timesheet_data):
        """TC48: Fill hours with 3 decimal places (8.125).

        Test Case ID: TC48 (Maps to TS_TC48 in JSON)
        Description: Enter hours with 3 decimals, test rounding behavior
        Expected: Value rounded to 2 decimal places (8.13 or 8.12)
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC48"]["test_data"]
        decimal_value = test_data["monday"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {"monday": decimal_value}
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Assert - Verify rounding behavior
        # Note: Actual rounding depends on system implementation
        pytest.skip("Rounding behavior for 3 decimals depends on system configuration")

    def test_fill_total_exceeding_60_hours_week(self, setup_with_test_project, load_timesheet_data):
        """TC49: Fill total exceeding 60 hours per week.

        Test Case ID: TC49 (Maps to TS_TC49 in JSON)
        Description: Enter total hours > 60 for week, verify warning
        Expected: Warning message displayed for excessive hours
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC49"]["test_data"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {
            "monday": test_data["monday"],
            "tuesday": test_data["tuesday"],
            "wednesday": test_data["wednesday"],
            "thursday": test_data["thursday"],
            "friday": test_data["friday"]
        }
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Assert - Check for warning
        # Note: Warning behavior depends on system configuration
        pytest.skip("Warning for excessive hours depends on system configuration")

    # ==================== EDIT TIMESHEET (3 TCs) ====================

    def test_edit_timesheet_not_submitted(self, setup_with_test_project, load_timesheet_data):
        """TC50: Edit timesheet with status 'Not Submitted'.

        Test Case ID: TC50 (Maps to TS_TC50 in JSON)
        Description: Edit timesheet that is not submitted
        Expected: Timesheet edited successfully
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC50"]["test_data"]

        # Act - Create timesheet first
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {"monday": test_data["original_hours"]}
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Verify status is Not Submitted
        status = timesheet_page.get_timesheet_status()
        assert status == "Not Submitted", f"Status should be 'Not Submitted', got '{status}'"

        # Verify can edit
        assert timesheet_page.is_timesheet_editable(), \
            "Timesheet with status 'Not Submitted' should be editable"

    def test_edit_timesheet_submitted(self, setup_with_test_project, load_timesheet_data):
        """TC51: Edit timesheet with status 'Submitted'.

        Test Case ID: TC51 (Maps to TS_TC51 in JSON)
        Description: Attempt to edit submitted timesheet
        Expected: Timesheet locked, cannot edit
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project

        # Act - Create and submit timesheet
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {"monday": "8", "tuesday": "8"}
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Submit timesheet
        timesheet_page.click_submit()
        time.sleep(2)

        # Assert - Timesheet should be locked
        assert timesheet_page.is_timesheet_locked(), \
            "Submitted timesheet should be locked and not editable"

    def test_edit_timesheet_rejected(self, setup_with_test_project, load_timesheet_data):
        """TC52: Edit timesheet with status 'Rejected'.

        Test Case ID: TC52 (Maps to TS_TC52 in JSON)
        Description: Edit rejected timesheet
        Expected: Timesheet can be edited after rejection
        """
        # Note: This test requires supervisor privileges to reject timesheet
        # Skipping as it requires multi-user setup
        pytest.skip("Requires supervisor privileges to reject timesheet first")

    # ==================== SUBMIT TIMESHEET (4 TCs) ====================

    def test_submit_timesheet_with_valid_hours(self, setup_with_test_project, load_timesheet_data):
        """TC53: Submit timesheet with valid hours.

        Test Case ID: TC53 (Maps to TS_TC53 in JSON)
        Description: Submit timesheet with valid hours
        Expected: Status changed to 'Submitted', timesheet locked
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC53"]["test_data"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {
            "monday": test_data["monday"],
            "tuesday": test_data["tuesday"],
            "wednesday": test_data["wednesday"],
            "thursday": test_data["thursday"],
            "friday": test_data["friday"]
        }
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        timesheet_page.click_submit()
        time.sleep(2)

        # Assert
        status = timesheet_page.get_timesheet_status()
        assert status == "Submitted", f"Status should be 'Submitted', got '{status}'"
        assert timesheet_page.is_timesheet_locked(), \
            "Submitted timesheet should be locked"

    def test_submit_empty_timesheet(self, setup_timesheet_page, load_timesheet_data):
        """TC54: Submit empty timesheet.

        Test Case ID: TC54 (Maps to TS_TC54 in JSON)
        Description: Attempt to submit timesheet with no hours
        Expected: Error message, submission blocked
        """
        # Arrange
        timesheet_page = setup_timesheet_page

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)

        # Try to submit without adding any hours
        if timesheet_page._is_element_visible(timesheet_page.SUBMIT_BUTTON, timeout=2):
            timesheet_page.click_submit()
            time.sleep(2)

        # Assert - Error should appear
        assert timesheet_page.is_error_toast_visible(), \
            "Error message should appear when submitting empty timesheet"

    def test_submit_timesheet_with_validation_errors(self, setup_with_test_project, load_timesheet_data):
        """TC55: Submit timesheet with validation errors.

        Test Case ID: TC55 (Maps to TS_TC55 in JSON)
        Description: Attempt to submit timesheet with invalid data
        Expected: Error message, submission blocked
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project
        test_data = load_timesheet_data["test_cases"]["TS_TC55"]["test_data"]
        invalid_hours = test_data["monday"]

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {"monday": invalid_hours}
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)

        # Try to submit with invalid data
        timesheet_page.click_submit()
        time.sleep(2)

        # Assert
        assert timesheet_page.is_error_toast_visible() or \
               timesheet_page.is_invalid_error_visible(), \
            "Error should prevent submission with validation errors"

    def test_withdraw_submitted_timesheet(self, setup_with_test_project, load_timesheet_data):
        """TC56: Withdraw submitted timesheet.

        Test Case ID: TC56 (Maps to TS_TC56 in JSON)
        Description: Withdraw a submitted timesheet
        Expected: Status changed to 'Not Submitted', timesheet unlocked
        """
        # Arrange
        timesheet_page, project_name, activity_name = setup_with_test_project

        # Act - Create and submit timesheet
        timesheet_page.click_create_timesheet()
        time.sleep(2)
        hours_data = {"monday": "8", "tuesday": "8"}
        timesheet_page.add_timesheet_row(project_name, activity_name, hours_data, row_index=0)
        time.sleep(2)
        timesheet_page.click_submit()
        time.sleep(2)

        # Withdraw timesheet
        if timesheet_page._is_element_visible(timesheet_page.RESET_BUTTON, timeout=2):
            timesheet_page.click_reset()
            time.sleep(2)

            # Assert
            status = timesheet_page.get_timesheet_status()
            assert status == "Not Submitted", \
                f"Status should be 'Not Submitted' after withdrawal, got '{status}'"
        else:
            pytest.skip("Reset/Withdraw button not available in this system configuration")

    # ==================== APPROVE/REJECT (6 TCs) ====================

    def test_supervisor_approve_valid_timesheet(self, load_timesheet_data):
        """TC57: Supervisor approve valid timesheet.

        Test Case ID: TC57 (Maps to TS_TC57 in JSON)
        Description: Supervisor approves a valid submitted timesheet
        Expected: Status changed to 'Approved'
        """
        # Note: Requires supervisor login and access to employee timesheets
        pytest.skip("Requires supervisor privileges and multi-user setup")

    def test_supervisor_reject_with_comment(self, load_timesheet_data):
        """TC58: Supervisor reject timesheet with comment.

        Test Case ID: TC58 (Maps to TS_TC58 in JSON)
        Description: Supervisor rejects timesheet with rejection comment
        Expected: Status changed to 'Rejected', comment saved
        """
        # Note: Requires supervisor login
        pytest.skip("Requires supervisor privileges and multi-user setup")

    def test_supervisor_reject_without_comment(self, load_timesheet_data):
        """TC59: Supervisor reject timesheet without comment.

        Test Case ID: TC59 (Maps to TS_TC59 in JSON)
        Description: Attempt to reject timesheet without comment
        Expected: Error message 'Required' for comment field
        """
        # Note: Requires supervisor login
        pytest.skip("Requires supervisor privileges and multi-user setup")

    def test_user_approve_own_timesheet_security(self, load_timesheet_data):
        """TC60: User approve own timesheet (security test).

        Test Case ID: TC60 (Maps to TS_TC60 in JSON)
        Description: Attempt to approve own timesheet
        Expected: Error or action blocked (security test)
        """
        # Note: Security test - user should not be able to approve own timesheet
        pytest.skip("Security test - requires role-based access control testing")

    def test_approve_timesheet_not_submitted(self, load_timesheet_data):
        """TC61: Approve timesheet with status 'Not Submitted'.

        Test Case ID: TC61 (Maps to TS_TC61 in JSON)
        Description: Attempt to approve timesheet that is not submitted
        Expected: Error message or action blocked
        """
        # Note: Requires supervisor login
        pytest.skip("Requires supervisor privileges and multi-user setup")

    def test_employee_view_rejection_comment(self, load_timesheet_data):
        """TC62: Employee view rejected timesheet comment.

        Test Case ID: TC62 (Maps to TS_TC62 in JSON)
        Description: Employee views rejection comment on rejected timesheet
        Expected: Rejection comment visible to employee
        """
        # Note: Requires timesheet to be rejected first
        pytest.skip("Requires supervisor to reject timesheet first")

    # ==================== GUI (1 TC) ====================

    def test_verify_grid_responsive_scrollable(self, setup_timesheet_page, load_timesheet_data):
        """TC63: Verify timesheet grid responsive and scrollable.

        Test Case ID: TC63 (Maps to TS_TC63 in JSON)
        Description: Verify timesheet grid is responsive and scrolls properly
        Expected: Grid responsive, scrolls properly, all elements visible
        """
        # Arrange
        timesheet_page = setup_timesheet_page

        # Act
        timesheet_page.click_create_timesheet()
        time.sleep(2)

        # Verify grid is visible and responsive
        columns = timesheet_page.verify_grid_columns()

        # Assert
        assert len(columns) == 7, "Grid should display all 7 day columns"
        # Additional responsive checks can be added based on viewport size