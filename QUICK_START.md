# 🚀 Quick Start - First 2 Hours

> اچ به شرایط ارتقاء در این 2 ساعت

---

## ⏳ Hour 1: Backend Setup

### روز 1.1: Clone + Environment (10 min)
```bash
git clone https://github.com/mhmdrz22/testest.git
cd testest/backend

# Copy environment
cp .env.example .env
# Edit .env: DEBUG=True, DB_ENGINE=django.db.backends.sqlite3 (local)

# Virtual env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install --upgrade pip
pip install -r requirements.txt
```

### روز 1.2: Create Django Project (5 min)
```bash
# Check if config exists
ls config/

# If NOT, create:
django-admin startproject config .

# If YES, check settings.py exists
ls config/settings.py
```

### روز 1.3: Create Tasks App (5 min)
```bash
python manage.py startapp tasks apps/tasks

# Add to config/settings.py INSTALLED_APPS:
# 'rest_framework',
# 'corsheaders',
# 'apps.tasks',
```

### روز 1.4: Models (20 min)

Create `backend/apps/tasks/models.py`:
```python
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('open', 'باز'),
        ('in_progress', 'در حال انجام'),
        ('closed', 'بسته شده'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.IntegerField(default=1, choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by', 'status']),
            models.Index(fields=['assigned_to', 'status']),
        ]

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comment by {self.author} on {self.task}'
    
    class Meta:
        ordering = ['-created_at']
```

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate
```

### روز 1.5: Serializers + Views (20 min)

Create `backend/apps/tasks/serializers.py`:
```python
from rest_framework import serializers
from .models import Task, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'task', 'content', 'author', 'author_username', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True, allow_null=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'created_by', 'created_by_username',
                  'assigned_to', 'assigned_to_username', 'created_at', 'updated_at', 'due_date', 'comments']
        read_only_fields = ['created_by', 'created_at', 'updated_at']
```

Create `backend/apps/tasks/views.py`:
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models as django_models
from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Show tasks created by or assigned to user
        return Task.objects.filter(
            django_models.Q(created_by=user) | django_models.Q(assigned_to=user)
        ).select_related('created_by', 'assigned_to')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        task = self.get_object()
        content = request.data.get('content')
        
        if not content:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        comment = Comment.objects.create(
            task=task,
            author=request.user,
            content=content
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """Get all tasks assigned to current user"""
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
```

Create `backend/apps/tasks/urls.py`:
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
```

Update `backend/config/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.tasks.urls')),
]
```

### روز 1.6: Test Backend (5 min)
```bash
python manage.py createsuperuser
python manage.py runserver

# Visit: http://localhost:8000/api/tasks/
# Or http://localhost:8000/admin/
```

---

## ⏳ Hour 2: Frontend + Docker

### روز 2.1: Frontend Setup (10 min)
```bash
cd frontend
npm install

# Update .env:
# VITE_API_BASE_URL=http://localhost:8000/api
```

### روز 2.2: Frontend Components (25 min)

Create `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const apiCall = async (endpoint, method = 'GET', data = null) => {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };

  if (data) options.body = JSON.stringify(data);

  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
  
  if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
  return response.json();
};

export const getTasks = () => apiCall('/tasks/');
export const createTask = (data) => apiCall('/tasks/', 'POST', data);
export const updateTask = (id, data) => apiCall(`/tasks/${id}/`, 'PATCH', data);
export const deleteTask = (id) => apiCall(`/tasks/${id}/`, 'DELETE');
```

Create `frontend/src/components/TaskList.jsx`:
```jsx
import React, { useState, useEffect } from 'react';
import { getTasks, deleteTask } from '../services/api';
import '../styles/TaskList.css';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await getTasks();
      setTasks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="task-list">
      <h2>ما به تو وظایف</h2>
      {tasks.length === 0 ? (
        <p>هیچ وظیفه‌ای باز وجود ندارد</p>
      ) : (
        <ul>
          {tasks.map(task => (
            <li key={task.id} className={`task task--${task.status}`}>
              <h3>{task.title}</h3>
              <p>{task.description}</p>
              <span className="status">{task.status}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;
```

Create `frontend/src/App.jsx`:
```jsx
import React from 'react';
import TaskList from './components/TaskList';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>بورد وظایف تیمی</h1>
      </header>
      <main className="app-main">
        <TaskList />
      </main>
    </div>
  );
}

export default App;
```

### روز 2.3: Test Frontend (5 min)
```bash
npm run dev
# Visit: http://localhost:5173
```

### روز 2.4: Docker Test (10 min)
```bash
cd ..

# Edit .env for Docker
cp .env.example .env
# DB_NAME=taskboard
# DB_USER=postgres
# DB_PASSWORD=postgres

# Build
docker-compose build

# Run
docker-compose up -d

# Check
docker-compose ps

# Logs
docker-compose logs -f backend
```

### روز 2.5: First Commit (5 min)
```bash
git add .
git commit -m "feat: add task models, API, frontend components"
git push origin main
```

---

## ✅ After 2 Hours

- [x] Backend running (لوکال)
- [x] Frontend running (لوکال)
- [x] Docker working
- [x] First commit pushed

### Next Steps:
1. Add tests (coverage)
2. Add more features (comments, admin panel)
3. Add GitHub Actions
4. Deploy

---

## 🔰 Troubleshooting

**Backend won't start**
```bash
# Check Python version
python --version  # Should be 3.10+

# Clear cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete

# Reinstall
pip install --force-reinstall -r requirements.txt
```

**Frontend won't build**
```bash
# Clear cache
rm -rf node_modules
npm cache clean --force
npm install
```

**Docker issues**
```bash
# Force rebuild
docker-compose build --no-cache

# Check logs
docker-compose logs -f [service-name]

# Clean everything
docker-compose down -v
```

---

**نام بردای برنامه⃆ با این 2 ساعت! 🚀**