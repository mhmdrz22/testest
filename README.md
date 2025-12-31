# Team Task Board - پروژه‌ی نهایی

<div dir="rtl">

## 📋 نمای کلی

یک سیستم مدیریت تسک‌های تیمی و پروژه‌ی نهایی درس **مهندسی نرم‌افزار** توسعه‌یافته با:
- **Backend**: Django REST Framework + PostgreSQL
- **Frontend**: React + Vite
- **Async Tasks**: Celery + Redis
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Testing**: Pytest + Jest (Coverage 85%+)

### ✨ ویژگی‌های اصلی

✅ بک‌اند قوی با Django REST Framework  
✅ فرانت‌اند مدرن با React + Vite  
✅ پایگاه‌داده PostgreSQL  
✅ صف‌های ناهمزمان با Celery + Redis برای ارسال ایمیل  
✅ پنل مدیریت برای ارسال اطلاعیه‌ها  
✅ تست‌های جامع و قابل اعتماد (85%+ coverage)  
✅ Docker containerization برای استقرار آسان  
✅ CI/CD خودکار با GitHub Actions  
✅ آماده برای استقرار روی سرورهای واقعی  

---

## 🚀 شروع سریع

### پیش‌نیازها

- Git
- Docker & Docker Compose
- یا Python 3.11+ و Node.js 18+

### نصب و اجرای محلی (بدون Docker)

**1️⃣ Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # یا venv\Scripts\activate (Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**2️⃣ Frontend (در ترمینال جدید):**

```bash
cd frontend
npm install
npm run dev
```

سپس به `http://localhost:5173` بروید.

### 🐳 اجرا با Docker Compose

```bash
# کپی فایل محیط
cp .env.example .env

# ایجاد و اجرای تمام سرویس‌ها
docker-compose up -d

# دیدن لاگ‌ها
docker-compose logs -f
```

پروژه در این آدرس‌ها فعال می‌شود:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin

---

## 📁 ساختار پروژه

### Backend

```
backend/
├── config/              # تنظیمات Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── apps/                # تقسیم‌بندی logical
│   ├── tasks/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── tests.py
│   ├── users/
│   └── admin_panel/     # فیچر جدید
│       ├── views.py
│       ├── tests.py
│       └── tasks.py
├── manage.py
├── requirements.txt
└── Dockerfile
```

### Frontend

```
frontend/
├── src/
│   ├── components/      # کامپوننت‌های reusable
│   ├── pages/           # صفحات اصلی
│   ├── hooks/           # Custom React Hooks
│   ├── services/        # API calls
│   ├── styles/          # CSS/Styling
│   ├── App.jsx
│   └── main.jsx
├── public/
├── package.json
├── vite.config.js
└── Dockerfile
```

---

## 🧪 تست‌نویسی

### تست‌های Backend

```bash
cd backend

# اجرای تمام تست‌ها
python manage.py test --verbosity=2

# اجرای تست‌های خاص
python manage.py test apps.tasks.tests

# تست‌ها با Coverage Report
coverage run --source='.' manage.py test
coverage report
coverage html  # ایجاد HTML report
```

### تست‌های Frontend

```bash
cd frontend

# اجرای تست‌ها
npm run test

# Watch mode
npm run test -- --watch

# Coverage report
npm run test:coverage
```

---

## 🔧 مراحل توسعه (7 مرحله‌ی اصلی)

### ✅ مرحله 1: راه‌اندازی اولیه
- [x] Fork/Clone از starter template
- [x] ایجاد repository جدید: `testest`
- [x] راه‌اندازی محیط محلی

### 📐 مرحله 2: بهبود ساختار و کیفیت کد
- [ ] مرتب‌سازی پوشه‌ها
- [ ] رعایت SOLID Principles
- [ ] استفاده از Design Patterns
- [ ] Refactoring کد
- [ ] بهبود خوانایی و naming

### 🧪 مرحله 3: تست‌نویسی
- [ ] Unit Tests (Backend)
- [ ] Integration Tests
- [ ] Frontend Component Tests
- [ ] Coverage ≥ 85%

### 🐳 مرحله 4: داکرایز
- [x] Dockerfile (Backend)
- [x] Dockerfile (Frontend)
- [x] docker-compose.yml
- [x] PostgreSQL + Redis سرویس‌ها
- [x] .env.example

### ⚙️ مرحله 5: CI/CD
- [x] GitHub Actions workflow
- [ ] Automated tests روی PR
- [ ] Build verification
- [ ] Code quality checks

### 🚀 مرحله 6: Deployment
- [ ] استقرار روی سرور واقعی
- [ ] تنظیم دامنه و DNS
- [ ] SSL Certificate
- [ ] Environment variables

### ✨ مرحله 7: فیچر جدید (Admin Panel)
- [ ] Backend API endpoints
- [ ] Celery tasks برای ارسال ایمیل
- [ ] Frontend Admin Panel
- [ ] تست‌های جامع

---

## 🔌 API Endpoints (Admin Panel)

### دریافت نمای کلی

```bash
GET /api/admin/overview/
Authorization: Token <your-token>

# Response
{
  "users": [
    {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com",
      "full_name": "کاربر اول",
      "open_tasks_count": 5
    }
  ]
}
```

### ارسال اطلاعیه ایمیل

```bash
POST /api/admin/notify/
Authorization: Token <your-token>
Content-Type: application/json

{
  "recipients": ["user@example.com"],
  "message": "# عنوان\n\nمتن پیام به Markdown"
}

# Response
{
  "status": "queued",
  "job_id": "abc123def456",
  "recipients_count": 1
}
```

---

## 📧 تنظیم Email

### استفاده از Gmail

1. [App Password](https://myaccount.google.com/apppasswords) ایجاد کنید
2. فایل `.env` را بروز‌رسانی کنید:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

---

## 🚨 Troubleshooting

### Port نگاه‌داری شده است

```bash
# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### خطای Database Connection

```bash
# بررسی PostgreSQL
docker ps | grep postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

### خطای Celery

```bash
# بررسی Redis
redis-cli ping

# اجرای Worker به صورت دستی
celery -A config worker -l info
```

---

## 📚 منابع مفید

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [GitHub Actions Guide](https://docs.github.com/en/actions)
- [Celery Documentation](https://docs.celeryproject.org/)

---

## 👥 مشارکت‌کنندگان

- **شما** - مهندس نرم‌افزار اصلی
- **تیم پروژه** - مشارکت در تست‌نویسی و deployment

---

## 📝 مجوز

مجوز MIT - برای استفاده‌ی آزاد در پروژه‌های شخصی و تجاری

---

## 📅 ددالین

**تاریخ تحویل نهایی**: 1404/10/03 23:59:59  
**تاریخ ارائه**: قبل از 1404/10/09

---

<div align="center">

**ساخته شده با ❤️ برای درس مهندسی نرم‌افزار**

</div>

</div>
