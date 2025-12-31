import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat schedule
app.conf.beat_schedule = {
    'send-periodic-notification': {
        'task': 'apps.adminpanel.tasks.send_periodic_notification',
        'schedule': crontab(minute=0, hour='*/6'),  # Every 6 hours
    },
    'cleanup-old-tasks': {
        'task': 'apps.tasks.tasks.cleanup_old_tasks',
        'schedule': crontab(hour=3, minute=0),  # Daily at 3 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
