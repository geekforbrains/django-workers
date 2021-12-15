from django.conf import settings


# How long (in seconds) should the worker sleep between task lookups?
SLEEP = getattr(settings, 'WORKERS_SLEEP', 5)

# How many logs to keep in admin
PURGE = getattr(settings, 'WORKERS_PURGE', 1000)

# Which apps should we skip when looking for tasks.py?
IGNORE_APPS = getattr(settings, 'WORKERS_IGNORE_APPS', '')
