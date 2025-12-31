# استفاده از Docker Hub به جای AWS ECR برای جلوگیری از TLS timeout
FROM python:3.10-slim

WORKDIR /app

# متغیر محیطی برای جلوگیری از buffering در Python
ENV PYTHONUNBUFFERED=1

# کپی فایل requirements و نصب وابستگی‌ها
COPY requirements.txt .

# ارتقای pip و نصب وابستگی‌ها
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# کپی تمام کدهای پروژه
COPY . .

# اجرای سرور با gunicorn (برای production)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
