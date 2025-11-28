"""Dashboard page object containing dashboard-related elements and actions."""
from playwright.sync_api import Page
from pages.base import BasePage


class DashboardPage(BasePage):
    """Page object for the dashboard page."""

    # Selectors
    USER_DROPDOWN = '.oxd-userdropdown-tab'
    LOGOUT_LINK = 'a:has-text("Logout")'
    PIM_MODULE = '//a[.//span[text()="PIM"]]'
    TIME_MODULE = '//a[.//span[text()="Time"]]'
    USER_NAME_IN_DROPDOWN = '.oxd-userdropdown-name'

    def __init__(self, page: Page):
        """Initialize the dashboard page.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)

    def navigate_to_pim(self) -> None:
        """Navigate to the PIM module."""
        self._click(self.PIM_MODULE)

    def navigate_to_time(self) -> None:
        """Navigate to the Time module."""
        self._click(self.TIME_MODULE)
        self.page.wait_for_load_state('networkidle')

    def logout(self) -> None:
        """Perform the logout action."""
        self._click(self.USER_DROPDOWN)
        self._click(self.LOGOUT_LINK)

    def is_user_dropdown_visible(self) -> bool:
        """Check if the user dropdown is visible (indicates successful login).

        Returns:
            bool: True if user dropdown is visible, False otherwise
        """
        return self._is_element_visible(self.USER_DROPDOWN)

    def get_logged_in_user_name(self) -> str:
        """Get the name of the currently logged-in user.

        Returns:
            str: The logged-in user's name
        """
        self._click(self.USER_DROPDOWN)
        return self._get_text(self.USER_NAME_IN_DROPDOWN)
