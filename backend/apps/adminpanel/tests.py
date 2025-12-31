from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import AdminLog, NotificationTemplate

User = get_user_model()

class AdminLogTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
    
    def test_admin_overview(self):
        response = self.client.get('/api/admin/admin/overview/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('tasks', response.data)
    
    def test_get_users_list(self):
        response = self.client.get('/api/admin/admin/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_access_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/admin/admin/overview/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_non_admin_access_denied(self):
        normal_user = User.objects.create_user(
            email='normaluser@example.com',
            username='normaluser',
            password='pass123'
        )
        self.client.force_authenticate(user=normal_user)
        response = self.client.get('/api/admin/admin/overview/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NotificationTemplateTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        
        self.template = NotificationTemplate.objects.create(
            title='Test Template',
            subject='Test Subject',
            body='Test Body'
        )
    
    def test_create_template(self):
        data = {
            'title': 'New Template',
            'subject': 'New Subject',
            'body': 'New Body'
        }
        response = self.client.post('/api/admin/notification-templates/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_templates(self):
        response = self.client.get('/api/admin/notification-templates/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_send_notification(self):
        data = {
            'user_ids': [],
            'template_id': self.template.id
        }
        response = self.client.post('/api/admin/notification-templates/send_notification/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
