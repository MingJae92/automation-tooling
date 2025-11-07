# 🧪 QA Automation Challenge: Django Todo App

## Overview

You are provided with a small Django app that implements a basic "To-Do List" feature.

Your task is to write automated tests using **Playwright** or **Selenium** to validate the application's behavior.

⚠️ **The app may contain one or more bugs.**

---

## 🎯 Your Objectives

1. **Set up the app** and ensure it runs locally.

2. **Write end-to-end UI automation** that covers:
   - User login
   - Adding a new task
   - Marking a task as completed
   - Deleting a task

3. **Write one or more tests that verify correct data isolation between users.**
   - Example: User A's tasks should **not** appear for User B.

4. **If you notice any bugs**, describe them in your test output or notes.

5. **Optionally: Validate pagination correctness** (no skipped or missing tasks).

---

## 🧰 Tech Requirements

- Use **Playwright (Python)** or **Selenium (Python)** for automation.
- Python 3.8 or higher recommended.
- Tests should be runnable with a simple command (e.g., `./manage.py test`,`pytest` or `python -m unittest`).

---

## 🚀 Setup Instructions

### 1. Clone or Download the Project

```bash
cd todo_app
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Create Test Users

Create at least two users for testing data isolation:

```bash
python manage.py createsuperuser
```

Follow the prompts to create a user (e.g., username: `user1`, password: `testpass123`).

Repeat to create a second user (e.g., username: `user2`, password: `testpass123`).

Alternatively, you can create users programmatically in your test setup:

```python
from django.contrib.auth.models import User

User.objects.create_user(username='user1', password='testpass123')
User.objects.create_user(username='user2', password='testpass123')
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The app should now be accessible at: **http://127.0.0.1:8000/**

---

## 📋 Application Features

### Login Page (`/login/`)
- Users can log in with their username and password.
- After successful login, users are redirected to the dashboard.

### Dashboard Page (`/dashboard/`)
- Users can:
  - **Add a new task** via an input form
  - **Mark a task as completed** (✓ button)
  - **Delete a task** (🗑️ button)
- Tasks are displayed in a paginated list (5 tasks per page)
- Each task shows:
  - Task title
  - Creator's username
  - Creation timestamp
  - Completion status

### Logout
- Users can log out via the navigation bar.

---

## 🧪 Testing Guidelines

### Test Coverage Expectations

Your automated tests should cover:

1. **Authentication Flow**
   - Login with valid credentials
   - Redirect to dashboard after login
   - Logout functionality

2. **Task Management (important to use browser automation here (playwrite or selenium etc))**
   - Adding a new task
   - Verifying the task appears in the list
   - Marking a task as completed
   - Deleting a task

3. **Data Isolation**
   - Create tasks as User A
   - Log out and log in as User B
   - Verify User B **cannot see** User A's tasks
   - Verify User B can only see their own tasks

4. **Pagination (Optional Bonus)**
   - Create more than 5 tasks
   - Navigate through pages
   - Verify no tasks are skipped or duplicated

### Example Test Structure

```python
def test_data_isolation():
    # Login as user1
    # Create 3 tasks
    # Logout
    
    # Login as user2
    # Verify dashboard shows 0 tasks (or only user2's tasks)
    # user1's tasks should NOT be visible
```

### Setting Up Your Test Framework

#### Option A: Playwright (Python)

```bash
pip install playwright pytest-playwright
playwright install
```

Example test:

```python
from playwright.sync_api import Page, expect

def test_login(page: Page):
    page.goto("http://127.0.0.1:8000/login/")
    page.fill('input[name="username"]', 'user1')
    page.fill('input[name="password"]', 'testpass123')
    page.click('button[type="submit"]')
    expect(page).to_have_url("http://127.0.0.1:8000/dashboard/")
```

#### Option B: Selenium (Python)

```bash
pip install selenium pytest
```

Example test:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_login():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:8000/login/")
    driver.find_element(By.NAME, "username").send_keys("user1")
    driver.find_element(By.NAME, "password").send_keys("testpass123")
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert "dashboard" in driver.current_url
    driver.quit()
```
#### Option C: Whatever you want
---

## 🕒 Time Expectation

- **~ 1 hours total** (including setup, test writing, and bug discovery)

---

## 💡 Bonus Points

- **Fix the bugs** you discover and document your fixes
- Write clear, maintainable test code with best practices
- Measure Test Coverage

---

## 📁 Project Structure

```
todo_app/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── todo_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── tasks/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── tests.py
    └── templates/
        └── tasks/
            ├── base.html
            ├── login.html
            └── dashboard.html
```

---

## 🐛 Bug Hints

If you're stuck, here are some areas to investigate:

1. **Data Isolation**: Are tasks properly filtered by user?
2. **Pagination Logic**: Are all tasks displayed correctly when navigating pages?
3. **Edge Cases**: What happens with empty task lists? Invalid page numbers?

---

## 📝 Submission Instructions

Create a public github repository with :

1. Your test code (Python files)
2. Instructions to run your tests (README or comments)
3. A brief report of any bugs found

---

## 📞 Questions?

If you have questions about the challenge, please reach out to the hiring team.

Good luck! 🚀
