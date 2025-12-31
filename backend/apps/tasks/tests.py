from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task, TaskComment
from datetime import datetime, timedelta
from django.utils import timezone


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_create_task(self):
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            created_by=self.user,
            status='open'
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.status, 'open')
        self.assertEqual(task.created_by, self.user)
    
    def test_task_str(self):
        task = Task.objects.create(
            title='Test Task',
            created_by=self.user
        )
        self.assertEqual(str(task), 'Test Task')
    
    def test_mark_completed(self):
        task = Task.objects.create(
            title='Test Task',
            created_by=self.user,
            status='open'
        )
        task.mark_completed()
        self.assertEqual(task.status, 'closed')
        self.assertIsNotNone(task.completed_at)


class TaskAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_list_tasks_authenticated(self):
        Task.objects.create(
            title='Task 1',
            created_by=self.user
        )
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_task_authenticated(self):
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'open',
            'priority': 'medium'
        }
        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')
    
    def test_update_task(self):
        task = Task.objects.create(
            title='Original Task',
            created_by=self.user,
            status='open'
        )
        data = {'status': 'in_progress'}
        response = self.client.patch(f'/api/tasks/{task.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, 'in_progress')
    
    def test_delete_task(self):
        task = Task.objects.create(
            title='Task to Delete',
            created_by=self.user
        )
        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
    
    def test_mark_completed_action(self):
        task = Task.objects.create(
            title='Task to Complete',
            created_by=self.user,
            status='open'
        )
        response = self.client.post(f'/api/tasks/{task.id}/mark_completed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, 'closed')
    
    def test_add_comment(self):
        task = Task.objects.create(
            title='Task with Comment',
            created_by=self.user
        )
        data = {'content': 'This is a comment'}
        response = self.client.post(f'/api/tasks/{task.id}/add_comment/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskComment.objects.count(), 1)
    
    def test_unauthenticated_access_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_filter_by_status(self):
        Task.objects.create(title='Open Task', created_by=self.user, status='open')
        Task.objects.create(title='Closed Task', created_by=self.user, status='closed')
        
        response = self.client.get('/api/tasks/?status=open')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Open Task')


class TaskCommentTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Task',
            created_by=self.user
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_comment(self):
        comment = TaskComment.objects.create(
            task=self.task,
            author=self.user,
            content='Test Comment'
        )
        self.assertEqual(comment.content, 'Test Comment')
        self.assertEqual(comment.task, self.task)
