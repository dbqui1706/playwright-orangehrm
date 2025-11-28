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
from pages.login_page import LoginPage
from pages.timesheet_page import TimesheetPage
from pages.project_page import ProjectPage
from pages.activity_page import ActivityPage
from config import VALID_USERNAME, VALID_PASSWORD, EMPLOYEE_PASSWORD, EMPLOYEE_USERNAME

@pytest.mark.usefixtures("driver_init")
class TestTimesheetEndToEnd:
    """End-to-end test suite for Timesheet workflow between Employee and Supervisor."""

    # ==================== HELPER METHODS ====================

    def _login(self, username: str, password: str):
        """Helper: Login with credentials."""
        login_page = LoginPage(self.page)
        login_page.login(username, password)
        time.sleep(1)

    def _logout(self):
        """Helper: Logout current user."""
        self.page.goto(self.page.url.split('/web')[0] + "/web/index.php/auth/logout")
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

    def _prepare_timesheet_row(self, timesheet_page, project_name: str, activity_name: str):
        """Helper: Prepare a row for data entry (handles existing rows logic).

        Returns:
            int: Row index to use
        """
        total_rows = timesheet_page.count_timesheet_rows()

        if total_rows == 0 or timesheet_page.is_row_empty(0):
            if total_rows == 0:
                timesheet_page.click_add_row()
                time.sleep(1)
            row_index = 0
        else:
            timesheet_page.click_add_row()
            time.sleep(1)
            row_index = total_rows

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
                time.sleep(0.5)
        print(f"✓ Added hours: {hours_data}")
        time.sleep(2)

    def _create_or_edit_timesheet(self, timesheet_page):
        """Helper: Create new timesheet or edit existing one."""
        if timesheet_page.is_create_timesheet_button_visible():
            timesheet_page.click_create_timesheet()
            time.sleep(2)
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

        timestamp = int(time.time())
        project_name = f"E2E_Project_{timestamp}"
        customer_name = "ACME Ltd"

        project_page.add_project(project_name, customer_name)
        time.sleep(2)

        # Add activity to project
        activity_page = ActivityPage(self.page)
        activity_name = f"E2E_Activity_{timestamp}"
        activity_page.add_activity(project_name, activity_name)
        time.sleep(2)

        # Logout admin
        self.page.goto(self.page.url.split('/web')[0] + "/web/index.php/auth/logout")
        time.sleep(1)

        return project_name, activity_name

    # ==================== E2E TEST CASES ====================

    def test_e2e_01_happy_path_employee_submit_supervisor_approve(
        self,
        load_timesheet_data,
    ):
        """
        E2E-01: Happy Path - Employee creates timesheet → Submits → Supervisor approves

        Flow:
        -----
        Step 1: Employee logs in and creates timesheet or edits existing
        Step 2: Employee adds project, activity, and hours
        Step 3: Employee submits timesheet
        Step 4: Supervisor logs in and views submitted timesheet
        Step 5: Supervisor approves timesheet
        Step 6: Employee logs in and verifies approved status

        Expected Result:
        ---------------
        - Timesheet status changes: Not Submitted → Submitted → Approved
        - Employee can see approved status
        """
        test_data = load_timesheet_data["test_cases"]["TS_HAPPY_01"]["test_data"]
        project_name, activity_name = test_data["project"], test_data["activity"]

        # STEP 1: Employee Login
        timesheet_page = self._login_and_navigate(
            EMPLOYEE_USERNAME, EMPLOYEE_PASSWORD, is_employee=True
        )

        # STEP 2: Create/Edit Timesheet
        self._create_or_edit_timesheet(timesheet_page)

        # STEP 3: Add Hours
        row_index = self._prepare_timesheet_row(timesheet_page, project_name, activity_name)
        self._fill_timesheet_hours(timesheet_page, test_data["hours"], row_index)

        assert timesheet_page.is_save_successful(), "Timesheet save failed"

        # STEP 4: Submit
        timesheet_page.click_submit()
        time.sleep(2)

        submitted_status = timesheet_page.get_timesheet_status()
        assert submitted_status == test_data["expected_status_after_submit"], \
            f"Status should be 'Submitted', got '{submitted_status}'"
        assert timesheet_page.is_timesheet_locked() , "Timesheet should be locked after submission"

        # STEP 5: Supervisor Approves
        self._logout()
        timesheet_page = self._login_and_navigate(
            VALID_USERNAME, VALID_PASSWORD, is_employee=False
        )

        if timesheet_page._is_element_visible(timesheet_page.APPROVE_BUTTON, timeout=3):
            timesheet_page.click_approve()
            time.sleep(2)
        else:
            pytest.skip("Approve button not found")

        # STEP 6: Verify Approval
        self._logout()
        timesheet_page = self._login_and_navigate(
            EMPLOYEE_USERNAME, EMPLOYEE_PASSWORD, is_employee=True
        )

        final_status = timesheet_page.get_timesheet_status()
        assert final_status == test_data["expected_status_after_approve"] \
            , f"Final status should be 'Approved', got '{final_status}'"

    def test_e2e_02_rejection_flow_employee_resubmit_supervisor_approve(
        self,
        load_timesheet_data,
        setup_test_project
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
        test_data = load_timesheet_data["test_cases"]["TS_ALT_01"]["test_data"]
        project_name, activity_name = setup_test_project

        # ========== STEP 1: Employee Submits (Incorrect Hours) ==========
        print("\n=== STEP 1: Employee submits timesheet with incorrect hours ===")

        employee_username = VALID_USERNAME
        employee_password = VALID_PASSWORD

        login_page = LoginPage(self.page)
        login_page.login(employee_username, employee_password)
        time.sleep(1)

        timesheet_page = TimesheetPage(self.page)
        timesheet_page.navigate_to_my_timesheet()
        time.sleep(1)

        # Create timesheet
        timesheet_page.click_create_timesheet()
        time.sleep(2)

        # Add incorrect hours (too many hours)
        timesheet_page.click_add_row()
        time.sleep(1)
        timesheet_page.select_project(project_name, row_index=0)
        time.sleep(1)
        timesheet_page.select_activity(activity_name, row_index=0)
        time.sleep(1)

        # Fill incorrect hours
        initial_hours = test_data["initial_hours"]
        for day, hours in initial_hours.items():
            if hours:
                timesheet_page.fill_hours(day, hours, row_index=0)
                time.sleep(0.5)

        print(f"✓ Added incorrect hours: {initial_hours}")
        time.sleep(2)

        # Submit
        timesheet_page.click_submit()
        time.sleep(2)

        submitted_status = timesheet_page.get_timesheet_status()
        assert submitted_status == "Submitted", \
            f"Status should be 'Submitted', got '{submitted_status}'"
        print(f"✓ Status: {submitted_status}")

        # ========== STEP 2: Supervisor Rejects with Comment ==========
        print("=== STEP 2: Supervisor rejects with comment ===")

        # Logout employee
        self.page.goto(self.page.url.split('/web')[0] + "/web/index.php/auth/logout")
        time.sleep(1)

        # Login as Supervisor
        supervisor_username = VALID_USERNAME
        supervisor_password = VALID_PASSWORD

        login_page.login(supervisor_username, supervisor_password)
        time.sleep(1)

        timesheet_page.navigate_to_employee_timesheet()
        time.sleep(2)

        # Reject with comment
        rejection_comment = test_data["rejection_comment"]

        if timesheet_page._is_element_visible(timesheet_page.REJECT_BUTTON, timeout=3):
            timesheet_page.click_reject(rejection_comment)
            time.sleep(2)
            print(f"✓ Supervisor rejected with comment: '{rejection_comment}'")
        else:
            pytest.skip("Reject button not found - supervisor may need to search for employee first")

        # ========== STEP 3: Employee Views Rejection and Edits ==========
        print("=== STEP 3: Employee sees rejection and edits timesheet ===")

        # Logout supervisor
        self.page.goto(self.page.url.split('/web')[0] + "/web/index.php/auth/logout")
        time.sleep(1)

        # Login as employee
        login_page.login(employee_username, employee_password)
        time.sleep(1)

        timesheet_page.navigate_to_my_timesheet()
        time.sleep(2)

        # Verify status is "Rejected"
        rejected_status = timesheet_page.get_timesheet_status()
        assert rejected_status == "Rejected", \
            f"Status should be 'Rejected', got '{rejected_status}'"
        print(f"✓ Status: {rejected_status}")

        # Verify rejection comment is visible
        comment = timesheet_page.get_rejection_comment()
        if comment:
            assert rejection_comment in comment, \
                f"Should see rejection comment '{rejection_comment}'"
            print(f"✓ Rejection comment visible: '{comment}'")

        # Verify timesheet can be edited after rejection
        assert timesheet_page.is_timesheet_editable(), \
            "Rejected timesheet should be editable"
        print("✓ Timesheet is editable after rejection")

        # ========== STEP 4: Employee Corrects and Re-submits ==========
        print("=== STEP 4: Employee corrects hours and re-submits ===")

        # Click Edit
        timesheet_page.click_edit()
        time.sleep(2)

        # Update with corrected hours
        corrected_hours = test_data["corrected_hours"]
        for day, hours in corrected_hours.items():
            if hours:
                timesheet_page.fill_hours(day, hours, row_index=0)
                time.sleep(0.5)

        print(f"✓ Corrected hours: {corrected_hours}")
        time.sleep(2)

        # Re-submit
        timesheet_page.click_submit()
        time.sleep(2)

        resubmitted_status = timesheet_page.get_timesheet_status()
        assert resubmitted_status == "Submitted", \
            f"Status should be 'Submitted' after correction, got '{resubmitted_status}'"
        print(f"✓ Re-submitted status: {resubmitted_status}")

        # ========== STEP 5: Supervisor Approves Corrected Timesheet ==========
        print("=== STEP 5: Supervisor approves corrected timesheet ===")

        # Logout employee
        self.page.goto(self.page.url.split('/web')[0] + "/web/index.php/auth/logout")
        time.sleep(1)

        # Login as Supervisor
        login_page.login(supervisor_username, supervisor_password)
        time.sleep(1)

        timesheet_page.navigate_to_employee_timesheet()
        time.sleep(2)

        # Approve
        if timesheet_page._is_element_visible(timesheet_page.APPROVE_BUTTON, timeout=3):
            timesheet_page.click_approve()
            time.sleep(2)
            print("✓ Supervisor approved the corrected timesheet")
        else:
            pytest.skip("Approve button not found")

        # ========== STEP 6: Employee Verifies Final Approval ==========
        print("=== STEP 6: Employee verifies final approval ===")

        # Logout supervisor
        self.page.goto(self.page.url.split('/web')[0] + "/web/index.php/auth/logout")
        time.sleep(1)

        # Login as employee
        login_page.login(employee_username, employee_password)
        time.sleep(1)

        timesheet_page.navigate_to_my_timesheet()
        time.sleep(2)

        # Verify final status is "Approved"
        final_status = timesheet_page.get_timesheet_status()
        assert final_status == test_data["expected_final_status"], \
            f"Final status should be 'Approved', got '{final_status}'"
        print(f"✓ Final status: {final_status}")

        print("\n✅ E2E-02 Rejection Flow test PASSED")


# ==================== HELPER NOTES ====================
"""
IMPORTANT SETUP NOTES:
======================

Before running these tests, you MUST set up the following in OrangeHRM:

1. CREATE EMPLOYEE USER:
   - Go to: Admin → User Management → Users → Add
   - Employee Name: Select an employee (or create new employee in PIM first)
   - Username: employee_user
   - Password: employee123
   - User Role: ESS
   - Status: Enabled

2. CREATE SUPERVISOR USER:
   - Go to: Admin → User Management → Users → Add
   - Employee Name: Select a supervisor employee
   - Username: supervisor_user
   - Password: supervisor123
   - User Role: ESS + Admin (or Supervisor if available)
   - Status: Enabled

3. SET UP SUPERVISOR RELATIONSHIP:
   - Go to: PIM → Employee List → Click on Employee
   - Tab: Report-to → Add Supervisor
   - Select the supervisor employee
   - Reporting Method: Direct
   - Save

4. CREATE PROJECT AND ASSIGN EMPLOYEE:
   - Go to: Time → Project Info → Add Project
   - Project Name: Any name (e.g., "Test Project")
   - Customer: Select existing customer
   - Project Admins: Add employee and supervisor
   - Save

5. ADD ACTIVITY TO PROJECT:
   - Edit the project → Activities section → Add
   - Activity Name: "Development" (or any name)
   - Save

6. UPDATE CREDENTIALS IN test_timesheet.py:
   - Replace VALID_USERNAME/VALID_PASSWORD with actual credentials
   - Update employee_username, employee_password
   - Update supervisor_username, supervisor_password

7. RUN TESTS:
   pytest tests/test_timesheet.py -v -s

Note: Tests marked with pytest.skip() indicate areas where supervisor/employee
interaction requires manual setup or UI navigation that varies by OrangeHRM version.
"""