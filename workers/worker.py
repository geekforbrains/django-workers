import json
from django.utils import timezone

from .models import Task


registry = {}  # Store reference to task functions
scheduled = []  # Scheduled tasks to be started on `runworkers` cmd


def task(schedule=None):
    def task_handler(fn):
        handler = '{0}.{1}'.format(fn.__module__, fn.__name__)
        registry[handler] = fn

        if schedule:
            scheduled.append({'handler': handler, 'schedule': schedule})

        def wrapper(*args, **kwargs):
            run_at = kwargs.pop('_schedule', timezone.now())
            task = Task.objects.create(
                handler=handler,
                args=json.dumps(args),
                kwargs=json.dumps(kwargs),
                run_at=run_at
            )

            # return the task id in case needed for polling
            return task.pk
        return wrapper
    return task_handler


def get_status(task_id):
    try:
        return Task.objects.get(pk=task_id).status
    except Task.DoesNotExist:
        return None
