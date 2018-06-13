from django.conf import settings


# When True, all tasks to run inline instead of async
DEBUG = getattr(settings, 'WORKERS_DEBUG', False)

# How long (in seconds) should the worker sleep between task lookups?
SLEEP = getattr(settings, 'WORKERS_SLEEP', 5)
