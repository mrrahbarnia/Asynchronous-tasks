"""
Tasks for celery processing.
"""
# import time

from celery import shared_task

from django.core.management import call_command

@shared_task(queue='tasks')
def task1():
    call_command('migrate_scheduling')




# @shared_task
# def tp1(queue='celery'):
#     time.sleep(3)
#     return

# @shared_task
# def tp2(queue='celery:1'):
#     time.sleep(3)
#     return

# @shared_task
# def tp3(queue='celery:2'):
#     time.sleep(3)
#     return

# @shared_task
# def tp4(queue='celery:3'):
#     time.sleep(3)
#     return

