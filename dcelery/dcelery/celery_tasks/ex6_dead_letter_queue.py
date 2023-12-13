from dcelery.celery_config import app

from celery import group

app.conf.task_acks_late = True
# with this config if any workers lost, the tasks that it picked up will reject for re'queue
app.conf.task_reject_on_worker_lost = True

@app.task(queue='tasks')
def my_task(z):
    try:
        if z == 2:
            raise ValueError('Value error occurred...')
    except Exception as e:
        handle_failed_tasks.apply_async(args=[z, str(e)])
        raise

@app.task(queue='dead_letter')
def handle_failed_tasks(z, exception):
    return "Custom logic to process."

def run_task_group():
    tasks_group = group(
        my_task.s(1),
        my_task.s(2),
        my_task.s(3),
    )
    tasks_group.apply_async()