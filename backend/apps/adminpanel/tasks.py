from celery import shared_task
from .models import AdminLog


@shared_task
def send_bulk_notification(user_ids, template_id, custom_subject=None, custom_body=None):
    """Send bulk notification to users"""
    from .models import NotificationTemplate
    from django.contrib.auth.models import User
    
    try:
        template = NotificationTemplate.objects.get(id=template_id)
        users = User.objects.filter(id__in=user_ids)
        
        # Here you would implement the actual email sending logic
        # For now, we'll just log it
        
        subject = custom_subject or template.subject
        body = custom_body or template.body
        
        # Send email to each user (implement with django.core.mail)
        # For example:
        # send_mail(subject, body, 'from@example.com', [user.email for user in users])
        
        return f'Notification sent to {len(users)} users'
    except NotificationTemplate.DoesNotExist:
        return 'Template not found'


@shared_task
def log_admin_action(admin_id, action, description):
    """Log admin action"""
    from django.contrib.auth.models import User
    
    try:
        admin = User.objects.get(id=admin_id)
        AdminLog.objects.create(
            admin=admin,
            action=action,
            description=description
        )
        return f'Action logged: {action}'
    except User.DoesNotExist:
        return 'Admin user not found'
