from rest_framework import serializers
from .models import Task, TaskComment, TaskAttachment


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'created_by', 'assigned_to',
            'status', 'priority', 'due_date', 'created_at', 'updated_at',
            'completed_at', 'is_active'
        ]
        read_only_fields = ('created_by', 'created_at', 'updated_at', 'completed_at')


class TaskCommentSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)
    
    class Meta:
        model = TaskComment
        fields = ['id', 'task', 'author', 'author_email', 'content', 'created_at', 'updated_at']
        read_only_fields = ('author', 'created_at', 'updated_at')


class TaskAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_email = serializers.EmailField(source='uploaded_by.email', read_only=True)
    
    class Meta:
        model = TaskAttachment
        fields = ['id', 'task', 'file', 'uploaded_by', 'uploaded_by_email', 'uploaded_at']
        read_only_fields = ('uploaded_by', 'uploaded_at')
