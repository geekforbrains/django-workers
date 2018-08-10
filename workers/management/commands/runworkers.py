import json
import logging
import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Task
from ...util import autodiscover
from ...worker import registry, scheduled
from ...settings import SLEEP, PURGE


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Start workers and wait for tasks to process'

    def handle(self, *args, **options):
        # Find any INSTALLED_APPS with a `tasks.py` file and import it
        autodiscover()

        for t in scheduled:
            Task.create_scheduled_task(t['handler'], t['schedule'])

        while True:
            log.debug('worker: waiting for tasks...')
            tasks = Task.objects.filter(run_at__lte=timezone.now(), completed_at=None)

            if tasks:
                for task in tasks:
                    log.debug('worker: running {0}'.format(task.handler))
                    args = json.loads(task.args)
                    kwargs = json.loads(task.kwargs)

                    try:
                        registry[task.handler](*args, **kwargs)
                        task.status = Task.COMPLETED
                    except Exception as e:
                        task.status = Task.FAILED
                        task.error = str(e)

                    task.completed_at = timezone.now()
                    task.save()

                    if task.schedule:
                        Task.create_scheduled_task(task.handler, task.schedule)

                purge = Task.objects.order_by('-completed_at').order_by('-run_at')[:PURGE]
                if purge:
                    log.debug('purging old tasks')
                    Task.objects.exclude(pk__in=purge).delete()
            else:
                time.sleep(SLEEP)
