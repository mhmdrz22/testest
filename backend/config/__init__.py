# This will make sure celery app is loaded
from .celery import app as celery_app

__all__ = ('celery_app',)

# Trigger workflow test
