from celery import chain

from dcelery.celery_config import app


@app.task(queue='tasks')
def add(x, y):
    return x + y

@app.task(queue='tasks')
def multiply(result):
    # Simulate an error for demonstration purposes
    if result == 5:
        raise ValueError('Value Error occurred...')
    return result * 2

def chain_tasks():
    chained_tasks = chain(add.s(1, 2), multiply.s())
    tasks_result = chained_tasks.apply_async()
    tasks_result.get()