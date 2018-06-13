import json
import logging
import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Task
from ...util import autodiscover
from ...worker import registry


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Start workers and wait for tasks to process'

    def handle(self, *args, **options):
        # Find any INSTALLED_APPS with a `tasks.py` file and import it
        autodiscover()

        while True:
            log.debug('worker: waiting for tasks...')
            tasks = Task.objects.filter(completed_at=None)
            for task in tasks:
                self.log('worker: running {0}'.format(task.handler))
                args = json.loads(task.args)
                kwargs = json.loads(task.kwargs)
                registry[task.handler](*args, **kwargs)
                task.completed_at = timezone.now()
                task.save()
            time.sleep(5)
