"""
Celery configuration.
"""
import os
from kombu import Queue, Exchange
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcelery.settings')

app = Celery('dcelery')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Sentry configuration for error tracking
sentry_dsn = 'https://7b629ae8a69aefb55308570f2173f898@o4506388578762752.ingest.sentry.io/4506388581318656'
sentry_sdk.init(dsn=sentry_dsn, integrations=[CeleryIntegration()])


# ================== RabbitMQ configuration ================== #
app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10}),
    Queue('dead_letter', routing_key='dead_letter')
        
]

# with this config if any tasks lost it stays in queue for a free worker
app.conf.task_acks_late = True
# Default task priority config
app.conf.task_default_priority = 5
# How many tasks from a queue executes at once
app.conf.worker_prefetch_multiplier = 1
# How many resources belong to each workers
app.conf.worker_concurrency = 1

base_dir = os.getcwd()
task_folder = os.path.join(base_dir, 'dcelery', 'celery_tasks')

if os.path.exists(task_folder) and os.path.isdir(task_folder):
    task_modules = []
    for filename in os.listdir(task_folder):
        if filename.startswith('ex') and filename.endswith('.py'):
            module_name = f'dcelery.celery_tasks.{filename[:-3]}'

            module = __import__(module_name, fromlist=['*'])

            for name in dir(module):
                obj = getattr(module, name)
                if callable(obj):
                    task_modules.append(f'{module_name}.{name}')

    app.autodiscover_tasks(task_modules)
