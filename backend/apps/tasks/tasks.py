from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Task


@shared_task
def cleanup_old_tasks():
    """Clean up old completed tasks older than 30 days"""
    cutoff_date = timezone.now() - timedelta(days=30)
    Task.objects.filter(
        status='closed',
        completed_at__lt=cutoff_date,
        is_active=False
    ).delete()
    return 'Cleanup completed'


@shared_task
def send_task_reminder(task_id):
    """Send reminder for upcoming tasks"""
    try:
        task = Task.objects.get(id=task_id)
        if task.assigned_to and task.due_date:
            # Send notification here
            return f'Reminder sent for task: {task.title}'
    except Task.DoesNotExist:
        return 'Task not found'
