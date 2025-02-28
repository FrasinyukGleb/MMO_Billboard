import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MMO_Billboard.settings')

app = Celery('MMO_Billboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'daily_email_notification': {
        'task': 'board.tasks.daily_email_notification',
        'schedule': crontab(minute=0, hour=0),
    },
}