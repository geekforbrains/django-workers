from django.conf import settings


# How long (in seconds) should the worker sleep between task lookups?
SLEEP = getattr(settings, 'WORKERS_SLEEP', 5)

# How many logs to keep in admin
PURGE = getattr(settings, 'WORKERS_PURGE', 1000)
