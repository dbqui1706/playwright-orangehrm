"""Login page object containing login-related elements and actions."""
from playwright.sync_api import Page
from pages.base import BasePage
from config import BASE_URL


class LoginPage(BasePage):
    """Page object for the login page."""

    # Selectors
    USERNAME_INPUT = 'input[name="username"]'
    PASSWORD_INPUT = 'input[name="password"]'
    LOGIN_BUTTON = 'button[type="submit"]'
    INVALID_CREDENTIALS_MESSAGE = 'p.oxd-alert-content-text'

    def __init__(self, page: Page):
        """Initialize the login page and navigate to it.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        self.page.goto(BASE_URL, wait_until='domcontentloaded', timeout=60000)
        self.page.wait_for_timeout(2000)  # Additional wait for page to stabilize

    def login(self, username: str, password: str) -> None:
        """Perform the login action.

        Args:
            username: Username for login
            password: Password for login
        """
        self._send_keys(self.USERNAME_INPUT, username)
        self._send_keys(self.PASSWORD_INPUT, password)
        self._click(self.LOGIN_BUTTON)

    def get_invalid_credentials_message(self) -> str:
        """Get the error message for invalid credentials.

        Returns:
            str: The error message text
        """
        return self._get_text(self.INVALID_CREDENTIALS_MESSAGE)

    def is_on_login_page(self) -> bool:
        """Check if currently on the login page.

        Returns:
            bool: True if on login page, False otherwise
        """
        return "login" in self.page.url.lower()
