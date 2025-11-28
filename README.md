# OrangeHRM Testing Project - Playwright Version

This project contains automated tests for the OrangeHRM website using **Playwright** framework.

## What Changed from Selenium to Playwright?

### Key Benefits of Playwright:
1. **Faster execution** - Playwright is generally faster than Selenium
2. **Auto-waiting** - Built-in automatic waiting for elements to be ready
3. **Better reliability** - More stable element detection and interaction
4. **Modern API** - Cleaner, more intuitive API
5. **Multiple browsers** - Easy testing across Chromium, Firefox, and WebKit
6. **Better debugging** - Built-in trace viewer and inspector

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.11+
*   pip

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/your_username_/orangehrm-testing-proj.git
    ```

2.  Install Python packages
    ```sh
    pip install -r requirements.txt
    ```

3.  Install Playwright browsers (first time only)
    ```sh
    playwright install chromium
    ```
    
    Or install all browsers:
    ```sh
    playwright install
    ```

## Running the tests

### Basic test execution:
```sh
pytest
```

### Run with visible browser (headed mode):
```sh
pytest --headed
```

### Run with specific browser:
```sh
pytest --browser chromium  # Default
pytest --browser firefox
pytest --browser webkit    # Safari engine
```

### Run tests in slow motion (for debugging):
```sh
pytest --headed --slowmo=1000
```

### Run specific test file:
```sh
pytest tests/test_login.py
```

### Run specific test:
```sh
pytest tests/test_login.py::TestLogin::test_successful_login
```

### Run with multiple workers (parallel execution):
```sh
pytest -n 4  # Requires pytest-xdist: pip install pytest-xdist
```

## Debugging

### Playwright Inspector:
```sh
PWDEBUG=1 pytest tests/test_login.py
```

### Generate trace file:
```sh
pytest --tracing on
```

## Project Structure

```
orangehrm-testing-proj/
├── pages/
│   ├── __init__.py
│   ├── base.py                 # Base page with common methods
│   ├── login_page.py           # Login page object
│   ├── dashboard_page.py       # Dashboard page object
│   ├── pim_page.py             # PIM page object
│   └── add_employee_page.py    # Add Employee page object
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures and hooks
│   ├── test_login.py           # Login test cases
│   ├── test_pim.py             # PIM test cases
│   ├── test_e2e.py             # End-to-end test cases
│   └── test_add_employee.py    # Add Employee test cases
├── utils/
│   ├── __init__.py
│   └── helpers.py              # Utility functions
├── config.py                   # Configuration settings
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

## Migration Notes

### Major Changes:

1. **No WebDriver setup required** - Playwright manages browsers automatically
2. **Selectors simplified** - Use CSS selectors and text selectors directly
3. **Auto-waiting** - No need for explicit waits in most cases
4. **Page object** - Uses `Page` object instead of `WebDriver`
5. **Built-in assertions** - Playwright has `expect()` for better assertions

### Code Comparison:

**Selenium:**
```python
from selenium.webdriver.common.by import By
element = driver.find_element(By.CSS_SELECTOR, ".button")
element.click()
```

**Playwright:**
```python
page.locator(".button").click()
```

**Selenium (with explicit wait):**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.ID, "username")))
```

**Playwright (auto-waits):**
```python
page.locator("#username").fill("text")
```

## Configuration

Configuration settings are in `config.py`:
- `BASE_URL` - Application URL
- `VALID_USERNAME` / `VALID_PASSWORD` - Test credentials
- `DEFAULT_WAIT_TIMEOUT` - Default timeout in seconds
- Directories for screenshots and reports

## Built With

*   [Playwright](https://playwright.dev/) - Modern web automation framework
*   [Pytest](https://docs.pytest.org/) - Testing framework
*   [pytest-playwright](https://github.com/microsoft/playwright-pytest) - Pytest plugin for Playwright

## Additional Resources

- [Playwright Documentation](https://playwright.dev/python/docs/intro)
- [Playwright Best Practices](https://playwright.dev/python/docs/best-practices)
- [Pytest Playwright Plugin](https://playwright.dev/python/docs/test-runners)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
