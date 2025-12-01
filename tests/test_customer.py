"""Test cases for Add Customer functionality using Playwright."""
import pytest
import time
import json
import os
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.customer_page import CustomerPage, CustomerErrorMessages
from config import VALID_USERNAME, VALID_PASSWORD

ABS_DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_FILE_PATH = os.path.join(ABS_DATA, "test-data", "customers_data.json")

with open(DATA_FILE_PATH) as f:
    CUSTOMER_DATA = json.load(f)
    CUSTOMER_DATA = CUSTOMER_DATA["test_cases"]

@pytest.mark.usefixtures("driver_init")
class TestCustomer:
    """Test suite for Add Customer functionality in Time module."""

    @pytest.fixture
    def customer_page(self):
        """Login and navigate to Customer page.

        Returns:
            CustomerPage: Instance of CustomerPage ready for testing
        """
        # Login
        login_page = LoginPage(self.page)
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        # Navigate to Time module
        dashboard_page = DashboardPage(self.page)
        dashboard_page.navigate_to_time()

        # Navigate to Customers
        customer_page = CustomerPage(self.page)
        customer_page.navigate_to_customer_page()

        return customer_page

    # ==================== POSITIVE TEST CASES ====================

    def test_add_customer_with_name_and_description(self, customer_page: CustomerPage):
        """TC01: Add customer with valid name and description.

        Test Case ID: TC01
        Description: Verify that a customer can be added with both name and description
        Expected: Customer is successfully created and saved
        """
        # Arrange
        data = CUSTOMER_DATA["CUST_TC01"]['test_data']
        customer_name = data["customer_name"]
        description = data["description"]

        # Act
        customer_page.add_customer(customer_name, description)

        # Assert
        assert customer_page.is_success_message_visible(), \
            "Success message should be displayed after adding customer"

        # Verify customer appears in list
        time.sleep(1)
        assert customer_page.search_customer(customer_name) ,\
            f"Customer '{customer_name}' should appear in the customer list"


    def test_add_customer_with_name_only(self, customer_page: CustomerPage):
        """TC02: Add customer with only name (description left blank).

        Test Case ID: TC02
        Description: Verify that a customer can be added with only name, no description
        Expected: Customer is successfully created without description
        """

        data = CUSTOMER_DATA["CUST_TC02"]['test_data']
        customer_name = data["customer_name"]
        description = data["description"]

        # Act
        customer_page.add_customer(customer_name, description=description)

        # Assert
        assert customer_page.is_success_message_visible(), \
            "Success message should be displayed even without description"

        # Verify customer appears in list
        time.sleep(1)
        assert customer_page.search_customer(customer_name), \
            f"Customer '{customer_name}' should appear in the customer list"

    # ==================== NEGATIVE TEST CASES - VALIDATION ====================

    def test_add_customer_with_empty_name(self, customer_page: CustomerPage):
        """TC03: Add customer with empty name field.

        Test Case ID: TC03
        Description: Verify validation when customer name is left empty
        Expected: Error message "Required" is displayed, form is not submitted
        """
        # Act
        customer_page.click_add_customer()
        # Leave name empty, just click save
        customer_page.click_save()

        # Assert
        assert customer_page.is_required_error_message(CustomerErrorMessages.REQUIRED), \
            "Required error message should be displayed for empty customer name"

        # error_messages = customer_page.get_required_error_messages()
        # assert len(error_messages) > 0, "Should have at least one required error"
        # assert "Required" in str(error_messages), \
        #     "Error message should contain 'Required'"

    def test_add_customer_name_exceeds_max_length(self, customer_page: CustomerPage):
        """TC04: Add customer with name exceeding 50 characters.

        Test Case ID: TC04
        Description: Verify validation when customer name exceeds maximum length (50 chars)
        Expected: Error validation message or input is truncated to 50 characters
        """
        # Arrange
        data = CUSTOMER_DATA["CUST_TC04"]['test_data']
        long_name = data["customer_name"]

        # Act
        customer_page.click_add_customer()
        customer_page.enter_customer_name(long_name)
        time.sleep(1)

        # Check the error message
        assert customer_page.is_required_error_message(CustomerErrorMessages.EXCEEDS_LIMIT), \
            f"Customer name should be truncated to 50 chars, but got {len(long_name)} chars"

    def test_add_customer_with_duplicate_name(self, customer_page: CustomerPage):
        """TC05: Add customer with name that already exists.

        Test Case ID: TC05
        Description: Verify validation when attempting to create customer with duplicate name
        Expected: Error message "Already exists" or similar duplicate error
        """
        # Arrange - First create a customer
        data = CUSTOMER_DATA["CUST_TC05"]['test_data']
        customer_name = data["customer_name"]
        description = data["description"]

        # Act - Add first customer
        # Ensure customer exists (MUST run TC01 first)
        assert customer_page.search_customer(customer_name), \
            f"Customer '{customer_name}' should appear in the customer list"

        # Try to add duplicate customer with same name
        customer_page.add_customer(customer_name, description)
        customer_page.click_save()

        # Assert - Should show duplicate error
        assert customer_page.is_required_error_message(CustomerErrorMessages.DUPLICATE), \
            "Should display 'Already exists' error for duplicate customer name"

    def test_add_customer_with_special_characters(self, customer_page: CustomerPage):
        """TC06: Add customer with special characters in name.

        Test Case ID: TC06
        Description: Verify behavior when customer name contains special characters (<, >, &) and scripts
        Expected: Test actual system behavior - may accept, reject, or escape special chars
        """
        # Arrange
        data = CUSTOMER_DATA["CUST_TC06"]['test_data']
        special_name = data["customer_name"]

        # Act
        customer_page.click_add_customer()
        customer_page.enter_customer_name(special_name)
        customer_page.click_save()

        # Wait for system response
        time.sleep(2)

        # If success then Website don't block special characters -> Assert fail for this case
        assert not customer_page.is_success_message_visible(), "System should not accept special characters or scripts in customer name"
