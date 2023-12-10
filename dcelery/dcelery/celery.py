"""
Celery configuration.
"""
import os
import time
from kombu import Queue, Exchange

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcelery.settings')

app = Celery('dcelery')

app.config_from_object('django.conf:settings', namespace='CELERY')


# ================== RabbitMQ configuration ================== #
app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10}),
]
app.conf.task_acks_late = True
app.conf.task_default_priority = 5
# How many tasks from a queue executes at once
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_concurrency = 1

@app.task(queue='tasks')
def tp1(a,b,message=None):
    time.sleep(5)
    result = a + b
    if message:
        result = f'{message}: {result}'
    return result

@app.task(queue='tasks')
def tp2():
    time.sleep(3)
    return

@app.task(queue='tasks')
def tp3():
    time.sleep(3)
    return

@app.task(queue='tasks')
def tp4():
    time.sleep(3)
    return


# ================== Redis configuration ================== #
# Routing the tasks to a specific worker
# app.conf.task_routes = {
#     'newapp.tasks.*': {'queue':'queue1'},
#     'newapp.tasks.task2': {'queue':'queue2'}
# }

# Task limits
# app.conf.task_default_rate_limit = '1/m'

# Task prioritization
# app.conf.broker_transport_options = {
#     'priority_steps': list(range(10)),
#     'sep': ':',
#     'queue_order_strategy': 'priority'
# }

app.autodiscover_tasks()


def test():
    result = tp1.apply_async(args=[5,10], kwargs={"message":"The sum is"})

    if result.ready():
        print('Task has completed.')
    else:
        print('Task is still running...')

    if result.successful():
        print('Task completed successfully.')
    else:
        print('Task encountered an error.')

    try:
        task_result = result.get()
        print('Task result:', task_result)
    except Exception as e:
        print('An exception occurred:', str(e))
    
    exception = result.get(propagate=False)
    if exception:
        print('An exception occurred during task execution:', str(exception))


# Synchronous and asynchronous tasks
def execute_sync():
    result = tp1.apply_async(args=[5,10], kwargs={'message':'The sum is'})
    task_result = result.get()
    print('The task is running synchronously')
    print(task_result)

def execute_async():
    result = tp1.apply_async(args=[5,10], kwargs={'message':'The sum is'})
    print('The task is running asynchronously')
    print('Task id:', result.task_id)