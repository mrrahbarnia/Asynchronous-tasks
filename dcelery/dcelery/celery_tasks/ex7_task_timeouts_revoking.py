from time import sleep
import sys

from dcelery.celery_config import app

@app.task(queue='tasks', time_limit=5)
def long_running_task():
    sleep(4)
    return 'Task completed successfully'


# @app.task(queue='tasks', bind=True)
def process_task_result(result):
    if result is None:
        print ('Task was revoked, skipping result processing...')
    else:
        return f'Task result: {result}'


def execute_task_examples():
    result = long_running_task.delay()
    try:
        result.get(timeout=10)
    except TimeoutError:
        print("Task timed out...")

    task = long_running_task.delay()
    task.revoke(terminate=True)

    sleep(3)
    sys.stdout.write(task.status)

    if task.status == 'REVOKED':
        process_task_result(None) # Task was revoked, process accordingly
    else:
        process_task_result(task.result)
