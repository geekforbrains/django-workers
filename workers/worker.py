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
            Task.objects.create(
                handler=handler,
                args=json.dumps(args),
                kwargs=json.dumps(kwargs),
                run_at=run_at
            )
        return wrapper
    return task_handler
