# import pytest
# from playwright.sync_api import Page, expect
# import time

# BASE_URL = "http://127.0.0.1:8000"

# # ---------- Helper Functions ----------
# def login(page: Page, username: str, password: str):
#     page.goto(f"{BASE_URL}/login/")
#     page.fill('input[name="username"]', username)
#     page.fill('input[name="password"]', password)
#     page.click('button[type="submit"]')
#     expect(page).to_have_url(f"{BASE_URL}/dashboard/")

# def logout(page: Page):
#     page.click('text=Logout')
#     expect(page).to_have_url(f"{BASE_URL}/login/")

# def add_task(page: Page, task_title: str):
#     page.fill('input[name="task_title"]', task_title)
#     page.click('button[type="submit"]')
#     expect(page.locator("ul li")).to_contain_text(task_title)

# def complete_task(page: Page, task_title: str):
#     task_item = page.locator(f"li:has-text('{task_title}')")
#     task_item.locator('button:has-text("✓")').click()
#     # Optional: Verify completed task has class or strikethrough
#     expect(task_item).to_have_class(re.compile("completed|done"))

# def delete_task(page: Page, task_title: str):
#     task_item = page.locator(f"li:has-text('{task_title}')")
#     task_item.locator('button:has-text("🗑️")').click()
#     expect(page.locator(f"li:has-text('{task_title}')")).to_have_count(0)

# # ---------- TEST CASES ----------
# def test_login_logout(page: Page):
#     login(page, "user1", "testpass123")
#     logout(page)

# def test_add_complete_delete_task(page: Page):
#     login(page, "user1", "testpass123")
#     task_name = "Test Task 1"
    
#     add_task(page, task_name)
#     complete_task(page, task_name)
#     delete_task(page, task_name)
    
#     logout(page)

# def test_data_isolation(page: Page):
#     # User A
#     login(page, "user1", "testpass123")
#     add_task(page, "UserA Task 1")
#     add_task(page, "UserA Task 2")
#     logout(page)
    
#     # User B
#     login(page, "user2", "testpass123")
#     expect(page.locator("ul li")).to_have_count(0)  # User A tasks should not appear
#     add_task(page, "UserB Task 1")
#     logout(page)
    
#     # Verify User A only sees their tasks
#     login(page, "user1", "testpass123")
#     tasks = page.locator("ul li")
#     expect(tasks).to_have_count(2)
#     expect(tasks).to_contain_text("UserA Task 1")
#     expect(tasks).to_contain_text("UserA Task 2")
#     logout(page)

# def test_pagination(page: Page):
#     login(page, "user1", "testpass123")
#     # Add 7 tasks to test 5-task pagination
#     for i in range(7):
#         add_task(page, f"Paginate Task {i+1}")
    
#     # Page 1 should have 5 tasks
#     tasks_page1 = page.locator("ul li")
#     expect(tasks_page1).to_have_count(5)
    
#     # Click "Next" for page 2
#     if page.locator("text=Next").count() > 0:
#         page.click("text=Next")
#     tasks_page2 = page.locator("ul li")
#     expect(tasks_page2).to_have_count(2)
    
#     # Cleanup: delete tasks
#     page.goto(f"{BASE_URL}/dashboard/")
#     for i in range(7):
#         delete_task(page, f"Paginate Task {i+1}")
    
#     logout(page)
