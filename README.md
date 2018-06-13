# Django Workers

A super simple background task worker that uses your Django database and admin for management. This
project is mean for small to medium scale uses. If you need something more, check out Celery.


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

```python
from workers import task


@task()
def say_hello(name):
    print('Howdy', name)
```

### Running tasks

```
python manage.py runworkers
```