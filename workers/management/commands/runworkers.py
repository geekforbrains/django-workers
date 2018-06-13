import json
import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Task
from ...util import autodiscover
from ...worker import registry


class Command(BaseCommand):
    help = 'Start workers and wait for tasks to process'

    def log(self, message):
        self.stdout.write(message)

    def handle(self, *args, **options):
        autodiscover(self.log)
        while True:
            self.log('looking for tasks...')
            tasks = Task.objects.filter(completed_at=None)
            for task in tasks:
                self.log('running: {0}'.format(task.handler))
                args = json.loads(task.args)
                kwargs = json.loads(task.kwargs)
                registry[task.handler](*args, **kwargs)
                task.completed_at = timezone.now()
                task.save()
            self.log('sleeping...')
            time.sleep(5)
