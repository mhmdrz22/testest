from django.contrib import admin
from .models import AdminLog, NotificationTemplate


@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ['admin', 'action', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['admin__username', 'description']
    readonly_fields = ['created_at']


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subject']
