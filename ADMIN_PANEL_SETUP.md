# 🎯 Admin Panel Setup Guide

## Overview
This guide walks you through setting up and testing the complete Admin Panel feature for Team Task Board.

## ✅ What's Included

### Frontend
- React Router with `/admin` route
- Admin-only access control based on `user.is_staff`
- User management table with checkbox selection
- Markdown editor for email composition
- Real-time email notification sending

### Backend
- `GET /api/admin/overview/` - Get all users with task statistics
- `POST /api/admin/notify/` - Send email to selected users
- Celery + Redis for asynchronous email processing
- Admin-only permissions (`IsStaffUser`)

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/mhmdrz22/testest.git
cd testest

# Create .env file from example
cp .env.example .env

# Edit .env (optional - defaults work for development)
nano .env
```

### 2. Start Services

```bash
# Build and start all services (backend, frontend, db, redis, worker)
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### 3. Create Admin User

```bash
# Open Django shell
docker-compose exec backend python manage.py shell
```

Inside the shell:

```python
from django.contrib.auth import get_user_model
User = get_user_model()

# Create admin user
admin = User.objects.create_user(
    email='admin@example.com',
    username='admin',
    password='admin123',
    is_staff=True,
    is_superuser=True
)
print(f"Admin created: {admin.email}")

# Create regular users for testing
user1 = User.objects.create_user(
    email='user1@example.com',
    username='user1',
    password='user123'
)
user2 = User.objects.create_user(
    email='user2@example.com',
    username='user2',
    password='user123'
)
print("Test users created")

exit()
```

### 4. Access Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin/

---

## 🧪 Testing the Admin Panel

### Step 1: Login as Admin

1. Open http://localhost:5173
2. Login with:
   - Email: `admin@example.com`
   - Password: `admin123`
3. You should see "Admin" badge next to your email
4. Navigation menu should show "Admin Panel" link

### Step 2: Access Admin Panel

1. Click "Admin Panel" in navigation
2. You should see:
   - User list table
   - Columns: Checkbox, Email, Username, Open Tasks, Total Tasks
   - Markdown editor for email
   - "Send Email" button

### Step 3: Test Access Control

1. Logout
2. Login as regular user:
   - Email: `user1@example.com`
   - Password: `user123`
3. "Admin Panel" link should NOT appear
4. Try visiting http://localhost:5173/admin directly
5. Should redirect to dashboard (access denied)

### Step 4: Send Test Email

1. Login as admin again
2. Go to Admin Panel
3. Select one or more users (check checkboxes)
4. Write message in Markdown editor:
   ```markdown
   ## Hello Team!
   
   This is a test notification from the admin panel.
   
   - Task 1
   - Task 2
   
   **Thanks!**
   ```
5. Click "Send Email"
6. Check console output (docker-compose logs worker)

---

## 📧 Email Configuration

### Development (Console Backend)

By default, emails are printed to console. Check worker logs:

```bash
docker-compose logs -f worker
```

### Production (SMTP)

Edit `.env`:

```env
# Gmail Example
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@taskboard.ir
```

**Gmail Setup:**
1. Enable 2-factor authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password in `EMAIL_HOST_PASSWORD`

**Restart services after changing .env:**
```bash
docker-compose down
docker-compose up -d
```

---

## 🔍 API Testing

### Get Admin Overview

```bash
# Login and get token
curl -X POST http://localhost:8000/api/accounts/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Copy access token, then:
curl -X GET http://localhost:8000/api/admin/overview/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "email": "admin@example.com",
    "username": "admin",
    "is_active": true,
    "open_tasks": 0,
    "total_tasks": 0
  },
  {
    "id": 2,
    "email": "user1@example.com",
    "username": "user1",
    "is_active": true,
    "open_tasks": 0,
    "total_tasks": 0
  }
]
```

### Send Notification

```bash
curl -X POST http://localhost:8000/api/admin/notify/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": ["user1@example.com", "user2@example.com"],
    "message": "# Test\n\nThis is a test notification."
  }'
```

**Expected Response:**
```json
{
  "job_id": "abc123...",
  "recipients_count": 2,
  "message": "Notification sent successfully. Emails will be delivered shortly."
}
```

---

## 🐛 Troubleshooting

### Admin Panel Not Showing

**Problem:** Admin Panel link not visible after login

**Solution:**
```bash
# Verify user is staff
docker-compose exec backend python manage.py shell
```
```python
from accounts.models import User
user = User.objects.get(email='admin@example.com')
print(f"is_staff: {user.is_staff}")
print(f"is_superuser: {user.is_superuser}")

# If False, fix it:
user.is_staff = True
user.is_superuser = True
user.save()
exit()
```

### Cannot Access /admin Route

**Problem:** Redirects to dashboard or shows blank page

**Solution:**
1. Clear browser cache
2. Check browser console for errors
3. Verify frontend build:
   ```bash
   docker-compose logs frontend
   ```

### Emails Not Sending

**Problem:** Email task fails or no output

**Solution:**
```bash
# Check worker logs
docker-compose logs -f worker

# Check Redis connection
docker-compose exec backend python manage.py shell
```
```python
import redis
r = redis.Redis(host='redis', port=6379, db=0)
r.ping()
# Should return: True
exit()
```

### Permission Denied (403)

**Problem:** API returns 403 Forbidden

**Solution:**
- Ensure user has `is_staff=True`
- Check JWT token is valid (not expired)
- Use fresh token from `/api/accounts/token/`

---

## 📊 Service Architecture

```
┌─────────────┐
│   Frontend  │  React + Vite (port 5173)
│  /admin UI  │  
└──────┬──────┘
       │
       ↓ HTTP
┌─────────────┐
│   Backend   │  Django + DRF (port 8000)
│  Admin APIs │  
└──────┬──────┘
       │
       ├─→ PostgreSQL (port 5432)
       │
       └─→ Redis (port 6379)
              ↓
       ┌──────────────┐
       │ Celery Worker│  Email processing
       └──────────────┘
```

---

## ✅ Production Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False` in settings
- [ ] Configure real SMTP (Gmail, SendGrid, Mailgun)
- [ ] Setup SSL/TLS certificates
- [ ] Use strong passwords
- [ ] Enable CSRF protection
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Setup monitoring for Celery worker
- [ ] Add rate limiting to admin endpoints
- [ ] Backup database regularly
- [ ] Use environment-specific .env files

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin/
- **Celery Docs**: https://docs.celeryq.dev/
- **Redis Docs**: https://redis.io/docs/

---

## 🎉 Success!

Your Admin Panel is now fully operational!

**Next Steps:**
1. Create tasks for test users
2. Test email notifications
3. Explore API documentation
4. Customize email templates
5. Add more admin features

**Need Help?**
- Check logs: `docker-compose logs [service-name]`
- Review API docs: http://localhost:8000/api/docs/
- Open an issue on GitHub

---

**Built with ❤️ for Software Engineering Course**
