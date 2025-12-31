from django.db import models
from django.contrib.auth.models import User


class AdminLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'ایجاد'),
        ('update', 'به‌روزرسانی'),
        ('delete', 'حذف'),
        ('send_notification', 'ارسال اطلاع‌رسانی'),
    ]
    
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['admin', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.admin.username} - {self.action}"


class NotificationTemplate(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
