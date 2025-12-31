from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Task, TaskComment, TaskAttachment
from .serializers import TaskSerializer, TaskCommentSerializer, TaskAttachmentSerializer, TaskCreateUpdateSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def get_queryset(self):
        user = self.request.user
        # Show tasks created by user or assigned to user
        queryset = Task.objects.filter(
            Q(created_by=user) | Q(assigned_to=user)
        ).prefetch_related('comments', 'attachments')
        
        # Filter by status if provided
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        return queryset.distinct()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        task = self.get_object()
        # Only creator or assigned user can update
        if self.request.user != task.created_by and self.request.user != task.assigned_to:
            self.permission_denied(
                self.request,
                message="You do not have permission to edit this task."
            )
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        task = self.get_object()
        task.mark_completed()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        task = self.get_object()
        serializer = TaskCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        task = self.get_object()
        comments = task.comments.all()
        serializer = TaskCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def attachments(self, request, pk=None):
        task = self.get_object()
        attachments = task.attachments.all()
        serializer = TaskAttachmentSerializer(attachments, many=True)
        return Response(serializer.data)


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TaskAttachmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAttachment.objects.all()
    serializer_class = TaskAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
