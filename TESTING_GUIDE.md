# 🚿 Testing Guide - 85%+ Coverage Target

> تست‌نویسی برای 85% coverage

---

## Backend Testing (Django)

### راه‌اندازی
```bash
cd backend

# Install test dependencies
pip install coverage django-extensions

# Create test file
touch apps/tasks/tests.py
```

### Basic Test Structure
```python
# backend/apps/tasks/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task, Comment

# ============ Model Tests ============
class TaskModelTests(TestCase):
    """Test Task model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_task(self):
        """Test creating a task"""
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
        """Test __str__ method"""
        task = Task.objects.create(
            title='Test Task',
            created_by=self.user
        )
        self.assertEqual(str(task), 'Test Task')
    
    def test_task_status_choices(self):
        """Test status field choices"""
        for status_choice in ['open', 'in_progress', 'closed']:
            task = Task.objects.create(
                title=f'Task {status_choice}',
                created_by=self.user,
                status=status_choice
            )
            self.assertEqual(task.status, status_choice)
    
    def test_task_default_priority(self):
        """Test default priority"""
        task = Task.objects.create(
            title='Test Task',
            created_by=self.user
        )
        self.assertEqual(task.priority, 1)  # Low
    
    def test_task_assigned_to_nullable(self):
        """Test assigned_to field is nullable"""
        task = Task.objects.create(
            title='Test Task',
            created_by=self.user,
            assigned_to=None
        )
        self.assertIsNone(task.assigned_to)
    
    def test_task_ordering(self):
        """Test tasks ordered by -created_at"""
        task1 = Task.objects.create(title='Task 1', created_by=self.user)
        task2 = Task.objects.create(title='Task 2', created_by=self.user)
        
        tasks = Task.objects.all()
        self.assertEqual(tasks[0].id, task2.id)  # Newest first

class CommentModelTests(TestCase):
    """Test Comment model"""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='testpass')
        self.task = Task.objects.create(
            title='Test Task',
            created_by=self.user
        )
    
    def test_create_comment(self):
        """Test creating a comment"""
        comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            content='Test comment'
        )
        self.assertEqual(comment.content, 'Test comment')
        self.assertEqual(comment.task, self.task)
    
    def test_comment_cascade_delete(self):
        """Test comment deleted when task deleted"""
        comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            content='Test'
        )
        task_id = self.task.id
        self.task.delete()
        
        self.assertFalse(Comment.objects.filter(task_id=task_id).exists())

# ============ API Tests ============
class TaskAPITests(APITestCase):
    """Test Task API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user('user1', password='pass123')
        self.user2 = User.objects.create_user('user2', password='pass123')
        
        self.task1 = Task.objects.create(
            title='Task 1',
            created_by=self.user1,
            assigned_to=self.user1
        )
        self.task2 = Task.objects.create(
            title='Task 2',
            created_by=self.user2,
            assigned_to=self.user2
        )
    
    def test_list_tasks_unauthenticated(self):
        """Unauthenticated users cannot list tasks"""
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_tasks_authenticated(self):
        """Authenticated users can list their tasks"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # user1 should only see tasks they created or are assigned to
        self.assertEqual(len(response.data), 1)
    
    def test_create_task_authenticated(self):
        """Authenticated users can create tasks"""
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'open'
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')
        self.assertEqual(response.data['created_by'], self.user1.id)
    
    def test_create_task_missing_title(self):
        """Creating task without title fails"""
        self.client.force_authenticate(user=self.user1)
        data = {'description': 'No title'}
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_task(self):
        """Task creator can update task"""
        self.client.force_authenticate(user=self.user1)
        data = {'status': 'closed', 'title': 'Updated'}
        response = self.client.patch(f'/api/tasks/{self.task1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'closed')
    
    def test_delete_task(self):
        """Task creator can delete task"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())
    
    def test_my_tasks_endpoint(self):
        """Test /api/tasks/my_tasks/ endpoint"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/tasks/my_tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.task1.id)
    
    def test_add_comment(self):
        """Test adding comment to task"""
        self.client.force_authenticate(user=self.user1)
        data = {'content': 'Test comment'}
        response = self.client.post(
            f'/api/tasks/{self.task1.id}/add_comment/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Test comment')

class TaskSerializerTests(TestCase):
    """Test serializers"""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='pass')
    
    def test_serializer_valid_data(self):
        """Test serializer with valid data"""
        from .serializers import TaskSerializer
        
        data = {
            'title': 'Test',
            'description': 'Desc',
            'status': 'open'
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_invalid_data(self):
        """Test serializer with invalid data"""
        from .serializers import TaskSerializer
        
        data = {'description': 'No title'}  # Missing required field
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
```

### راه اجرای تست‌ها
```bash
# All tests
python manage.py test

# Specific app
python manage.py test apps.tasks

# Specific test class
python manage.py test apps.tasks.tests.TaskModelTests

# Specific test method
python manage.py test apps.tasks.tests.TaskModelTests.test_create_task

# Verbose output
python manage.py test --verbosity=2

# Stop on first failure
python manage.py test --failfast
```

### Coverage Report
```bash
# Generate coverage
coverage run --source='apps' manage.py test

# Show report
coverage report

# Generate HTML report
coverage html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

---

## Frontend Testing (Vitest)

### Setup
```bash
cd frontend

# Install testing library
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

### Configure vitest

Create `frontend/vitest.config.js`:
```javascript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
    coverage: {
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.{js,jsx}'],
      exclude: ['src/test/**'],
    },
  },
});
```

Create `frontend/src/test/setup.js`:
```javascript
import '@testing-library/jest-dom';
```

Update `frontend/package.json`:
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

### Test Example

Create `frontend/src/components/__tests__/TaskList.test.jsx`:
```jsx
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import TaskList from '../TaskList';

// Mock API
vi.mock('../../services/api', () => ({
  getTasks: vi.fn(),
}));

describe('TaskList Component', () => {
  const mockTasks = [
    {
      id: 1,
      title: 'Task 1',
      description: 'Description 1',
      status: 'open',
      priority: 1,
      created_at: '2025-12-31T00:00:00Z',
    },
    {
      id: 2,
      title: 'Task 2',
      description: 'Description 2',
      status: 'in_progress',
      priority: 2,
      created_at: '2025-12-30T00:00:00Z',
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders task list', async () => {
    const { getTasks } = await import('../../services/api');
    getTasks.mockResolvedValueOnce(mockTasks);

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();
    });
  });

  it('displays empty state', async () => {
    const { getTasks } = await import('../../services/api');
    getTasks.mockResolvedValueOnce([]);

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText(/هیچ وظیفه/)).toBeInTheDocument();
    });
  });

  it('handles loading state', () => {
    const { getTasks } = await import('../../services/api');
    getTasks.mockImplementationOnce(() => new Promise(() => {}));

    render(<TaskList />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('handles error state', async () => {
    const { getTasks } = await import('../../services/api');
    getTasks.mockRejectedValueOnce(new Error('API Error'));

    render(<TaskList />);

    await waitFor(() => {
      expect(screen.getByText(/Error:/)).toBeInTheDocument();
    });
  });
});
```

### راه اجرای تست‌ها
```bash
# Run tests
npm run test

# Watch mode
npm run test -- --watch

# UI mode
npm run test:ui

# Coverage
npm run test:coverage

# Specific file
npm run test -- TaskList.test.jsx
```

---

## Coverage Targets

```
چک‌لیست:
✓ Models: 95%+
✓ Views/API: 90%+
✓ Serializers: 85%+
✓ Components: 85%+
✓ Services: 80%+
✓ Utils: 75%+

 Total: 85%+ از کل کد
```

---

## CI/CD Test Commands

Create `.github/workflows/test.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_PASSWORD: postgres
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt
          python manage.py test --verbosity=2
          coverage run --source='.' manage.py test
          coverage report

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: |
          cd frontend
          npm ci
          npm run test
          npm run test:coverage
```

---

## Tips & Best Practices

1. **Test naming**: `test_<what>_<scenario>_<expected_result>`
2. **Setup/Teardown**: Use `setUp()` and `tearDown()` methods
3. **Mocking**: Mock external services and APIs
4. **Assertions**: Use specific assertions (not just `assertTrue`)
5. **Coverage**: Aim for >85%, not 100%
6. **Test data**: Use factories or fixtures for complex data

---

**Target**: 85%+ coverage ✅
**Status**: Setup complete, ready for tests 🚀