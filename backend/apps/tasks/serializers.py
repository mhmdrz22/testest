from rest_framework import serializers
from .models import Task, TaskComment, TaskAttachment


class TaskCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = TaskComment
        fields = ['id', 'task', 'author', 'author_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['task', 'author', 'created_at', 'updated_at']


class TaskAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = TaskAttachment
        fields = ['id', 'task', 'file', 'uploaded_by', 'uploaded_by_name', 'uploaded_at']
        read_only_fields = ['uploaded_by', 'uploaded_at']


class TaskSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True, allow_null=True)
    comments = TaskCommentSerializer(many=True, read_only=True)
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'created_by', 'created_by_username',
            'assigned_to', 'assigned_to_username',
            'due_date', 'created_at', 'updated_at', 'completed_at',
            'is_active', 'comments', 'attachments'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'completed_at']


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assigned_to', 'due_date', 'is_active']
    
    def validate_title(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Title cannot be empty")
        return value
