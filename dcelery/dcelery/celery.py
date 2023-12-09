"""
Celery configuration.
"""
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcelery.settings')

app = Celery('dcelery')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Routing the tasks to a specific worker
app.conf.task_routes = {
    'newapp.tasks.*': {'queue':'queue1'},
    'newapp.tasks.task2': {'queue':'queue2'}
}

app.autodiscover_tasks()