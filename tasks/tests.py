from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task


class TaskViewsTest(TestCase):
    """Test suite for login, logout, and dashboard views."""

    def setUp(self):
        """Set up test user and client."""
        self.client = Client()
        self.username = 'testuser'
        self.password = 'securepassword123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.dashboard_url = reverse('dashboard')

    def test_login_view_get(self):
        """GET request to login should render login page."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/login.html')

    def test_login_valid_user_redirects_to_dashboard(self):
        """POST valid credentials should log in and redirect to dashboard."""
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, self.dashboard_url)

    def test_login_invalid_credentials_shows_error(self):
        """POST invalid credentials should show error message."""
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpass',
        }, follow=True)
        self.assertContains(response, "Invalid username or password.")

    def test_logout_redirects_to_login(self):
        """Logout should redirect to login page."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)

    def test_dashboard_requires_login(self):
        """Unauthenticated users should be redirected to login."""
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, f"{self.login_url}?next={self.dashboard_url}")

    def test_dashboard_loads_for_authenticated_user(self):
        """Authenticated users should see the dashboard page."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/dashboard.html')
        self.assertContains(response, self.username)

    def test_add_task_via_post(self):
        """POST action=add should create a new task."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.dashboard_url, {
            'action': 'add',
            'title': 'Test Task',
        }, follow=True)
        self.assertTrue(Task.objects.filter(title='Test Task').exists())
        self.assertContains(response, 'Task added successfully!')

    def test_complete_task_via_post(self):
        """POST action=complete should mark a task as completed."""
        self.client.login(username=self.username, password=self.password)
        task = Task.objects.create(user=self.user, title='Incomplete Task')
        response = self.client.post(self.dashboard_url, {
            'action': 'complete',
            'task_id': task.id,
        }, follow=True)
        task.refresh_from_db()
        self.assertTrue(task.completed)
        self.assertContains(response, 'Task marked as completed!')

    def test_delete_task_via_post(self):
        """POST action=delete should remove a task."""
        self.client.login(username=self.username, password=self.password)
        task = Task.objects.create(user=self.user, title='Delete Me')
        response = self.client.post(self.dashboard_url, {
            'action': 'delete',
            'task_id': task.id,
        }, follow=True)
        self.assertFalse(Task.objects.filter(id=task.id).exists())
        self.assertContains(response, 'Task deleted successfully!')

    def test_pagination_logic(self):
        """Dashboard should paginate correctly with ITEMS_PER_PAGE = 5."""
        self.client.login(username=self.username, password=self.password)
        for i in range(8):
            Task.objects.create(user=self.user, title=f'Task {i+1}')

        # Page 0 should show first 5 tasks
        response_page_0 = self.client.get(self.dashboard_url + '?page=0')
        self.assertEqual(len(response_page_0.context['tasks']), 5)

        # Page 1 should show remaining 3 tasks
        response_page_1 = self.client.get(self.dashboard_url + '?page=1')
        self.assertEqual(len(response_page_1.context['tasks']), 3)
