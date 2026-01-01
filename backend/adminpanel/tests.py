from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import Task
from unittest.mock import patch, MagicMock

User = get_user_model()


class AdminOverviewTests(APITestCase):
    def setUp(self):
        # Create admin user
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123"
        )
        # Create regular user
        self.user = User.objects.create_user(
            email="user@example.com",
            password="userpass123"
        )
        self.overview_url = reverse("admin-overview")

    def test_admin_can_access_overview(self):
        """
        Test that admin user can access the overview endpoint.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.overview_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("users", response.data)

    def test_regular_user_cannot_access_overview(self):
        """
        Test that regular user cannot access admin overview.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.overview_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_access_overview(self):
        """
        Test that unauthenticated users cannot access overview.
        """
        response = self.client.get(self.overview_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminNotifyTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123"
        )
        self.user1 = User.objects.create_user(
            email="user1@example.com",
            password="pass123"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com",
            password="pass123"
        )
        self.notify_url = reverse("admin-notify")

    @patch('adminpanel.views.send_admin_notification_email.delay')
    def test_admin_can_send_notification(self, mock_celery_task):
        """
        Test that admin can send notification to existing users.
        Uses mock to avoid Celery/Redis connection issues in tests.
        """
        # Mock the Celery task to avoid Redis connection
        mock_celery_task.return_value = MagicMock(id='test-job-id')
        
        self.client.force_authenticate(user=self.admin)
        data = {
            "recipients": ["user1@example.com", "user2@example.com"],
            "message": "Test notification message"
        }
        response = self.client.post(self.notify_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn("job_id", response.data)
        self.assertEqual(response.data["recipients_count"], 2)
        
        # Verify the Celery task was called with correct arguments
        mock_celery_task.assert_called_once()
        call_args = mock_celery_task.call_args[0]
        self.assertEqual(len(call_args[0]), 2)  # 2 recipients
        self.assertEqual(call_args[1], "Test notification message")

    def test_notify_with_invalid_email(self):
        """
        Test notification with non-existing email addresses.
        """
        self.client.force_authenticate(user=self.admin)
        data = {
            "recipients": ["nonexistent@example.com"],
            "message": "Test message"
        }
        response = self.client.post(self.notify_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
