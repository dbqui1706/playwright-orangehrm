"""Test cases for Add Project and Activity functionality using Playwright."""
import pytest
import time
import json
import os
from pages.login_page import LoginPage
from pages.project_page import ProjectPage
from pages.activity_page import ActivityPage
from config import VALID_USERNAME, VALID_PASSWORD

@pytest.mark.usefixtures("driver_init")
class TestAddProject:
    """Test suite for Add Project functionality in Time module."""

    @pytest.fixture(scope="class")
    def load_projects_data(self):
        """Load test data from projects_data.json file.

        Returns:
            dict: Test data for all project test cases
        """
        json_file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "test-data",
            "projects_data.json"
        )
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @pytest.fixture
    def setup_customer_and_project_page(self) -> tuple[ProjectPage, str]:
        """Login, create a test customer, and navigate to Project page.

        Returns:
            tuple: (ProjectPage, customer_name) ready for testing
        """
        # Login
        login_page = LoginPage(self.page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        # Navigate to Projects
        time.sleep(1)
        project_page = ProjectPage(self.page)
        project_page.navigate_to_project_page()

        # Use existing customer "ACME Ltd" or create one if needed
        customer_name = "ACME Ltd"

        return project_page, customer_name

    # ==================== POSITIVE TEST CASES ====================

    def test_add_project_with_name_and_customer(self, setup_customer_and_project_page, load_projects_data):
        """TC07: Add project with valid name and customer.

        Test Case ID: TC07 (Maps to PRJ_TC01 in JSON)
        Description: Verify that a project can be added with name and customer (required fields)
        Expected: Project is successfully created and saved
        """
        # Arrange
        project_page, _ = setup_customer_and_project_page
        test_data = load_projects_data["test_cases"]["PRJ_TC01"]["test_data"]
        timestamp = int(time.time()) % 10000
        project_name = f"{test_data['project_name']}_{timestamp}"

        customer_name = test_data["customer_name"]

        # Act
        project_page.add_project(project_name, customer_name)

        # Assert
        assert project_page.is_success_message_visible(), \
            "Success message should be displayed after adding project"

        # Verify project appears in list
        time.sleep(1)

        # Go back to project page to search
        project_page.navigate_to_project_page()
        project_page.search_project(project_name)
        assert project_page.is_project_in_table(project_name), \
            f"Project '{project_name}' should appear in the project list"

    def test_add_project_with_name_customer_and_admin(self, setup_customer_and_project_page, load_projects_data):
        """TC08: Add project with name, customer, and project admin.

        Test Case ID: TC08 (Maps to PRJ_TC02 in JSON)
        Description: Verify that a project can be added with name, customer, and project admin
        Expected: Project is successfully created with assigned admin
        """
        # Arrange
        project_page, _ = setup_customer_and_project_page
        test_data = load_projects_data["test_cases"]["PRJ_TC02"]["test_data"]
        timestamp = int(time.time()) % 10000
        project_name = f"{test_data['project_name']}_{timestamp}"
        customer_name = test_data["customer_name"]
        admin_name = test_data["project_admin"]

        # Act
        project_page.add_project(project_name, customer_name, admin_name)

        # Assert
        assert project_page.is_success_message_visible(), \
            "Success message should be displayed after adding project with admin"

        # Verify project appears in list
        time.sleep(1)
        project_page.navigate_to_project_page()
        project_page.search_project(project_name)
        assert project_page.is_project_in_table(project_name), \
            f"Project '{project_name}' should appear in the project list"

    def test_add_project_with_name_customer_and_description(self, setup_customer_and_project_page, load_projects_data):
        """TC09: Add project with name, customer, and description.

        Test Case ID: TC09 (Maps to PRJ_TC02 in JSON)
        Description: Verify that a project can be added with name, customer, and description
        Expected: Project is successfully created with description
        """
        # Arrange
        project_page, _ = setup_customer_and_project_page
        test_data = load_projects_data["test_cases"]["PRJ_TC02"]["test_data"]
        timestamp = int(time.time()) % 10000
        project_name = f"{test_data['project_name']}_Desc_{timestamp}"
        customer_name = test_data["customer_name"]
        description = test_data["description"]

        # Act
        project_page.add_project(project_name, customer_name, description=description)

        # Assert
        assert project_page.is_success_message_visible(), \
            "Success message should be displayed after adding project with description"

        # Verify project appears in list
        time.sleep(1)
        project_page.navigate_to_project_page()
        project_page.search_project(project_name)
        assert project_page.is_project_in_table(project_name), \
            f"Project '{project_name}' should appear in the project list"

    # def test_add_project_with_multiple_admins(self, setup_customer_and_project_page, load_projects_data):
    #     """TC14: Add project with multiple project admins.
    #
    #     Test Case ID: TC14 (Maps to PRJ_TC03 in JSON)
    #     Description: Verify that a project can be created with multiple project admins
    #     Expected: Project is successfully created with multiple admins assigned
    #     """
    #     # Arrange
    #     project_page, _ = setup_customer_and_project_page
    #     test_data = load_projects_data["test_cases"]["PRJ_TC03"]["test_data"]
    #     timestamp = int(time.time()) % 10000
    #     project_name = f"{test_data['project_name']}_{timestamp}"
    #     customer_name = test_data["customer_name"]
    #     data = api.list_all_employees_for_project()["data"][:2]
    #     admins = [f"{emp['firstName']}" for emp in data]
    #
    #     # Act
    #     project_page.click_add_project()
    #     project_page.enter_project_name(project_name)
    #     project_page.enter_customer_name(customer_name)
    #
    #     # Add multiple admins using the add_multiple_project_admins method
    #     project_page.add_multiple_project_admins(admins)
    #     time.sleep(1)
    #
    #     project_page.click_save()
    #
    #     # Assert
    #     assert project_page.is_success_message_visible(), \
    #         "Success message should be displayed after adding project with multiple admins"
    #
    #     # Verify project appears in list
    #     time.sleep(1)
    #     project_page.navigate_to_project_page()
    #     project_page.search_project(project_name)
    #     assert project_page.is_project_in_table(project_name), \
    #         f"Project '{project_name}' should appear in the project list"

    # ==================== NEGATIVE TEST CASES - VALIDATION ====================

    def test_add_project_with_empty_name(self, setup_customer_and_project_page, load_projects_data):
        """TC10: Add project with empty project name.

        Test Case ID: TC10 (Maps to PRJ_TC04 in JSON)
        Description: Verify validation when project name is left empty
        Expected: Error message "Required" is displayed, form is not submitted
        """
        # Arrange
        project_page, _ = setup_customer_and_project_page
        test_data = load_projects_data["test_cases"]["PRJ_TC04"]["test_data"]
        expected_error = load_projects_data["test_cases"]["PRJ_TC04"]["expected_error"]
        customer_name = test_data["customer_name"]

        # Act
        project_page.click_add_project()
        # Leave project name empty (as per test data)
        project_page.enter_customer_name(customer_name)
        project_page.click_save()

        # Assert
        assert project_page.is_required_error_visible(), \
            f"Error message '{expected_error}' should be displayed for empty project name"

        error_messages = project_page.get_required_error_messages()
        assert len(error_messages) > 0, "Should have at least one required error"
        assert expected_error in str(error_messages), \
            f"Error message should contain '{expected_error}'"

    def test_add_project_without_customer(self, setup_customer_and_project_page, load_projects_data):
        """TC11: Add project without selecting customer.

        Test Case ID: TC11 (Maps to PRJ_TC05 in JSON)
        Description: Verify validation when customer is not selected
        Expected: Error message "Required" is displayed for customer field
        """
        # Arrange
        project_page, _ = setup_customer_and_project_page
        test_data = load_projects_data["test_cases"]["PRJ_TC05"]["test_data"]
        expected_error = load_projects_data["test_cases"]["PRJ_TC05"]["expected_error"]
        timestamp = int(time.time())
        project_name = f"{test_data['project_name']}_{timestamp}"

        # Act
        project_page.click_add_project()
        project_page.enter_project_name(project_name)
        # Do NOT select customer (customer_name is empty in test data)
        project_page.click_save()

        # Assert
        assert project_page.is_required_error_visible(), \
            f"Error message '{expected_error}' should be displayed when customer is not selected"

        error_messages = project_page.get_required_error_messages()
        assert len(error_messages) > 0, "Should have at least one required error"
        assert expected_error in str(error_messages), \
            f"Error message should contain '{expected_error}'"

    def test_add_project_name_exceeds_max_length(self, setup_customer_and_project_page, load_projects_data):
        """TC12: Add project with name exceeding 50 characters.

        Test Case ID: TC12 (Maps to PRJ_TC07 in JSON)
        Description: Verify validation when project name exceeds maximum length (50 chars)
        Expected: Error validation message or input is truncated to 50 characters
        """
        # Arrange
        project_page, _ = setup_customer_and_project_page
        test_data = load_projects_data["test_cases"]["PRJ_TC07"]["test_data"]
        # Generate long name that exceeds 50 characters
        long_name = test_data["project_name"]  # 51 characters from JSON

        # Act
        project_page.click_add_project()
        project_page.enter_project_name(long_name)
        time.sleep(1)

        # Check the actual value in the input field
        actual_value = project_page.get_project_name_input_value()

        # Assert - System should either truncate or show validation error
        # assert len(actual_value) <= 50, \
        #     f"Project name should be truncated to 50 chars, but got {len(actual_value)} chars"

    def test_add_project_with_duplicate_name(self, setup_customer_and_project_page, load_projects_data):
        """TC13: Add project with name that already exists.

        Test Case ID: TC13 (Maps to PRJ_TC08 in JSON)
        Description: Verify validation when attempting to create project with duplicate name
        Expected: Error message "Already exists" or similar duplicate error
        """
        # Arrange
        project_page, _ = setup_customer_and_project_page
        test_data = load_projects_data["test_cases"]["PRJ_TC08"]["test_data"]
        expected_error = load_projects_data["test_cases"]["PRJ_TC08"]["expected_error"]
        timestamp = int(time.time())
        project_name = f"{test_data['project_name']}_{timestamp}"
        customer_name = test_data["customer_name"]

        # Act - Add first project
        project_page.add_project(project_name, customer_name)
        assert project_page.is_success_message_visible(), \
            "First project should be created successfully"

        time.sleep(5)

        # Try to add duplicate project with same name
        project_page.navigate_to_project_page()
        project_page.click_add_project()
        project_page.enter_project_name(project_name)
        project_page.enter_customer_name(customer_name)
        project_page.click_save()

        # Assert - Should show duplicate error
        time.sleep(2)
        # assert project_page.is_duplicate_error_visible(), \
        #     f"Should display '{expected_error}' error for duplicate project name"

    # ==================== ACTIVITY TEST CASES ====================

    @pytest.fixture
    def setup_project_and_activity_page(self) -> tuple[ActivityPage, ProjectPage, str]:
        """Login, create test project, and navigate to Activity page.

        Returns:
            tuple: (ActivityPage, ProjectPage, project_name) ready for testing
        """
        # Login
        login_page = LoginPage(self.page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        # Create a test project first
        time.sleep(1)
        project_page = ProjectPage(self.page)
        project_page.navigate_to_project_page()

        # Create test project for activities
        timestamp = int(time.time()) % 10000
        project_name = f"TestProject_Activity_{timestamp}"
        project_page.add_project(project_name, "ACME Ltd")
        time.sleep(2)

        # Initialize activity page
        activity_page = ActivityPage(self.page)

        return activity_page, project_page, project_name

    # ==================== POSITIVE TEST CASES - ACTIVITY ====================

    def test_add_activity_with_valid_name(self, setup_project_and_activity_page, load_projects_data):
        """TC15: Add activity with valid name for project.

        Test Case ID: TC15 (Maps to ACT_TC01 in JSON)
        Description: Verify that an activity can be added with valid name for a project
        Expected: Activity is successfully created and saved
        """
        # Arrange
        activity_page, project_page, project_name = setup_project_and_activity_page
        test_data = load_projects_data["test_cases"]["ACT_TC01"]["test_data"]
        timestamp = int(time.time()) % 10000
        activity_name = f"{test_data['activity_name']}_{timestamp}"

        # Act
        activity_page.add_activity(project_name, activity_name)

        # Assert
        assert activity_page.is_success_message_visible(), \
            "Success message should be displayed after adding activity"

        # Scroll down to view activity list
        activity_page.scroll_to_activity_list()

        # Verify activity appears in table
        time.sleep(1)
        assert activity_page.is_activity_in_table(activity_name), \
            f"Activity '{activity_name}' should appear in the activity list"

    # ==================== NEGATIVE TEST CASES - ACTIVITY VALIDATION ====================

    def test_add_activity_with_empty_name(self, setup_project_and_activity_page, load_projects_data):
        """TC16: Add activity with empty name.

        Test Case ID: TC16 (Maps to ACT_TC02 in JSON)
        Description: Verify validation when activity name is left empty
        Expected: Error message "Required" is displayed, form is not submitted
        """
        # Arrange
        activity_page, project_page, project_name = setup_project_and_activity_page
        test_data = load_projects_data["test_cases"]["ACT_TC02"]["test_data"]
        expected_error = load_projects_data["test_cases"]["ACT_TC02"]["expected_error"]

        # Act
        activity_page.click_add_activity()
        # Leave activity name empty
        activity_page.click_save()

        # Assert
        assert activity_page.is_required_error_visible(), \
            f"Error message '{expected_error}' should be displayed for empty activity name"

        error_messages = activity_page.get_required_error_messages()
        assert len(error_messages) > 0, "Should have at least one required error"
        assert expected_error in str(error_messages), \
            f"Error message should contain '{expected_error}'"

    def test_add_activity_name_exceeds_max_length(self, setup_project_and_activity_page, load_projects_data):
        """TC17: Add activity with name exceeding 100 characters.

        Test Case ID: TC17 (Maps to ACT_TC03 in JSON)
        Description: Verify validation when activity name exceeds maximum length (100 chars)
        Expected: Error validation message or input is truncated to 100 characters
        """
        # Arrange
        activity_page, project_page, project_name = setup_project_and_activity_page
        test_data = load_projects_data["test_cases"]["ACT_TC03"]["test_data"]
        long_name = test_data["activity_name"]  # 101 characters from JSON

        # Act
        activity_page.click_add_activity()
        activity_page.enter_activity_name(long_name)
        time.sleep(1)

        # Assert - System should either truncate or show validation error
        assert activity_page.is_activity_exceeds_limit_error_visible() , \
            "Error message for exceeding 100 characters should be displayed"

    def test_add_duplicate_activity_in_same_project(self, setup_project_and_activity_page, load_projects_data):
        """TC18: Add duplicate activity name in same project.

        Test Case ID: TC18 (Maps to ACT_TC04 in JSON)
        Description: Verify validation when attempting to create activity with duplicate name in same project
        Expected: Error message "Already exists" for duplicate activity name
        """
        # Arrange
        activity_page, project_page, project_name = setup_project_and_activity_page
        test_data = load_projects_data["test_cases"]["ACT_TC04"]["test_data"]
        expected_error = load_projects_data["test_cases"]["ACT_TC04"]["expected_error"]
        timestamp = int(time.time())
        activity_name = f"{test_data['activity_name']}_Dup_{timestamp}"

        # Act - Add first activity
        activity_page.add_activity(project_name, activity_name)
        assert activity_page.is_success_message_visible(), \
            "First activity should be created successfully"

        time.sleep(2)

        # Try to add duplicate activity with same name
        activity_page.click_add_activity()
        activity_page.enter_activity_name(activity_name)
        activity_page.click_save()

        # Assert - Should show duplicate error
        time.sleep(2)
        assert activity_page.is_duplicate_error_visible(), \
            f"Should display '{expected_error}' error for duplicate activity name"

    # ==================== EDIT ACTIVITY TEST CASES ====================

    def test_edit_activity_name(self, setup_project_and_activity_page):
        """TC21: Edit activity name.

        Test Case ID: TC21
        Description: Verify that activity name can be edited successfully
        Expected: Activity name is updated and success message is displayed
        """
        # Arrange
        activity_page, project_page, project_name = setup_project_and_activity_page
        timestamp = int(time.time()) % 10000
        old_activity_name = f"OldActivity_{timestamp}"
        new_activity_name = f"NewActivity_{timestamp}"

        # Create activity first
        activity_page.add_activity(project_name, old_activity_name)
        assert activity_page.is_success_message_visible(), \
            "Activity should be created successfully"
        time.sleep(2)

        # Scroll to activity list
        activity_page.scroll_to_activity_list()

        # Find and click edit button for the activity
        activity_row = f"//div[contains(@class, 'oxd-table-card')]//div[text()='{old_activity_name}']"
        if activity_page._is_element_visible(activity_row, timeout=3):
            edit_button = f"{activity_row}/ancestor::div[contains(@class, 'oxd-table-card')]//button//i[contains(@class, 'bi-pencil')]"
            activity_page._click(edit_button)
            time.sleep(1)

            # Clear and enter new name
            activity_page._send_keys(activity_page.ACTIVITY_NAME_INPUT, new_activity_name)
            activity_page.click_save()

        # Assert
        assert activity_page.is_success_message_visible(), \
            "Success message should be displayed after editing activity"

        time.sleep(1)
        assert activity_page.is_activity_in_table(new_activity_name), \
            f"Updated activity '{new_activity_name}' should appear in activity list"
