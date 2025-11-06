# Sample Test Structure (Reference for Candidates)
# This is an example of how you might structure your tests
# Feel free to use Playwright or Selenium based on your preference

"""
Example using Playwright:

To run these tests:
1. pip install playwright pytest-playwright
2. playwright install
3. pytest test_example.py

"""

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function")
def browser_context(page: Page):
    """Setup: Navigate to login page before each test"""
    page.goto("http://127.0.0.1:8000/login/")
    yield page


def test_login_success(browser_context: Page):
    """Test successful login redirects to dashboard"""
    page = browser_context
    
    # TODO: Fill in login credentials
    page.fill('input[name="username"]', 'your_username')
    page.fill('input[name="password"]', 'your_password')
    
    # TODO: Submit login form
    page.click('button[type="submit"]')
    
    # TODO: Assert redirect to dashboard
    expect(page).to_have_url("http://127.0.0.1:8000/dashboard/")


def test_add_task(browser_context: Page):
    """Test adding a new task"""
    # TODO: Login first
    # TODO: Add a task
    # TODO: Verify task appears in the list
    pass


def test_complete_task(browser_context: Page):
    """Test marking a task as completed"""
    # TODO: Login and create a task
    # TODO: Click complete button
    # TODO: Verify task is marked as completed
    pass


def test_delete_task(browser_context: Page):
    """Test deleting a task"""
    # TODO: Login and create a task
    # TODO: Click delete button
    # TODO: Verify task is removed from list
    pass


def test_data_isolation():
    """
    IMPORTANT TEST: Verify users can only see their own tasks
    
    Steps:
    1. Login as user1
    2. Create several tasks
    3. Logout
    4. Login as user2
    5. Verify user2 CANNOT see user1's tasks
    6. Create user2's own tasks
    7. Verify only user2's tasks are visible
    """
    # TODO: Implement this critical test
    pass


def test_pagination():
    """
    BONUS TEST: Verify pagination works correctly
    
    Steps:
    1. Login
    2. Create 15+ tasks
    3. Navigate through pages
    4. Verify all tasks appear exactly once (no skips or duplicates)
    """
    # TODO: Implement pagination test
    pass


# For Selenium users, here's an equivalent example:
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_login_selenium():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:8000/login/")
    
    driver.find_element(By.NAME, "username").send_keys("your_username")
    driver.find_element(By.NAME, "password").send_keys("your_password")
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    
    assert "dashboard" in driver.current_url
    driver.quit()
"""
