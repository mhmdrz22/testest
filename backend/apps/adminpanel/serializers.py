from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AdminLog, NotificationTemplate


class UserListSerializer(serializers.ModelSerializer):
    created_tasks = serializers.SerializerMethodField()
    assigned_tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'created_tasks', 'assigned_tasks']
    
    def get_created_tasks(self, obj):
        return obj.created_tasks.count()
    
    def get_assigned_tasks(self, obj):
        return obj.assigned_tasks.count()


class AdminLogSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin.username', read_only=True)
    
    class Meta:
        model = AdminLog
        fields = ['id', 'admin', 'admin_name', 'action', 'description', 'created_at']
        read_only_fields = ['created_at']


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ['id', 'title', 'subject', 'body', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class NotificationSendSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())
    template_id = serializers.IntegerField()
    custom_subject = serializers.CharField(max_length=255, required=False, allow_blank=True)
    custom_body = serializers.CharField(required=False, allow_blank=True)
