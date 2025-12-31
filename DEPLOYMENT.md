# راه‌نمای Deployment

<div dir="rtl">

## استقرار روی Liara (PaaS ایرانی)

Liara یک سرویس PaaS رایگانی است که برای استقرار پروژه‌ها به خرابی اسقلد.

### مرحله 1: تهیه کرده

```bash
# CLI Liara را نصب کنید
npm install -g @liara/cli

# از روی لیارا لوگین کنید
liara login

# بررسی پروژه‌ها
liara project list
```

### مرحله 2: استقرار Backend

```bash
# رو به وررتر Backend
cd backend

# ایجاد فایل liara.json
cat > liara.json << EOF
{
  "name": "taskboard-backend",
  "platform": "django",
  "python": "3.11",
  "port": 8000,
  "master": "main"
}
EOF

# استقرار
liara deploy
```

### مرحله 3: استقرار Frontend

```bash
# رو به وررتر Frontend
cd ../frontend

# ایجاد فایل liara.json
cat > liara.json << EOF
{
  "name": "taskboard-frontend",
  "platform": "node",
  "port": 3000,
  "build": "npm run build",
  "start": "npm run preview",
  "master": "main"
}
EOF

# استقرار
liara deploy
```

### مرحله 4: برنامه‌ریزی Database

Liara مربوط PostgreSQL فراهم می‌كند. بعد از استقرار backend:

```bash
# اجرای migrations
liara run --app taskboard-backend python manage.py migrate

# ایجاد Super User
liara run --app taskboard-backend python manage.py createsuperuser
```

---

## دامنه و DNS

### از IranNic دامنه بخرید

1. [IranNic](https://www.irnic.ir) را رفته باز کنید
2. یک دامنه `.ir` را بخرید
3. **Nameservers Liara** را تنظیم کنید:
   - `ns1.liara.ir`
   - `ns2.liara.ir`

### در Liara Dashboard

1. به [Liara Console](https://console.liara.ir) بروید
2. برای هر ام پروژه:
   - **Domains** tab رو باز کنید
   - **Add Domain** را مبر کلیک کنید
   - دامنه خود را وارد کنید
   - SSL Certificate به طور خودکار ایجاد می‌شود

---

## تنظیم Environment Variables

### در Liara Dashboard

**Backend:**

```
DEBUG=False
ALLOWED_HOSTS=yourdomain.ir,www.yourdomain.ir,taskboard-backend.liara.run
DB_NAME=<liara-provided-db-name>
DB_USER=<liara-provided-db-user>
DB_PASSWORD=<liara-provided-db-password>
DB_HOST=<liara-provided-db-host>
DB_PORT=5432
REDIS_URL=<liara-provided-redis-url>
SECRET_KEY=<strong-random-key>
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
VITE_API_BASE_URL=https://yourdomain.ir/api
```

**Frontend:**

```
VITE_API_BASE_URL=https://yourdomain.ir/api
NODE_ENV=production
```

---

## استقرار روی VPS (اختیاری)

### الف) Linode / Hetzner / Vultr

```bash
# SSH به Server
ssh root@your-server-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone Repository
cd /home
git clone https://github.com/mhmdrz22/testest.git
cd testest

# Setup Environment
cp .env.example .env
# روز رسانی فایل .env
sudo nano .env

# Run with Docker Compose
sudo docker-compose up -d

# Check status
sudo docker-compose ps
```

### ب) Nginx برای Reverse Proxy

```bash
# Nginx نصب کنید
sudo apt install nginx

# Configuration
sudo nano /etc/nginx/sites-available/taskboard
```

```nginx
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name yourdomain.ir www.yourdomain.ir;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/taskboard /etc/nginx/sites-enabled/

# Test
sudo nginx -t

# Restart
sudo systemctl restart nginx
```

### ج) SSL with Certbot

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.ir -d www.yourdomain.ir

# Auto-renew
sudo systemctl enable certbot.timer
```

---

## ررفع مشکلات Deployment

### آپ پ عمل نمی‌كند

```bash
# Logs را ببینید
liara logs --app taskboard-backend

# Debug mode
Liara Console > App > Logs tab
```

### Database Connection Error

```bash
# Check database
liara run --app taskboard-backend python manage.py dbshell

# Re-run migrations
liara run --app taskboard-backend python manage.py migrate
```

### Static Files

```bash
# Collect static files
liara run --app taskboard-backend python manage.py collectstatic --noinput
```

---

## رصد و Monitoring

### Logs

```bash
# Backend logs
liara logs --app taskboard-backend

# Frontend logs
liara logs --app taskboard-frontend

# Follow logs
liara logs --app taskboard-backend --follow
```

### Restart Services

```bash
# Restart Backend
liara restart --app taskboard-backend

# Restart Frontend
liara restart --app taskboard-frontend
```

### Health Check

```bash
# Check backend health
curl https://yourdomain.ir/api/health/

# Check frontend
curl https://yourdomain.ir/
```

---

## Continuous Deployment

### GitHub to Liara

1. از [Liara Integration](https://console.liara.ir/integrations) استفاده کنید
2. انتخاب کنید: GitHub Repository
3. انتخاب کنید: مخزن `testest`
4. هر push به main automatically deploy می‌شود

---

## Checklist برای Production

- [ ] DEBUG=False
- [ ] SECRET_KEY تغییر یافته
- [ ] ALLOWED_HOSTS صحیح تنظیم شده
- [ ] Database backup enabled
- [ ] Email configuration verified
- [ ] SSL certificate active
- [ ] Monitoring setup
- [ ] Error logging configured
- [ ] Backup strategy in place

</div>
