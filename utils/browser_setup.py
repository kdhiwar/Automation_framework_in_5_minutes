from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import yaml
import os
import allure


class BrowserSetup:
    """Browser setup and configuration class"""

    def __init__(self):
        self.driver = None
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from config.yaml"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    @allure.step("Initialize browser driver")
    def get_driver(self, browser_name=None):
        """Initialize and return WebDriver instance"""
        browser = browser_name or self.config['browser']['default']
        headless = self.config['browser']['headless']

        if browser.lower() == 'chrome':
            self.driver = self._setup_chrome(headless)
        elif browser.lower() == 'firefox':
            self.driver = self._setup_firefox(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        # Set timeouts
        self.driver.implicitly_wait(self.config['browser']['implicit_wait'])
        self.driver.set_page_load_timeout(self.config['browser']['page_load_timeout'])

        # Maximize window
        self.driver.maximize_window()

        return self.driver

    def _setup_chrome(self, headless=False):
        """Setup Chrome driver with options"""
        chrome_options = Options()

        if headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def _setup_firefox(self, headless=False):
        """Setup Firefox driver with options"""
        firefox_options = FirefoxOptions()

        if headless:
            firefox_options.add_argument('--headless')

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=firefox_options)

    @allure.step("Close browser")
    def quit_driver(self):
        """Quit the WebDriver instance"""
        if self.driver:
            self.driver.quit()
            self.driver = None