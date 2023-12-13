from celery import group

from dcelery.celery_config import app


@app.task(queue='tasks')
def my_task(number):
    if number == 3:
        raise ValueError('Value Error...number is invalid.')
    return number * 2


def result_handler(result):
    if result.successful():
        print(f'Task completed: {result.get()}')
    elif result.failed() and isinstance(result.result, ValueError):
        print(f'Task failed: {result.result}')
    elif result.status == 'REVOKED':
        print(f'Task was revoked: {result.id}')

def run_tasks():
    tasks_group = group(my_task.s(i) for i in range(5))
    tasks_result = tasks_group.apply_async()
    tasks_result.get(disable_sync_subtasks=False, propagate=False)

    for result in tasks_result:
        result_handler(result)