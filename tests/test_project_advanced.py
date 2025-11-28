"""Advanced test cases for Project management functionality using Playwright."""
import pytest
import time
from pages.login_page import LoginPage
from pages.project_page import ProjectPage
from pages.activity_page import ActivityPage
from config import VALID_USERNAME, VALID_PASSWORD


@pytest.mark.usefixtures("driver_init")
class TestProjectAdvanced:
    """Test suite for Edit, Search, Delete and GUI verification of Projects."""

    @pytest.fixture
    def setup_project_page(self) -> tuple[ProjectPage, str]:
        """Login and navigate to Project page.

        Returns:
            tuple: (ProjectPage, test_project_name) ready for testing
        """
        # Login
        login_page = LoginPage(self.page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        # Navigate to Projects
        time.sleep(1)
        project_page = ProjectPage(self.page)
        project_page.navigate_to_project_page()

        # Create a test project for editing/deleting
        timestamp = int(time.time())
        test_project_name = f"TestProject_Advanced_{timestamp}"
        project_page.add_project(test_project_name, "ABC Corporation", "Admin")
        time.sleep(2)

        project_page.navigate_to_project_page()
        return project_page, test_project_name

    # ==================== EDIT PROJECT TEST CASES ====================

    def test_edit_project_name(self, setup_project_page):
        """TC19: Edit project name to a different name.

        Test Case ID: TC19
        Description: Verify that project name can be edited successfully
        Expected: Project name is updated and success message is displayed
        """
        # Arrange
        project_page, old_name = setup_project_page
        timestamp = int(time.time())
        new_name = f"EditedProject_{timestamp}"

        # Act
        project_page.edit_project_name(old_name, new_name)

        # Assert
        assert project_page.is_success_message_visible(), \
            "Success message should be displayed after editing project name"

        # Verify new name appears in table
        time.sleep(1)
        project_page.navigate_to_project_page()
        assert project_page.is_project_in_table(new_name), \
            f"Updated project name '{new_name}' should appear in project list"

        # Verify old name doesn't appear
        assert not project_page.is_project_in_table(old_name), \
            f"Old project name '{old_name}' should not appear in project list"

    def test_edit_project_customer(self, setup_project_page):
        """TC20: Edit project to change customer.

        Test Case ID: TC20
        Description: Verify that project customer can be changed successfully
        Expected: Project customer is updated and success message is displayed
        """
        # Arrange
        project_page, project_name = setup_project_page
        new_customer = "XYZ Technologies"

        # Act
        project_page.edit_project_customer(project_name, new_customer)

        # Assert
        assert project_page.is_success_message_visible(), \
            "Success message should be displayed after editing project customer"

        time.sleep(1)

    # TC21 and TC22 are activity-related and should be in test_activity.py

    # ==================== SEARCH/FILTER TEST CASES ====================

    def test_search_project_by_name(self, setup_project_page):
        """TC23: Search project by name (partial match).

        Test Case ID: TC23
        Description: Verify that projects can be searched by name
        Expected: Search results show projects matching the search term
        """
        # Arrange
        project_page, project_name = setup_project_page

        # Act
        project_page.navigate_to_project_page()
        project_page.search_project(project_name)

        # Assert
        assert project_page.is_project_in_table(project_name), \
            f"Project '{project_name}' should appear in search results"

        row_count = project_page.get_table_row_count()
        assert row_count > 0, "Search should return at least one project"

    def test_filter_by_customer(self, setup_project_page):
        """TC24: Filter projects by customer.

        Test Case ID: TC24
        Description: Verify that projects can be filtered by customer name
        Expected: Only projects for selected customer are displayed
        """
        # Arrange
        project_page, project_name = setup_project_page
        customer_name = "ABC Corporation"

        # Act
        project_page.navigate_to_project_page()
        project_page.search_by_customer(customer_name)

        # Assert
        row_count = project_page.get_table_row_count()
        assert row_count > 0, f"Should show projects for customer '{customer_name}'"

        # Verify our test project is in the results
        assert project_page.is_project_in_table(project_name), \
            f"Project '{project_name}' should be in filtered results for customer '{customer_name}'"

    def test_filter_by_project_admin(self, setup_project_page):
        """TC25: Filter projects by project admin.

        Test Case ID: TC25
        Description: Verify that projects can be filtered by project admin
        Expected: Only projects with selected admin are displayed
        """
        # Arrange
        project_page, project_name = setup_project_page
        admin_name = "Admin"

        # Act
        project_page.navigate_to_project_page()
        project_page.search_by_project_admin(admin_name)

        # Assert
        row_count = project_page.get_table_row_count()
        assert row_count > 0, f"Should show projects for admin '{admin_name}'"

        # Verify our test project is in the results
        assert project_page.is_project_in_table(project_name), \
            f"Project '{project_name}' should be in filtered results for admin '{admin_name}'"

    # ==================== DELETE PROJECT TEST CASES ====================

    def test_delete_project_without_activities(self, setup_project_page):
        """TC26: Delete project without activities.

        Test Case ID: TC26
        Description: Verify that a project without activities can be deleted
        Expected: Project is successfully deleted
        """
        # Arrange
        project_page, project_name = setup_project_page

        # Act
        project_page.delete_project(project_name)

        # Assert
        assert project_page.is_success_message_visible(), \
            "Success message should be displayed after deleting project"

        # Verify project is deleted
        time.sleep(1)
        project_page.navigate_to_project_page()
        assert not project_page.is_project_in_table(project_name), \
            f"Deleted project '{project_name}' should not appear in project list"

    def test_delete_project_with_activities_no_timesheet(self):
        """TC27: Delete project with activities but no timesheet data.

        Test Case ID: TC27
        Description: Verify that a project with activities (but no timesheet) can be deleted
        Expected: Project and activities are successfully deleted
        """
        # Login and setup
        login_page = LoginPage(self.page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        # Create project with activity
        project_page = ProjectPage(self.page)
        project_page.navigate_to_project_page()

        timestamp = int(time.time())
        project_name = f"ProjectWithActivity_{timestamp}"
        project_page.add_project(project_name, "ABC Corporation")
        time.sleep(2)

        # Add activity to project
        activity_page = ActivityPage(self.page)
        activity_name = f"TestActivity_{timestamp}"
        activity_page.add_activity(project_name, activity_name)
        time.sleep(2)

        # Act - Delete project
        project_page.navigate_to_project_page()
        project_page.delete_project(project_name)

        # Assert
        assert project_page.is_success_message_visible(), \
            "Success message should be displayed after deleting project with activities"

        time.sleep(1)
        project_page.navigate_to_project_page()
        assert not project_page.is_project_in_table(project_name), \
            f"Deleted project '{project_name}' should not appear in project list"

    def test_delete_project_with_timesheet_data(self):
        """TC28: Delete project with timesheet data.

        Test Case ID: TC28
        Description: Verify that deleting a project with timesheet data shows warning/blocks deletion
        Expected: Warning message is displayed or deletion is blocked
        """
        # NOTE: This test requires creating timesheet data first
        # For now, we'll test the delete warning mechanism
        # In a real scenario, you would:
        # 1. Create a project
        # 2. Create activities
        # 3. Create timesheet entries using those activities
        # 4. Try to delete the project
        # 5. Verify warning appears

        # This is a placeholder test - actual implementation depends on timesheet functionality
        pytest.skip("Requires timesheet data to be created first. Implement after timesheet module is ready.")

    # ==================== GUI VERIFICATION TEST CASES ====================

    def test_customer_dropdown_displays_all_customers(self):
        """TC29: Verify customer dropdown displays all customers.

        Test Case ID: TC29
        Description: Verify that customer dropdown shows all available customers
        Expected: All customers are displayed in dropdown
        """
        # Login and setup
        login_page = LoginPage(self.page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        project_page = ProjectPage(self.page)
        project_page.navigate_to_project_page()

        # Act
        customer_options = project_page.get_customer_dropdown_options()

        # Assert
        assert len(customer_options) > 0, "Customer dropdown should have at least one option"

        # Verify expected customers are in the list
        expected_customers = ["ABC Corporation", "XYZ Technologies"]
        for customer in expected_customers:
            assert any(customer in option for option in customer_options), \
                f"Customer '{customer}' should be in dropdown options"

    def test_project_admin_multiselect_works(self):
        """TC30: Verify project admin multi-select functionality.

        Test Case ID: TC30
        Description: Verify that project admin field supports selecting multiple admins
        Expected: Multiple admins can be selected for a project
        """
        # Login and setup
        login_page = LoginPage(self.page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        project_page = ProjectPage(self.page)
        project_page.navigate_to_project_page()

        # Act
        multiselect_works = project_page.verify_project_admin_multiselect()

        # Assert
        assert multiselect_works, \
            "Project admin field should support multi-select functionality"