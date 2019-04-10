import json
import logging
import signal
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

    def __init__(self, *args, **kwargs):
        self.__SIGINT = False
        signal.signal(signal.SIGINT, self.__handler)
        super().__init__(*args, **kwargs)

    def __handler(self, sig, frame):
        log.info('received SIGINT, shutting down workers...')
        self.__SIGINT = True

    def handle(self, *args, **options):
        # Find any INSTALLED_APPS with a `tasks.py` file and import it
        autodiscover()

        for t in scheduled:
            Task.create_scheduled_task(t['handler'], t['schedule'])

        log.debug('worker: ready for tasks...')
        while not self.__SIGINT:
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
                        log.exception(e)

                    task.completed_at = timezone.now()
                    task.save()

                    if task.schedule:
                        Task.create_scheduled_task(task.handler, task.schedule)

                # if PURGE is 1000, we will keep the latest 1000 completed tasks
                keep = (
                    Task.objects
                    .filter(status=Task.COMPLETED)
                    .order_by('-completed_at')
                    .order_by('-run_at')[:PURGE]
                )

                if keep:
                    # If there are more than PURGE (ex. 1000) completed tasks, delete
                    # any that are not in keep
                    Task.objects.exclude(pk__in=keep).filter(status=Task.COMPLETED).delete()
            else:
                time.sleep(SLEEP)
