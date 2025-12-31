from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AdminLog, NotificationTemplate

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff', 'created_date']
        read_only_fields = ['id', 'created_date']


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
