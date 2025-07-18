This Repo shows how to create Selenium Python Test Automation Framework in 5 minutes using claude.ai
---------------------------------------------------------------------------------------------------------
Goto Claude.ai and Use AI Prompt and check the awesome code generated :

for https://practice.expandtesting.com/login
Create a Selenium Python Test Automation Framework that includes the following:
Technologies & Libraries:

    Selenium for browser automation
    Pytest for test execution
    Page Object Model (POM) for maintainability
    Allure Report for test reporting

Project Structure & Implementation:

    Project Initialization:
        Create a well-structured Python framework using Pytest and Selenium.
        Implement the Page Object Model (POM) pattern.
        Integrate Allure Reports for test execution reports.

    Folder & File Structure:

selenium-python-framework/
├── tests/
│   ├── test_login.py  
├── pages/
│   ├── login_page.py  
├── config/
│   ├── config.yaml  # Configuration file (URL, credentials, etc.)
├── utils/
│   ├── browser_setup.py  # WebDriver initialization  
├── reports/
├── requirements.txt
├── pytest.ini
├── README.md

Sample Login Test Implementation:

    login_page.py: Create a class for login page interactions.
    test_login.py: Write a Pytest test case to verify login functionality.

Allure Report Integration:

    Ensure Allure Report is properly set up and can generate reports after execution.

Guide for Users:

    README.md should include instructions on:
        How to install dependencies (pip install -r requirements.txt)
        How to execute test cases (pytest --alluredir=reports/)
        How to view Allure Reports (allure serve reports/)
        How to add new test cases
-----------------------------------------------------------------------------------------------------------------------------------



Selenium Python Test Automation Framework
A comprehensive test automation framework for login functionality testing using Selenium WebDriver, Pytest, and Page Object Model (POM) design pattern.

🚀 Features
Selenium WebDriver for browser automation
Pytest for test execution and fixtures
Page Object Model (POM) design pattern
Allure Reports for detailed test reporting
YAML Configuration for test data management
Cross-browser support (Chrome, Firefox)
Screenshot on failure functionality
Parameterized tests for data-driven testing

📁 Project Structure
selenium-python-framework/
├── tests/
│   └── test_login.py           # Login test cases
├── pages/
│   └── login_page.py           # Login page POM
├── config/
│   └── config.yaml             # Configuration and test data
├── utils/
│   └── browser_setup.py        # WebDriver setup and teardown
├── reports/                    # Allure report output directory
├── conftest.py                 # Pytest fixtures and configuration
├── pytest.ini                 # Pytest configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation

🛠️ Installation
Prerequisites
Python 3.8 or higher
pip (Python package installer)
Chrome or Firefox browser
Setup
Clone the repository:
bash
git clone <repository-url>
cd selenium-python-framework
Create a virtual environment (recommended):
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
bash
pip install -r requirements.txt
Install Allure (for report generation): On macOS:
bash
brew install allure
On Windows:
bash
# Download from https://github.com/allure-framework/allure2/releases
# Add to PATH
On Linux:
bash
sudo apt-get install allure
🧪 Running Tests
Basic Test Execution
bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_login.py

# Run specific test method
pytest tests/test_login.py::TestLogin::test_successful_login

# Run tests with verbose output
pytest -v
Generate Allure Reports
bash
# Run tests and generate Allure results
pytest --alluredir=reports/allure-results

# Generate and serve Allure report
allure serve reports/allure-results

# Generate static Allure report
allure generate reports/allure-results -o reports/allure-report --clean
Run Tests with Different Browsers
Modify the config/config.yaml file to change the browser:

yaml
browser:
  default: "chrome"  # or "firefox"
  headless: false    # Set to true for headless mode
Run Tests in Headless Mode
bash
# Set headless mode in config.yaml or override via environment
pytest --alluredir=reports/allure-results
📊 Test Reports
Allure Reports
The framework generates comprehensive Allure reports with:

Test execution summary
Detailed test steps
Screenshots on failure
Test history and trends
Categorized test results
Viewing Reports
bash
# Serve interactive report
allure serve reports/allure-results

# Open in browser at: http://localhost:port
🔧 Configuration
config/config.yaml
yaml
base_url: "https://practice.expandtesting.com"
login_url: "https://practice.expandtesting.com/login"
secure_area_url: "https://practice.expandtesting.com/secure"

credentials:
  valid:
    username: "practice"
    password: "SuperSecretPassword!"
  invalid:
    username: "invalid_user"
    password: "invalid_password"

browser:
  default: "chrome"
  headless: false
  implicit_wait: 10
  page_load_timeout: 30
📝 Test Cases
The framework includes the following test scenarios:

✅ Positive Test Cases
test_successful_login: Validates successful login with valid credentials
test_login_with_special_characters: Tests login with special characters
❌ Negative Test Cases
test_invalid_login: Validates login failure with invalid credentials
test_empty_username: Tests login with empty username
test_empty_password: Tests login with empty password
🏗️ Adding New Tests
1. Create a New Test File
python
# tests/test_new_feature.py
import pytest
import allure
from pages.login_page import LoginPage

class TestNewFeature:
    
    @allure.epic("New Feature")
    @allure.feature("Feature Name")
    @allure.story("User Story")
    @allure.title("Test Title")
    def test_new_functionality(self, driver):
        # Test implementation
        pass
2. Create a New Page Object
python
# pages/new_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class NewPage:
    
    # Locators
    ELEMENT_LOCATOR = (By.ID, "element-id")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    @allure.step("Perform action")
    def perform_action(self):
        element = self.wait.until(EC.element_to_be_clickable(self.ELEMENT_LOCATOR))
        element.click()
3. Update Configuration
Add new test data or URLs to config/config.yaml:

yaml
new_feature:
  url: "https://example.com/new-feature"
  test_data:
    value1: "test_value"
    value2: "another_value"
🐛 Debugging and Troubleshooting
Common Issues
WebDriver not found:
The framework uses webdriver-manager to automatically download drivers
Ensure internet connection is available during first run
Element not found:
Check if locators are correct
Verify element is visible and clickable
Increase wait times if necessary
Test failures:
Check screenshots in Allure reports
Review browser console logs
Verify test data and configuration
Debug Mode
bash
# Run with debug output
pytest -v -s --tb=long

# Run single test with debug
pytest -v -s tests/test_login.py::TestLogin::test_successful_login
📈 Continuous Integration
GitHub Actions Example
yaml
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: pytest --alluredir=reports/allure-results
    - name: Generate Allure Report
      run: allure generate reports/allure-results -o reports/allure-report
🤝 Contributing
Fork the repository
Create a feature branch (git checkout -b feature/new-feature)
Commit your changes (git commit -am 'Add new feature')
Push to the branch (git push origin feature/new-feature)
Create a Pull Request


Create an issue in the repository
Review the troubleshooting section
Check Allure reports for detailed error information
Happy Testing! 🎉

#   A u t o m a t i o n _ f r a m e w o r k _ i n _ 5 _ m i n u t e s 
 
 
