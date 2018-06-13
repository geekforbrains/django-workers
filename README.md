# Django Workers

A simple background task worker that uses your Django database and admin for management. This
project is meant for small to medium scale uses. If you need something more, check out Celery.


### Install

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

### Creating tasks

Create a `tasks.py` file in the Django app you'd like to have tasks in. These tasks will automatically
become available thanks to autodiscovery.

```python
from workers import task


@task()
def say_hello(name):
    print('Howdy', name)
```

### Calling tasks

Tasks become simple Python callables.

```python
say_hello('Foo')  # Sent to background automatically
```

### Running the workers

Now boot-up your workers to crunch some data.

```
python manage.py runworkers
```