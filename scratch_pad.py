# Task grouping for parallel executions
from celery import group
from dcelery.newapp.tasks import tp1, tp2, tp3, tp4

task_group = group(tp1.s(), tp2.s(), tp3.s(), tp4.s())
task_group.apply_async()

# Task chaining for creating a sequence of jobs to execute jobs one by one
from celery import chain
from dcelery.newapp.tasks import tp1, tp2, tp3, tp4

task_chain = chain(tp4.s(), tp3.s(), tp2.s(), tp1.s())
task_chain.apply_async()