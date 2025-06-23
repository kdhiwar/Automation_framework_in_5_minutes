import pytest
import allure
import yaml
import os
from pages.login_page import LoginPage


class TestLogin:
    """Test class for login functionality"""

    @classmethod
    def setup_class(cls):
        """Load test configuration"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            cls.config = yaml.safe_load(file)

    @allure.epic("Authentication")
    @allure.feature("Login")
    @allure.story("Valid Login")
    @allure.title("Test successful login with valid credentials")
    @allure.description("This test verifies that a user can successfully log in with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver):
        """Test successful login with valid credentials"""

        # Arrange
        login_page = LoginPage(driver)
        valid_username = self.config['credentials']['valid']['username']
        valid_password = self.config['credentials']['valid']['password']

        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
            assert login_page.is_on_login_page(), "User should be on login page"

        with allure.step("Perform login with valid credentials"):
            login_page.login(valid_username, valid_password)

        with allure.step("Verify successful login"):
            assert login_page.is_login_successful(), "Login should be successful"
            assert login_page.is_on_secure_area(), "User should be redirected to secure area"

        with allure.step("Verify page title"):
            page_title = login_page.get_page_title()
            assert "Secure Area" in page_title, f"Page title should contain 'Secure Area', but got: {page_title}"

        # Cleanup - logout
        with allure.step("Logout from secure area"):
            login_page.logout()
            assert login_page.is_on_login_page(), "User should be back on login page after logout"

    @allure.epic("Authentication")
    @allure.feature("Login")
    @allure.story("Invalid Login")
    @allure.title("Test login failure with invalid credentials")
    @allure.description(
        "This test verifies that login fails with invalid credentials and shows appropriate error message")
    @allure.severity(allure.severity_level.HIGH)
    def test_invalid_login(self, driver):
        """Test login failure with invalid credentials"""

        # Arrange
        login_page = LoginPage(driver)
        invalid_username = self.config['credentials']['invalid']['username']
        invalid_password = self.config['credentials']['invalid']['password']

        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()
            assert login_page.is_on_login_page(), "User should be on login page"

        with allure.step("Attempt login with invalid credentials"):
            login_page.login(invalid_username, invalid_password)

        with allure.step("Verify login failure"):
            assert not login_page.is_login_successful(), "Login should fail with invalid credentials"
            assert login_page.is_on_login_page(), "User should remain on login page"

        with allure.step("Verify error message"):
            error_message = login_page.get_error_message()
            assert error_message is not None, "Error message should be displayed"
            assert "invalid" in error_message.lower(), f"Error message should mention invalid credentials, got: {error_message}"

    @allure.epic("Authentication")
    @allure.feature("Login")
    @allure.story("Empty Credentials")
    @allure.title("Test login with empty username")
    @allure.description("This test verifies that login fails when username is empty")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_empty_username(self, driver):
        """Test login with empty username"""

        # Arrange
        login_page = LoginPage(driver)
        valid_password = self.config['credentials']['valid']['password']

        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()

        with allure.step("Attempt login with empty username"):
            login_page.login("", valid_password)

        with allure.step("Verify login failure"):
            assert not login_page.is_login_successful(), "Login should fail with empty username"
            assert login_page.is_on_login_page(), "User should remain on login page"

    @allure.epic("Authentication")
    @allure.feature("Login")
    @allure.story("Empty Credentials")
    @allure.title("Test login with empty password")
    @allure.description("This test verifies that login fails when password is empty")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_empty_password(self, driver):
        """Test login with empty password"""

        # Arrange
        login_page = LoginPage(driver)
        valid_username = self.config['credentials']['valid']['username']

        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()

        with allure.step("Attempt login with empty password"):
            login_page.login(valid_username, "")

        with allure.step("Verify login failure"):
            assert not login_page.is_login_successful(), "Login should fail with empty password"
            assert login_page.is_on_login_page(), "User should remain on login page"

    @allure.epic("Authentication")
    @allure.feature("Login")
    @allure.story("Edge Cases")
    @allure.title("Test login with special characters in credentials")
    @allure.description("This test verifies login behavior with special characters")
    @allure.severity(allure.severity_level.LOW)
    @pytest.mark.parametrize("username,password", [
        ("user@domain.com", "password123"),
        ("user123!", "@#$%^&*()"),
        ("   practice   ", "SuperSecretPassword!"),  # with spaces
    ])
    def test_login_with_special_characters(self, driver, username, password):
        """Test login with various special characters"""

        # Arrange
        login_page = LoginPage(driver)

        with allure.step(f"Navigate to login page"):
            login_page.navigate_to_login_page()

        with allure.step(f"Attempt login with username: '{username}' and password: '[HIDDEN]'"):
            login_page.login(username, password)

        with allure.step("Verify login result"):
            # Only the valid credentials (even with spaces) should work
            if username.strip() == self.config['credentials']['valid']['username'] and password == \
                    self.config['credentials']['valid']['password']:
                assert login_page.is_login_successful(), "Login should succeed with valid credentials"
                login_page.logout()  # Cleanup
            else:
                assert not login_page.is_login_successful(), "Login should fail with invalid credentials"