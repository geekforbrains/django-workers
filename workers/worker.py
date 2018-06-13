import json

from .models import Task


registry = {}  # Store reference to task functions


def task():
    def task_handler(handler):
        name = '{0}.{1}'.format(handler.__module__, handler.__name__)
        registry[name] = handler

        def wrapper(*args, **kwargs):
            Task.objects.create(
                handler=name,
                args=json.dumps(args),
                kwargs=json.dumps(kwargs)
            )
        return wrapper
    return task_handler
