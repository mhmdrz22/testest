from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.utils.crypto import get_random_string

from accounts.models import User
from tasks.models import Task
from .permissions import IsStaffUser
from .tasks import send_admin_notification_email


class AdminOverviewView(APIView):
    """
    GET /api/admin/overview/
    Returns list of all users with their task statistics.
    Admin only.
    """
    permission_classes = [IsStaffUser]

    def get(self, request, *args, **kwargs):
        # Annotate users with task counts
        queryset = (
            User.objects
            .all()
            .annotate(
                open_tasks_count=Count(
                    "tasks",
                    filter=Q(tasks__status__in=["TODO", "DOING"]),
                    distinct=True,
                ),
                total_tasks_count=Count(
                    "tasks",
                    distinct=True,
                )
            )
        )
        
        # Format response to match frontend expectations
        data = [
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_active": user.is_active,
                "open_tasks": user.open_tasks_count,  # Frontend expects 'open_tasks'
                "total_tasks": user.total_tasks_count,  # Frontend expects 'total_tasks'
            }
            for user in queryset
        ]
        return Response(data, status=status.HTTP_200_OK)


class AdminNotifySerializer(serializers.Serializer):
    recipients = serializers.ListField(
        child=serializers.EmailField(),
        allow_empty=False,
    )
    message = serializers.CharField()


class AdminNotifyView(APIView):
    """
    POST /api/admin/notify/
    Send email notification to selected users.
    Admin only.
    """
    permission_classes = [IsStaffUser]

    def post(self, request, *args, **kwargs):
        serializer = AdminNotifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipients = serializer.validated_data["recipients"]
        message = serializer.validated_data["message"]

        # Filter only existing users
        existing_users = User.objects.filter(email__in=recipients).values_list("email", flat=True)
        recipient_list = list(existing_users)

        if not recipient_list:
            return Response(
                {"detail": "No valid recipients found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate unique job ID
        job_id = get_random_string(32)
        
        # Call Celery task asynchronously
        send_admin_notification_email.delay(recipient_list, message)

        return Response(
            {
                "job_id": job_id,
                "recipients_count": len(recipient_list),
                "message": "Notification sent successfully. Emails will be delivered shortly."
            },
            status=status.HTTP_202_ACCEPTED,
        )
