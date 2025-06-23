from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import yaml
import os


class LoginPage:
    """Page Object Model for Login Page"""

    # Locators
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.ID, "flash")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Logout')]")
    SECURE_AREA_HEADER = (By.TAG_NAME, "h2")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from config.yaml"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    @allure.step("Navigate to login page")
    def navigate_to_login_page(self):
        """Navigate to the login page"""
        self.driver.get(self.config['login_url'])
        # Wait for page to load
        self.wait.until(EC.presence_of_element_located(self.USERNAME_FIELD))
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="login_page_loaded",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Enter username: {username}")
    def enter_username(self, username):
        """Enter username in the username field"""
        username_field = self.wait.until(EC.element_to_be_clickable(self.USERNAME_FIELD))
        username_field.clear()
        username_field.send_keys(username)

    @allure.step("Enter password")
    def enter_password(self, password):
        """Enter password in the password field"""
        password_field = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(password)

    @allure.step("Click login button")
    def click_login_button(self):
        """Click the login button"""
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_button.click()

    @allure.step("Perform login with credentials")
    def login(self, username, password):
        """Perform complete login action"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

        # Take screenshot after login attempt
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="after_login_attempt",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Check if login is successful")
    def is_login_successful(self):
        """Check if login was successful by verifying URL and page elements"""
        try:
            # Wait for URL to change to secure area
            WebDriverWait(self.driver, 10).until(
                lambda driver: self.config['secure_area_url'] in driver.current_url
            )

            # Check for secure area elements
            secure_header = self.wait.until(EC.presence_of_element_located(self.SECURE_AREA_HEADER))
            logout_button = self.wait.until(EC.presence_of_element_located(self.LOGOUT_BUTTON))

            return True
        except TimeoutException:
            return False

    @allure.step("Get success message")
    def get_success_message(self):
        """Get the success message text"""
        try:
            success_element = self.wait.until(EC.presence_of_element_located(self.SUCCESS_MESSAGE))
            return success_element.text
        except TimeoutException:
            return None

    @allure.step("Get error message")
    def get_error_message(self):
        """Get the error message text"""
        try:
            error_element = self.wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
            return error_element.text
        except TimeoutException:
            return None

    @allure.step("Check if user is on login page")
    def is_on_login_page(self):
        """Check if currently on login page"""
        return self.config['login_url'] in self.driver.current_url

    @allure.step("Check if user is on secure area")
    def is_on_secure_area(self):
        """Check if currently on secure area"""
        return self.config['secure_area_url'] in self.driver.current_url

    @allure.step("Logout from secure area")
    def logout(self):
        """Logout from the secure area"""
        if self.is_on_secure_area():
            logout_button = self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON))
            logout_button.click()

            # Wait for redirect to login page
            self.wait.until(
                lambda driver: self.config['login_url'] in driver.current_url
            )

    @allure.step("Get current page title")
    def get_page_title(self):
        """Get the current page title"""
        return self.driver.title

    @allure.step("Get current URL")
    def get_current_url(self):
        """Get the current URL"""
        return self.driver.current_url