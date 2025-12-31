import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# امنیتی: در محیط واقعی حتماً SECRET_KEY را از env بگیر
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-change-me")

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third‑party apps
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "django_filters",

    # Local apps (توجه به پیشوند apps.)
    "accounts",
    "apps.tasks",
    "apps.adminpanel",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database (با استفاده از dj_database_url و متغیرهای محیطی GitHub Actions/Docker)
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
    )
}

print(f"DEBUG: Connecting to Database -> {DATABASES['default']['ENGINE']}")

# Authentication backends - support case-insensitive email login
AUTHENTICATION_BACKENDS = [
    'accounts.backends.CaseInsensitiveEmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Team Task Board API",
    "DESCRIPTION": "Simple API for managing team tasks (Software Engineering project starter).",
    "VERSION": "1.0.0",
}

CORS_ALLOW_ALL_ORIGINS = True

# نکته مهم: مسیر کامل به اپ یوزر سفارشی
AUTH_USER_MODEL = "accounts.User"


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Celery configuration
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/1")
