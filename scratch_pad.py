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

# Run on django to inspect tasks
celery inspect active
celery inspect active_queues

# Priority
from dcelery.celery import tp1, tp2, tp3, tp4
tp1.apply_async(priority=3)
tp2.apply_async(priority=9)
tp4.apply_async(priority=6)
tp3.apply_async(priority=8)
tp3.apply_async(priority=8)
tp2.apply_async(priority=9)
tp1.apply_async(priority=3)
tp4.apply_async(priority=6)

# Passing arguments
tp1.apply_async(args=[5,6], kwargs={"message":"The sum is"})

# For printing the result
result = tp1.apply_async(args=[5,6], kwargs={"message":"The sum is"})
result.get()
# Returns True or False for showing whether the task executed successfully or not
result.successful()
# Check if the task has completed
result.ready()