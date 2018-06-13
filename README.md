# Django Workers

A simple background task worker that uses your Django database and admin for management. This
project is meant for small to medium scale uses. If you need something more, check out Celery.


## Install

Download the package

```
pip install django-workers
```

and add it to your Django installed apps

```python
INSTALLED_APPS = [
    # ...
    'workers',
    # ...
]
```

## Basics

Create a `tasks.py` file in the Django app you'd like to have tasks in. These tasks will automatically
become available thanks to autodiscovery.

```python
from workers import task

@task()
def say_hello(name):
    print('Howdy', name)
```

### Calling tasks

Tasks become simple Python callables. Calling them inserts that task to your Django database and
waits for a worker to pick it up.

```python
say_hello('Foo')  # Sent to background automatically
```

### Running the workers

Now boot-up your workers to crunch some data. Workers poll the Database for new tasks they should
work on.

```
python manage.py runworkers
```


## Scheduled tasks

Sometimes you want to run a specific task every X minutes or at a later date. Thats what scheduled 
tasks are for.

### Repeating scheduled tasks

Tasks specified with a schedule in minutes will repeat.

```python
from workers import task

@task(schedule=1)
def do_something():
    print('I run every minute')

@task(schedule=5)
def do_something_later():
    print('I run every 5 minutes')

@task(schedule=60*8)
def do_something_even_later():
    print('I run every 8 hours')
```

### Date scheduled tasks

Tasks can be scheduled to *run once* at a later date by passing a `datetime` object when the task
is called.

```python
from datetime import datetime, timedelta
from workers import task

trial_end_date = datetime.utcnow() + timedelta(days=14)

@task()
def trial_ending():
    send_email('Your trial is ending!')

# Specifying the `schedule` argument will tell the worker when this task should run
trial_ending(schedule=trial_end_date)
```

## Settings

You can optionally override these settings in your Django `settings.py` file:

- `WORKERS_DEBUG` (default False) - When True, tasks are run inline instead of async
- `WORKERS_SLEEP` (default 5) - Wait in seconds before checking for tasks, if none were found
- `WORKERS_TIMEOUT` (default 30) - Seconds a task can run before its killed
- `WORKERS_RETRY` (default 3) - Number of retries before giving up