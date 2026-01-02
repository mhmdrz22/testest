"""
Tests for Admin Panel functionality
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AdminPanelAccessTestCase(TestCase):
    """Test access control for admin panel"""
    
    def setUp(self):
        """Set up test client and users"""
        self.client = APIClient()
        
        # Create regular user
        self.user = User.objects.create_user(
            email='user@test.com',
            username='testuser',
            password='testpass123'
        )
        
        # Create admin user
        self.admin = User.objects.create_user(
            email='admin@test.com',
            username='admin',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
    
    def test_admin_overview_requires_authentication(self):
        """Test that admin overview requires authentication"""
        response = self.client.get('/api/admin/overview/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_admin_overview_requires_staff_permission(self):
        """Test that regular users cannot access admin overview"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/admin/overview/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_overview_accessible_by_staff(self):
        """Test that staff users can access admin overview"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/admin/overview/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_admin_notify_requires_staff_permission(self):
        """Test that regular users cannot send notifications"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/admin/notify/', {
            'recipients': ['user@test.com'],
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_notify_validates_recipients(self):
        """Test that notify endpoint validates recipient emails"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/admin/notify/', {
            'recipients': ['nonexistent@test.com'],
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_admin_notify_success(self):
        """Test successful email notification"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/admin/notify/', {
            'recipients': ['user@test.com'],
            'message': '# Test\n\nThis is a test'
        })
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('job_id', response.data)
        self.assertIn('recipients_count', response.data)
        self.assertEqual(response.data['recipients_count'], 1)


class AdminOverviewDataTestCase(TestCase):
    """Test admin overview data correctness"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email='admin@test.com',
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin)
    
    def test_admin_overview_returns_all_users(self):
        """Test that overview returns all users"""
        # Create additional users
        User.objects.create_user(
            email='user1@test.com',
            username='user1',
            password='pass123'
        )
        User.objects.create_user(
            email='user2@test.com',
            username='user2',
            password='pass123'
        )
        
        response = self.client.get('/api/admin/overview/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # admin + 2 users
    
    def test_admin_overview_includes_task_counts(self):
        """Test that overview includes open_tasks and total_tasks"""
        response = self.client.get('/api/admin/overview/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if len(response.data) > 0:
            user_data = response.data[0]
            self.assertIn('open_tasks', user_data)
            self.assertIn('total_tasks', user_data)
            self.assertIn('email', user_data)
            self.assertIn('username', user_data)
