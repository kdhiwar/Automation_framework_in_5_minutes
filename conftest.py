import pytest
import allure
from utils.browser_setup import BrowserSetup


@pytest.fixture(scope="session")
def browser_setup():
    """Session-wide browser setup fixture"""
    browser = BrowserSetup()
    yield browser
    browser.quit_driver()


@pytest.fixture(scope="function")
def driver(browser_setup):
    """Function-scoped driver fixture"""
    driver = browser_setup.get_driver()
    yield driver

    # Take screenshot on test failure
    if hasattr(pytest, "current_test_failed") and pytest.current_test_failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG
        )

    # Clean up
    browser_setup.quit_driver()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot on failure"""
    outcome = yield
    rep = outcome.get_result()

    # Set a flag on the pytest object to indicate test failure
    if rep.when == "call" and rep.failed:
        pytest.current_test_failed = True
    else:
        pytest.current_test_failed = False