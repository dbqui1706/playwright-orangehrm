"""Test cases for login functionality using Playwright."""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config import VALID_USERNAME, VALID_PASSWORD


@pytest.mark.usefixtures("driver_init")
class TestLogin:
    """Test suite for login functionality."""

    def test_successful_login(self):
        """Test successful login with valid credentials."""
        # Arrange
        login_page = LoginPage(self.page)

        # Act
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        # Assert
        dashboard_page = DashboardPage(self.page)
        assert dashboard_page.is_user_dropdown_visible(), \
            "Login failed: User dropdown is not visible on dashboard"

    def test_login_with_invalid_password(self):
        """Test login failure with invalid password."""
        # Arrange
        login_page = LoginPage(self.page)
        invalid_password = "wrongpassword"

        # Act
        login_page.login(VALID_USERNAME, invalid_password)

        # Assert
        error_message = login_page.get_invalid_credentials_message()
        assert "Invalid credentials" in error_message, \
            f"Expected 'Invalid credentials' error message, got: '{error_message}'"

    def test_login_with_invalid_username(self):
        """Test login failure with invalid username."""
        # Arrange
        login_page = LoginPage(self.page)
        invalid_username = "InvalidUser"

        # Act
        login_page.login(invalid_username, VALID_PASSWORD)

        # Assert
        error_message = login_page.get_invalid_credentials_message()
        assert "Invalid credentials" in error_message, \
            f"Expected 'Invalid credentials' error message, got: '{error_message}'"

    def test_login_with_empty_credentials(self):
        """Test login failure with empty username and password."""
        # Arrange
        login_page = LoginPage(self.page)

        # Act
        login_page.login("", "")

        # Assert
        # Should still be on login page
        assert login_page.is_on_login_page(), \
            "Expected to remain on login page with empty credentials"
