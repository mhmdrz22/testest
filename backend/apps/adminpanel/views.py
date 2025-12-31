from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import AdminLog, NotificationTemplate
from .serializers import UserListSerializer, AdminLogSerializer, NotificationTemplateSerializer, NotificationSendSerializer


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class AdminOverviewViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get admin dashboard overview"""
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        
        from apps.tasks.models import Task
        total_tasks = Task.objects.count()
        open_tasks = Task.objects.filter(status='open').count()
        closed_tasks = Task.objects.filter(status='closed').count()
        
        return Response({
            'users': {
                'total': total_users,
                'active': active_users
            },
            'tasks': {
                'total': total_tasks,
                'open': open_tasks,
                'closed': closed_tasks
            }
        })
    
    @action(detail=False, methods=['get'])
    def users(self, request):
        """Get all users list for admin"""
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)


class AdminLogViewSet(viewsets.ModelViewSet):
    queryset = AdminLog.objects.all()
    serializer_class = AdminLogSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['action', 'admin']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['post'])
    def send_notification(self, request):
        """Send notification to users"""
        serializer = NotificationSendSerializer(data=request.data)
        if serializer.is_valid():
            # Here you would implement the actual notification sending logic
            # For now, we'll just log it
            user_ids = serializer.validated_data.get('user_ids')
            template_id = serializer.validated_data.get('template_id')
            
            AdminLog.objects.create(
                admin=request.user,
                action='send_notification',
                description=f'Sent notification to {len(user_ids)} users using template {template_id}'
            )
            
            return Response({
                'status': 'success',
                'message': f'Notification sent to {len(user_ids)} users'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
