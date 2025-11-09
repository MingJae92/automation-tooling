import pytest
from django.contrib.auth.models import User
from playwright.sync_api import Page, expect

# ---------------- Fixtures ---------------- #


@pytest.fixture
def create_users(db):
    """
    Create dummy test users in the test database.
    This keeps them isolated from your real dev DB.
    """
    mingchi = User.objects.create_user(
        username="mingchi_test", password="securepassword123")
    user_b = User.objects.create_user(
        username="user_b_test", password="pass123")
    return {"mingchi": mingchi, "user_b": user_b}


@pytest.fixture
def login(page: Page):
    """
    Reusable login helper.
    """
    def do_login(username, password):
        page.goto("http://127.0.0.1:8000/login/")
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        # Wait for redirect to dashboard
        expect(page).to_have_url(
            "http://127.0.0.1:8000/dashboard/", timeout=10000)
    return do_login

# ---------------- Tests ---------------- #


def test_login_success(page: Page, create_users):
    """
    Test valid login redirects to dashboard.
    """
    page.goto("http://127.0.0.1:8000/login/")
    page.fill('input[name="username"]', 'mingchi_test')
    page.fill('input[name="password"]', 'securepassword123')
    page.click('button[type="submit"]')
    expect(page).to_have_url("http://127.0.0.1:8000/dashboard/", timeout=10000)


def test_login_logout_flow(page: Page, create_users, login):
    """
    Test login and logout flow.
    """
    login("mingchi_test", "securepassword123")
    expect(page).to_have_url("http://127.0.0.1:8000/dashboard/")

    page.goto("http://127.0.0.1:8000/logout/")
    expect(page).to_have_url("http://127.0.0.1:8000/login/")


def test_task_management(page: Page, create_users, login):
    """
    Test adding, completing, and deleting tasks.
    """
    login("mingchi_test", "securepassword123")

    # Add a task
    page.fill('input[name="title"]', "Task 1")
    page.click('button[type="submit"]')
    page.wait_for_selector("text=Task 1")
    expect(page.locator("text=Task 1")).to_be_visible()

    # Complete the task (matches your template buttons)
    page.locator("form input[value='complete'] + button").click()
    completed_task = page.locator("text=Task 1")
    assert "text-decoration-line-through" in (
        completed_task.get_attribute("class") or "")

    # Delete the task
    page.locator("form input[value='delete'] + button").click()
    page.wait_for_timeout(500)
    expect(page.locator("text=Task 1")).not_to_be_visible()


def test_data_isolation(page: Page, create_users, login):
    """
    Ensure User B cannot see User A's tasks.
    """
    # Login as Mingchi and create a task
    login("mingchi_test", "securepassword123")
    page.fill('input[name="title"]', "Private Task")
    page.click('button[type="submit"]')
    page.wait_for_selector("text=Private Task")
    page.goto("http://127.0.0.1:8000/logout/")

    # Login as User B
    login("user_b_test", "pass123")
    assert page.locator("text=Private Task").count() == 0

    # Add a task for User B
    page.fill('input[name="title"]', "User B Task")
    page.click('button[type="submit"]')
    page.wait_for_selector("text=User B Task")
    expect(page.locator("text=User B Task")).to_be_visible()


def test_pagination(page: Page, create_users, login):
    """
    Test pagination with more than 5 tasks.
    """
    login("mingchi_test", "securepassword123")

    # Add 8 tasks
    for i in range(8):
        page.fill('input[name="title"]', f"Task {i+1}")
        page.click('button[type="submit"]')
        page.wait_for_selector(f"text=Task {i+1}")

    # Verify first 5 tasks visible
    for i in range(1, 6):
        expect(page.locator(f"text=Task {i}")).to_be_visible()

    # Click 'Next' to go to second page
    page.locator("ul.pagination li a:has-text('Next')").click()
    page.wait_for_timeout(500)

    # Verify remaining tasks
    for i in range(6, 9):
        expect(page.locator(f"text=Task {i}")).to_be_visible()
