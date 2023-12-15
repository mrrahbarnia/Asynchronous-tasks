from datetime import timedelta

from celery.schedules import crontab

from dcelery.celery_config import app


app.conf.beat_schedule = {
    'task1': {
        'task': 'dcelery.celery_tasks.ex13_task_schedule_crontab.task1',
        # Every 10 minutes between 12 am and 6 am,on each mondays
        'schedule': crontab(minute='0-59/10', hour='0-5', day_of_week='mon'),
        'kwargs': {'foo': 'bar'},
        'args': (2, 3),
        'options': {
            'queue': 'tasks',
            'priory': 5,
        }
    },
    'task2': {
        'task': 'dcelery.celery_tasks.ex13_task_schedule_crontab.task2',
        'schedule': timedelta(seconds=5),
    }
}


@app.task(queue='tasks')
def task1(a, b, **kwargs):
    result = a + b
    print(f"Return Task1 ...{result}")


@app.task(queue='tasks')
def task2():
    return "Return Task2 ..."