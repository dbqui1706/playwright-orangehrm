"""
End-to-End Timesheet Testing - Employee & Supervisor Flow
==========================================================

This module tests the complete timesheet workflow:
1. E2E-01: Happy Path - Employee creates → Submits → Supervisor approves
2. E2E-02: Rejection Flow - Submit → Reject → Employee edits → Re-submits → Approve

Prerequisites:
--------------
Before running these tests, ensure you have:
1. Two user accounts set up in OrangeHRM:
   - Employee account (ESS User role)
   - Supervisor account (ESS + Supervisor role)
2. Supervisor is assigned as the reporting supervisor for Employee
3. At least one project with activities exists
4. Employee is assigned to the project

Setup Instructions:
------------------
See TIMESHEET_SETUP.md for detailed setup instructions.
"""

import pytest
import time
import json
import os

from pages.add_employee_page import AddEmployeePage
from pages.login_page import LoginPage
from pages.timesheet_page import TimesheetPage
from pages.project_page import ProjectPage
from pages.activity_page import ActivityPage
from config import VALID_USERNAME, VALID_PASSWORD, EMPLOYEE_PASSWORD, EMPLOYEE_USERNAME, BASE_URL


@pytest.mark.usefixtures("driver_init")
class TestTimesheetEndToEnd:
    """End-to-end test suite for Timesheet workflow between Employee and Supervisor."""
    LOGOUT_URL = BASE_URL + "auth/logout"

    # ==================== HELPER METHODS ====================

    def _login(self, username: str, password: str):
        """Helper: Login with credentials."""
        login_page = LoginPage(self.page)
        login_page.login(username, password)
        time.sleep(1)

    def _logout(self):
        """Helper: Logout current user."""
        self.page.goto(self.LOGOUT_URL)
        time.sleep(1)

    def _navigate_to_timesheet(self, is_employee: bool = True):
        """Helper: Navigate to timesheet page.

        Args:
            is_employee: True for My Timesheet, False for Employee Timesheet
        """
        timesheet_page = TimesheetPage(self.page)
        if is_employee:
            timesheet_page.navigate_to_my_timesheet()
        else:
            timesheet_page.navigate_to_employee_timesheet()
        time.sleep(1)
        return timesheet_page

    def _login_and_navigate(self, username: str, password: str, is_employee: bool = True):
        """Helper: Login and navigate to timesheet in one go."""
        self._login(username, password)
        return self._navigate_to_timesheet(is_employee)

    def _prepare_timesheet_row(self, timesheet_page, project_name: str, activity_name: str, row_index: int = 0) -> int:
        """Helper: Prepare a row for data entry (handles existing rows logic).

        Returns:
            int: Row index to use
        """
        print(f"✓ Using row index: {row_index}")

        # Fill project and activity
        timesheet_page.select_project(project_name, row_index=row_index)
        time.sleep(2)
        timesheet_page.select_activity(activity_name, row_index=row_index)
        time.sleep(2)

        return row_index

    def _fill_timesheet_hours(self, timesheet_page, hours_data: dict, row_index: int = 0):
        """Helper: Fill hours for all days."""
        for day, hours in hours_data.items():
            if hours:
                timesheet_page.fill_hours(day, hours, row_index=row_index)
                # time.sleep(0.5)
        print(f"✓ Added hours: {hours_data}")
        time.sleep(2)

    def _create_or_edit_timesheet(self, timesheet_page):
        """Helper: Create new timesheet or edit existing one."""
        if timesheet_page.is_create_timesheet_button_visible():
            timesheet_page.click_create_timesheet()
        else:
            timesheet_page.click_edit()
            time.sleep(2)

    @pytest.fixture(scope="class")
    def load_timesheet_data(self):
        """Load test data from timesheet_data.json file.

        Returns:
            dict: Test data including account info and test cases
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
    def employee_login(self) -> TimesheetPage:
        """Login as Employee and navigate to My Timesheets.

        Returns:
            TimesheetPage: Initialized timesheet page for employee
        """
        # Get employee credentials from test data
        employee_username = EMPLOYEE_USERNAME
        employee_password = EMPLOYEE_PASSWORD

        # Login as Employee
        login_page = LoginPage(self.page)
        login_page.login(employee_username, employee_password)
        time.sleep(1)

        # Navigate to My Timesheets
        timesheet_page = TimesheetPage(self.page)
        timesheet_page.navigate_to_my_timesheet()
        time.sleep(1)

        return timesheet_page

    @pytest.fixture
    def create_mock_employee(self, ):
        """Create a mock employee for testing."""
        login_page = LoginPage(self.page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        time.sleep(1)

        # Navigate to Add Employee Page
        employee_page = AddEmployeePage(self.page)
        employee_page.navigate_to_add_employee_page()

        # Arrange
        timestamp = int(time.time()) % 10000
        username = f"mock-{timestamp}"
        password = "2742003Huong!"
        frist_name = "mock"
        last_name = f"user-{timestamp}"

        # Act
        employee_page.add_employee_with_login(
            first_name=frist_name,
            last_name=last_name,
            username=username,
            password=password,
            status_enabled=True
        )
        # logout admin
        employee_page.logout()
        return username, password, frist_name, last_name

    @pytest.fixture
    def supervisor_login(self, load_timesheet_data):
        """Login as Supervisor and navigate to Employee Timesheets.

        Returns:
            TimesheetPage: Initialized timesheet page for supervisor
        """
        # Get supervisor credentials from test data
        # NOTE: Update these with your actual test supervisor credentials
        supervisor_username = VALID_USERNAME
        supervisor_password = VALID_PASSWORD

        # Logout first if already logged in
        try:
            self.page.goto(self.page.url.split('/web')[0] + "/web/index.php/auth/logout")
            time.sleep(1)
        except:
            pass

        # Login as Supervisor
        login_page = LoginPage(self.page)
        login_page.login(supervisor_username, supervisor_password)
        time.sleep(1)

        # Navigate to Employee Timesheets
        timesheet_page = TimesheetPage(self.page)
        timesheet_page.navigate_to_employee_timesheet()
        time.sleep(1)

        return timesheet_page

    @pytest.fixture
    def setup_test_project(self):
        """Setup a test project with activity for timesheet testing.

        Returns:
            tuple: (project_name, activity_name)
        """
        # Login as Admin to create project
        login_page = LoginPage(self.page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        time.sleep(1)

        # Create test project
        project_page = ProjectPage(self.page)
        project_page.navigate_to_project_page()

        timestamp = int(time.time()) % 10000
        project_name = f"E2E_Project_{timestamp}"
        customer_name = "ACME Ltd"
        project_admin = "Qui Dang"
        description = "E2E Test Project Creation"

        project_page.add_project(project_name, customer_name, project_admin)
        time.sleep(2)

        # Add activity to project
        activity_page = ActivityPage(self.page)
        activity_name = f"E2E_Activity_{timestamp}"
        activity_page.add_activity(project_name, activity_name)
        time.sleep(2)

        # Navigate to Add Employee Page
        employee_page = AddEmployeePage(self.page)
        employee_page.navigate_to_add_employee_page()

        # Arrange
        timestamp = int(time.time()) % 10000
        username = f"mock-{timestamp}"
        password = "2742003Huong!"
        frist_name = "mock"
        last_name = f"user-{timestamp}"

        # Act
        employee_page.add_employee_with_login(
            first_name=frist_name,
            last_name=last_name,
            username=username,
            password=password,
            status_enabled=True
        )

        # Logout admin
        self._logout()

        return project_name, activity_name, project_admin, description, username, password

    # ==================== POSITIVE TESTCASE ====================

    def test_timesheets_01_happy_path_employee_submit_supervisor_approve(
            self,
            load_timesheet_data,
            # setup_test_project,
            create_mock_employee
    ):
        """
        E2E-01: Happy Path - Employee creates timesheet → Submits → Supervisor approves

        Prerequisites:
        - Employee and Supervisor accounts exist
        - In this case Supervisor is Admin user and Employee is a mock user created
        for the test from fixture "create_mock_employee"

        Flow:
        -----
        Step 1: Employee logs in and creates timesheet or edits existing
        Step 2: Employee adds project, activity, and hours
        Step 3: Employee submits timesheet
        Step 4: Supervisor logs in and views submitted timesheet
        Step 5: Supervisor approves timesheet
        Step 6: Search and View for Employee's Timesheet
        Step 7: Employee verifies approved status

        Expected Result:
        ---------------
        - Timesheet status changes: Not Submitted → Submitted → Approved
        - Employee can see approved status
        """
        test_data = load_timesheet_data["test_cases"]["TIMESHEETS_01"]["test_data"]
        # project_name, activity_name, _, _, employee_username, employee_password = setup_test_project
        employee_username, employee_password, _, _ = create_mock_employee
        project_name, activity_name = test_data["project"], test_data["activity"]

        # STEP 1: Employee Login
        timesheet_page = self._login_and_navigate(
            employee_username, employee_password, is_employee=True
        )

        employee_name = timesheet_page.get_employee_name()

        # STEP 2: Create/Edit Timesheet
        self._create_or_edit_timesheet(timesheet_page)

        # STEP 3: Add Hours
        row_index = self._prepare_timesheet_row(timesheet_page, project_name, activity_name)
        self._fill_timesheet_hours(timesheet_page, test_data["hours"], row_index)
        timesheet_page.save_timesheet()

        assert timesheet_page.is_save_successful(), "Timesheet save failed"

        # STEP 4: Submit
        timesheet_page.click_submit()
        time.sleep(2)

        submitted_status = timesheet_page.get_timesheet_status()
        assert submitted_status == test_data["expected_status_after_submit"], \
            f"Status should be 'Submitted', got '{submitted_status}'"

        # STEP 5: Supervisor Approves
        self._logout()
        timesheet_page = self._login_and_navigate(
            VALID_USERNAME, VALID_PASSWORD, is_employee=False
        )

        # STEP 6: Search and View for Employee's Timesheet
        timesheet_page.search_employee_timesheet(employee_name)
        timesheet_page.view_employee_timesheet()

        # Approve
        timesheet_page.click_approve()

        # STEP 7: Verify Approval
        self._logout()
        timesheet_page = self._login_and_navigate(
            employee_username, employee_password, is_employee=True
        )

        final_status = timesheet_page.get_timesheet_status()
        assert final_status == test_data["expected_status_after_approve"] \
            , f"Final status should be 'Approved', got '{final_status}'"

    def test_timesheets_02_rejection_flow_employee_resubmit_supervisor_approve(
            self,
            load_timesheet_data,
            # setup_test_project
            create_mock_employee
    ):
        """
        E2E-02: Rejection Flow - Submit → Reject → Employee edits → Re-submits → Approve

        Flow:
        -----
        Step 1: Employee creates and submits timesheet (with incorrect hours)
        Step 2: Supervisor logs in and rejects with comment
        Step 3: Employee logs in, sees rejection, edits hours
        Step 4: Employee re-submits corrected timesheet
        Step 5: Supervisor approves the corrected timesheet
        Step 6: Employee verifies final approval

        Expected Result:
        ---------------
        - Status flow: Not Submitted → Submitted → Rejected → Not Submitted → Submitted → Approved
        - Employee can see rejection comment
        - Employee can edit and resubmit after rejection
        """
        # Get test data
        test_data = load_timesheet_data["test_cases"]["TIMESHEETS_02"]["test_data"]
        employee_username, employee_password, _, _ = create_mock_employee

        project_name, activity_name = test_data["project"], test_data["activity"]
        # STEP 1: Employee Login and Submit
        timesheet_page = self._login_and_navigate(
            employee_username, employee_password, is_employee=True
        )
        employee_name = timesheet_page.get_employee_name()
        self._create_or_edit_timesheet(timesheet_page)
        row_index = self._prepare_timesheet_row(timesheet_page, project_name, activity_name)
        self._fill_timesheet_hours(timesheet_page, test_data["initial_hours"], row_index)
        timesheet_page.save_timesheet()
        assert timesheet_page.is_save_successful(), "Timesheet save failed"
        timesheet_page.click_submit()
        time.sleep(2)
        submitted_status = timesheet_page.get_timesheet_status()
        assert submitted_status == test_data["expected_status_after_submit"], \
            f"Status should be 'Submitted', got '{submitted_status}'"
        # STEP 2: Supervisor Rejects
        self._logout()
        timesheet_page = self._login_and_navigate(
            VALID_USERNAME, VALID_PASSWORD, is_employee=False
        )
        timesheet_page.search_employee_timesheet(employee_name)
        timesheet_page.view_employee_timesheet()
        timesheet_page.click_reject(test_data["rejection_comment"])

        # STEP 3: Employee Edits after Rejection
        self._logout()
        timesheet_page = self._login_and_navigate(
            employee_username, employee_password, is_employee=True
        )
        rejection_status = timesheet_page.get_timesheet_status()
        assert rejection_status == test_data["expected_status_after_reject"], \
            f"Rejection comment mismatch. Expected: '{test_data['expected_status_after_reject']}', Got: '{rejection_status}'"
        self._create_or_edit_timesheet(timesheet_page)

        # STEP 4: Re-submit Corrected Timesheet
        # row_index = self._prepare_timesheet_row(timesheet_page, project_name, activity_name)
        self._fill_timesheet_hours(timesheet_page, test_data["corrected_hours"], 0)
        timesheet_page.save_timesheet()
        assert timesheet_page.is_save_successful(), "Timesheet save failed"
        timesheet_page.click_submit()
        time.sleep(2)
        resubmitted_status = timesheet_page.get_timesheet_status()
        assert resubmitted_status == test_data["expected_status_after_resubmit"], \
            f"Status should be 'Submitted', got '{resubmitted_status}'"

        # STEP 5: Supervisor Approves Corrected Timesheet
        self._logout()
        timesheet_page = self._login_and_navigate(
            VALID_USERNAME, VALID_PASSWORD, is_employee=False
        )
        timesheet_page.search_employee_timesheet(employee_name)
        timesheet_page.view_employee_timesheet()
        timesheet_page.click_approve()
        # STEP 6: Verify Final Approval
        self._logout()
        timesheet_page = self._login_and_navigate(
            employee_username, employee_password, is_employee=True
        )
        final_status = timesheet_page.get_timesheet_status()
        assert final_status == test_data["expected_final_status"], \
            f"Final status should be 'Approved', got '{final_status}'"

    # [TimeSheet-4]: Kiểm tra tạo timesheet cho nhiều projects trong cùng một tuần
    # "TIMESHEETS_04": {
    #     "test_name": "Employee creates timesheet for multiple projects and activities",
    #     "category": "positive",
    #     "description": "Multiple project-activity combinations in one timesheet",
    #     "test_data": {
    #         "rows": [
    #             {
    #                 "project": "ACME Ltd",
    #                 "activity": "Development",
    #                 "hours": {"monday": "4", "tuesday": "4", "wednesday": "4"}
    #             },
    #             {
    #                 "project": "ASF - Phase 1",
    #                 "activity": "Bug Fixes",
    #                 "hours": {"monday": "4", "tuesday": "4", "wednesday": "4"}
    #             }
    #         ],
    #         "expected_status_after_submit": "Submitted",
    #         "expected_status_after_approve": "Approved"
    #     },
    #     "expected_result": "Multiple projects submitted and approved"
    # },
    def test_timesheets_04_multiple_projects_single_week(self, load_timesheet_data, create_mock_employee):
        """
        Testcase: Create timesheet with multiple projects in a single week
        Flow:
        -----
        Step 1: Employee logs in and creates timesheet
        Step 2: Employee adds multiple project/activity combinations with hours
        Step 3: Employee submits timesheet
        Step 4: Supervisor approves timesheet
        Step 5: Employee verifies approved status
        Expected Result:
        ---------------
        - Timesheet with multiple projects is successfully submitted and approved
        """
        test_data = load_timesheet_data["test_cases"]["TIMESHEETS_04"]["test_data"]
        username, password, _, _ = create_mock_employee

        # STEP 1: Employee Login
        timesheet_page = self._login_and_navigate(
            username, password, is_employee=True
        )
        employee_name = timesheet_page.get_employee_name()


        # STEP 2: Create/Edit Timesheet
        self._create_or_edit_timesheet(timesheet_page)

        # STEP 3: Add Multiple Projects/Activities
        for i, row in enumerate(test_data["rows"]):
            project = row["project"]
            activity = row["activity"]
            hours = row["hours"]
            if i > 0:
                timesheet_page.click_add_row()
            row_index = self._prepare_timesheet_row(timesheet_page, project, activity, row_index=i)
            self._fill_timesheet_hours(timesheet_page, hours, row_index)

        timesheet_page.save_timesheet()
        assert timesheet_page.is_save_successful(), "Timesheet save failed"

        # STEP 4: Submit
        timesheet_page.click_submit()
        time.sleep(2)

        submitted_status = timesheet_page.get_timesheet_status()
        assert submitted_status == test_data["expected_status_after_submit"], \
            f"Status should be 'Submitted', got '{submitted_status}'"
        # STEP 5: Supervisor Approves
        self._logout()
        timesheet_page = self._login_and_navigate(
            VALID_USERNAME, VALID_PASSWORD, is_employee=False
        )
        timesheet_page.search_employee_timesheet(employee_name)
        timesheet_page.view_employee_timesheet()
        timesheet_page.click_approve()

        # STEP 6: Verify Approval
        self._logout()
        timesheet_page = self._login_and_navigate(
            username, password, is_employee=True
        )
        final_status = timesheet_page.get_timesheet_status()
        assert final_status == test_data["expected_status_after_approve"] \
            , f"Final status should be 'Approved', got '{final_status}'"


    # ==================== NEGATIVE TESTCASE ====================
    def test_timesheet_03_submit_timesheet_empty_record(self, load_timesheet_data, create_mock_employee):
        """
        Negative Testcase: Attempt to submit timesheet with empty record

        Flow:
        -----
        Step 1: Employee logs in and creates timesheet
        Step 2: Employee attempts to submit without adding any project/activity/hours

        Expected Result:
        ---------------
        - Submission should be blocked
        - Appropriate error message should be displayed
        """
        test_data = load_timesheet_data["test_cases"]["TIMESHEETS_03"]
        username, password, _, _ = create_mock_employee

        # STEP 1: Employee Login
        timesheet_page = self._login_and_navigate(
            username, password, is_employee=True
        )

        # STEP 2: Attempt to Submit without adding any data
        timesheet_page.click_submit()
        time.sleep(2)

        # Verify error message
        submit_success = timesheet_page.get_timesheet_status()
        if submit_success and submit_success.strip().lower() == "submitted":
            pytest.fail(f"Expected error message '{test_data['expected_result']}', got '{submit_success}'")

    # [TimeSheet-5]: Kiểm tra timesheet với số giờ thập phân (decimal hours)
    # "TIMESHEETS_05": {
    #     "test_name": "Check timesheet with decimal hours input",
    #     "category": "positive",
    #     "description": "Employee enters decimal hours in timesheet",
    #     "test_data": {
    #         "project": "ACME Ltd",
    #         "activity": "Development",
    #         "hours": {
    #             "monday": "7.5",
    #             "tuesday": "8.25",
    #             "wednesday": "6.75",
    #             "thursday": "8.0",
    #             "friday": "7.5"
    #         },
    #         "expected_total_hours": "38.0"
    #     },
    #     "expected_result": "Decimal hours accepted and total calculated correctly"
    # }
    def test_timesheet_05_decimal_hours_entry(self, load_timesheet_data, create_mock_employee):
        """
        Testcase: Employee enters decimal hours in timesheet

        Flow:
        -----
        Step 1: Employee logs in and creates timesheet
        Step 2: Employee adds project/activity and enters decimal hours
        Step 3: Employee saves timesheet
        Step 4: Verify total hours calculation

        Expected Result:
        ---------------
        - Decimal hours should be accepted
        - Total hours should be calculated correctly
        """
        test_data = load_timesheet_data["test_cases"]["TIMESHEETS_05"]
        username, password, _, _ = create_mock_employee

        # STEP 1: Employee Login
        timesheet_page = self._login_and_navigate(
            username, password, is_employee=True
        )

        # STEP 2: Create/Edit Timesheet
        self._create_or_edit_timesheet(timesheet_page)

        # STEP 3: Add Project/Activity and Decimal Hours
        row_index = self._prepare_timesheet_row(timesheet_page, test_data["test_data"]["project"], test_data["test_data"]["activity"])
        self._fill_timesheet_hours(timesheet_page, test_data["test_data"]["hours"], row_index)
        timesheet_page.save_timesheet()

        assert timesheet_page.is_save_successful(), "Timesheet save failed"
        time.sleep(2)
        # STEP 4: Verify Total Hours
        total_hours = timesheet_page.get_row_total(row_index)
        assert total_hours == test_data["test_data"]["expected_total_hours"], \
            f"Total hours should be '{test_data['test_data']['expected_total_hours']}', got '{total_hours}'"


    # [TimeSheet-6]: Kiểm tra tính năng nhân viên tạo timesheet 1 project nhưng không thêm trường hours
    # "TIMESHEETS_06": {
    #     "test_name": "Employee creates timesheet with project without assigned time",
    #     "category": "negative",
    #     "description": "Employee tries to submit timesheet for project with no assigned time",
    #     "test_data": {
    #         "project": "ACME Ltd",
    #         "activity": "Development"
    #     },
    #     "expected_result": "Save/Submit blocked - no assigned time for project"
    # }
    def test_timesheet_06_project_no_assigned_time(self, load_timesheet_data, create_mock_employee):
        """
        Negative Testcase: Employee tries to submit timesheet for project with no assigned time

        Flow:
        -----
        Step 1: Employee logs in and creates timesheet
        Step 2: Employee adds project/activity but leaves hours empty
        Step 3: Employee save record
        Step 4: Verify that submission is blocked

        Expected Result:
        ---------------
        - Submission should be blocked
        - Appropriate error message should be displayed
        """
        test_data = load_timesheet_data["test_cases"]["TIMESHEETS_06"]
        username, password, _, _ = create_mock_employee

        # STEP 1: Employee Login
        timesheet_page = self._login_and_navigate(
            username, password, is_employee=True
        )

        # STEP 2: Create/Edit Timesheet
        self._create_or_edit_timesheet(timesheet_page)

        # STEP 3: Add Project/Activity without hours
        row_index = self._prepare_timesheet_row(timesheet_page, test_data["test_data"]["project"], test_data["test_data"]["activity"])
        # Do not fill any hours
        timesheet_page.save_timesheet()

        # if save is successful --> fail the test
        if timesheet_page.is_save_successful():
            pytest.fail(f"Expected error message '{test_data['expected_result']}', but timesheet was saved successfully")
        else:
            print(f"✓ Save blocked as expected with message: '{test_data['expected_result']}'")

    # "TIMESHEETS_07": {
    #       "test_name": "Employee attempts to enter negative hours in timesheet",
    #       "category": "negative",
    #       "description": "Employee inputs negative hours for a day",
    #       "test_data": {
    #         "project": "ACME Ltd",
    #         "activity": "Development",
    #         "hours": {
    #           "monday": "-5",
    #           "tuesday": "8"
    #         }
    #       },
    #       "expected_result": "Should Be Less Than 24 and in HH:MM or Decimal Format"
    #     }
    def test_timesheet_07_negative_hours_entry(self, load_timesheet_data, create_mock_employee):
        """
        Negative Testcase: Employee attempts to enter negative hours in timesheet

        Flow:
        -----
        Step 1: Employee logs in and creates timesheet
        Step 2: Employee adds project/activity and enters negative hours
        Step 3: Check contain error "Should Be Less Than 24 and in HH:MM or Decimal Format"

        Expected Result:
        ---------------
        - Negative hours should be rejected
        - Appropriate error message should be displayed
        """
        test_data = load_timesheet_data["test_cases"]["TIMESHEETS_07"]
        username, password, _, _ = create_mock_employee

        # STEP 1: Employee Login
        timesheet_page = self._login_and_navigate(
            username, password, is_employee=True
        )

        # STEP 2: Create/Edit Timesheet
        self._create_or_edit_timesheet(timesheet_page)

        # STEP 3: Add Project/Activity with Negative Hours
        row_index = self._prepare_timesheet_row(timesheet_page, test_data["test_data"]["project"], test_data["test_data"]["activity"])
        self._fill_timesheet_hours(timesheet_page, test_data["test_data"]["hours"], row_index)

        assert timesheet_page.is_hours_error_visible() , \
            f"Expected error message '{test_data['expected_result']}' not displayed for negative hours entry"

    # "TIMESHEETS_08": {
    #     "test_name": "Employee attempts to enter hours exceeding 24 in a day",
    #     "category": "negative",
    #     "description": "Employee inputs hours greater than 24 for a day",
    #     "test_data": {
    #         "project": "ACME Ltd",
    #         "activity": "Development",
    #         "hours": {
    #             "monday": "25",
    #             "tuesday": "8"
    #         }
    #     },
    #     "expected_result": "Should not exceed 24"
    # }
    def test_timesheet_08_exceeding_24_hours_entry(self, load_timesheet_data, create_mock_employee):
        """
        Negative Testcase: Employee attempts to enter hours exceeding 24 in a day

        Flow:
        -----
        Step 1: Employee logs in and creates timesheet
        Step 2: Employee adds project/activity and enters hours > 24
        Step 3: Check contain error "Should not exceed 24"

        Expected Result:
        ---------------
        - Hours exceeding 24 should be rejected
        - Appropriate error message should be displayed
        """
        test_data = load_timesheet_data["test_cases"]["TIMESHEETS_08"]
        username, password, _, _ = create_mock_employee

        # STEP 1: Employee Login
        timesheet_page = self._login_and_navigate(
            username, password, is_employee=True
        )

        # STEP 2: Create/Edit Timesheet
        self._create_or_edit_timesheet(timesheet_page)

        # STEP 3: Add Project/Activity with Exceeding Hours
        row_index = self._prepare_timesheet_row(timesheet_page, test_data["test_data"]["project"], test_data["test_data"]["activity"])
        self._fill_timesheet_hours(timesheet_page, test_data["test_data"]["hours"], row_index)

        assert timesheet_page.is_hours_error_visible() , \
            f"Expected error message '{test_data['expected_result']}' not displayed for exceeding hours entry"

    # "TIMESHEETS_09": {
    #     "test_name": "Employee attempts to enter invalid text format for hours",
    #     "category": "negative",
    #     "description": "Employee inputs non-numeric text for hours",
    #     "test_data": {
    #         "project": "ACME Ltd",
    #         "activity": "Development",
    #         "hours": {
    #             "monday": "abc",
    #             "tuesday": "eight"
    #         }
    #     },
    #     "expected_result": "Error: Invalid or field reject non-numeric input"
    # }
    def test_timesheet_09_invalid_text_format_hours_entry(self, load_timesheet_data, create_mock_employee):
        """
        Negative Testcase: Employee attempts to enter invalid text format for hours

        Flow:
        -----
        Step 1: Employee logs in and creates timesheet
        Step 2: Employee adds project/activity and enters non-numeric text for hours
        Step 3: Check contain error "Error: Invalid or field reject non-numeric input"

        Expected Result:
        ---------------
        - Non-numeric text should be rejected
        - Appropriate error message should be displayed
        """
        test_data = load_timesheet_data["test_cases"]["TIMESHEETS_09"]
        username, password, _, _ = create_mock_employee

        # STEP 1: Employee Login
        timesheet_page = self._login_and_navigate(
            username, password, is_employee=True
        )

        # STEP 2: Create/Edit Timesheet
        self._create_or_edit_timesheet(timesheet_page)

        # STEP 3: Add Project/Activity with Invalid Text Hours
        row_index = self._prepare_timesheet_row(timesheet_page, test_data["test_data"]["project"], test_data["test_data"]["activity"])
        self._fill_timesheet_hours(timesheet_page, test_data["test_data"]["hours"], row_index)

        assert timesheet_page.is_hours_error_visible() , \
            f"Expected error message '{test_data['expected_result']}' not displayed for invalid text hours entry"

    # "TIMESHEETS_10": {
    #     "test_name": "Employee attempts to create timesheet for a future week",
    #     "category": "negative",
    #     "description": "Employee creates timesheet for next week and create timesheet",
    #     "test_data": {
    #         "expected_create_timesheet": "disabled"
    #     },
    #     "expected_result": "Cannot submit future timesheet"
    # }
    def test_timesheet_10_create_future_week_timesheet(self, load_timesheet_data, create_mock_employee):
        """
        Negative Testcase: Employee attempts to create timesheet for a future week

        Flow:
        -----
        Step 1: Employee logs in and navigates to timesheet page
        Step 2: Employee selects next week
        Step 3: Check if "Create Timesheet" button is disabled

        Expected Result:
        ---------------
        - Employee should not be able to create timesheet for future week
        - Appropriate message or disabled state should be displayed
        """
        test_data = load_timesheet_data["test_cases"]["TIMESHEETS_10"]
        username, password, _, _ = create_mock_employee

        # STEP 1: Employee Login
        timesheet_page = self._login_and_navigate(
            username, password, is_employee=True
        )

        # STEP 2: Select Next Week
        timesheet_page.go_to_next_week()
        time.sleep(2)

        # STEP 3: Verify "Create Timesheet" Button State
        is_create_disabled = timesheet_page.is_create_timesheet_button_disabled()
        assert is_create_disabled, \
            f"Expected 'Create Timesheet' button to be disabled for future week, but it was enabled"

    # "TIMESHEETS_11": {
    #     "test_name": "Check that approved timesheet cannot be edited",
    #     "category": "negative",
    #     "description": "Employee tries to edit timesheet after Supervisor approval",
    #     "test_data": {
    #         "project": "ACME Ltd",
    #         "activity": "Development",
    #         "hours": {
    #             "monday": "8",
    #             "tuesday": "8",
    #             "wednesday": "8",
    #             "thursday": "8",
    #             "friday": "8"
    #         },
    #         "expected_status_after_submit": "Submitted",
    #         "expected_status_after_approve": "Approved",
    #         "edit_attempt_after_approval": true
    #     },
    #     "expected_result": "Edit button disabled or hidden, cannot edit approved timesheet"
    # }
    def test_timesheet_11_edit_approved_timesheet(self, load_timesheet_data, create_mock_employee):
        """
        Negative Testcase: Check that approved timesheet cannot be edited

        Flow:
        -----
        Step 1: Employee logs in and creates timesheet
        Step 2: Employee adds project/activity and hours
        Step 3: Employee submits timesheet
        Step 4: Supervisor approves timesheet
        Step 5: Employee attempts to edit approved timesheet

        Expected Result:
        ---------------
        - Edit button should be disabled or hidden for approved timesheet
        - Employee should not be able to edit approved timesheet
        """
        test_data = load_timesheet_data["test_cases"]["TIMESHEETS_11"]
        username, password, _, _ = create_mock_employee

        # STEP 1: Employee Login
        timesheet_page = self._login_and_navigate(
            username, password, is_employee=True
        )
        employee_name = timesheet_page.get_employee_name()

        # STEP 2: Create/Edit Timesheet
        self._create_or_edit_timesheet(timesheet_page)

        # STEP 3: Add Project/Activity and Hours
        row_index = self._prepare_timesheet_row(timesheet_page, test_data["test_data"]["project"], test_data["test_data"]["activity"])
        self._fill_timesheet_hours(timesheet_page, test_data["test_data"]["hours"], row_index)
        timesheet_page.save_timesheet()
        assert timesheet_page.is_save_successful(), "Timesheet save failed"

        # STEP 4: Submit
        timesheet_page.click_submit()
        time.sleep(2)
        submitted_status = timesheet_page.get_timesheet_status()
        assert submitted_status == test_data["test_data"]["expected_status_after_submit"], \
            f"Status should be 'Submitted', got '{submitted_status}'"
        # STEP 5: Supervisor Approves
        self._logout()
        timesheet_page = self._login_and_navigate(
            VALID_USERNAME, VALID_PASSWORD, is_employee=False
        )
        timesheet_page.search_employee_timesheet(employee_name)
        timesheet_page.view_employee_timesheet()
        timesheet_page.click_approve()
        # STEP 6: Attempt to Edit Approved Timesheet
        self._logout()
        timesheet_page = self._login_and_navigate(
            username, password, is_employee=True
        )
        can_edit = timesheet_page.is_edit_button_visible()
        assert not can_edit, \
            "Edit button should be disabled or hidden for approved timesheet, but it is visible"
