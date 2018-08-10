from datetime import timedelta
import logging

from django.db import models
from django.utils import timezone


log = logging.getLogger(__name__)


class Task(models.Model):
    WAITING = 'waiting'
    COMPLETED = 'completed'
    FAILED = 'failed'

    STATUS_CHOICES = (
        (WAITING, 'Waiting'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed')
    )

    handler = models.CharField(max_length=255, db_index=True)
    args = models.TextField(blank=True)
    kwargs = models.TextField(blank=True)
    error = models.TextField(blank=True)
    schedule = models.IntegerField(blank=True, null=True, db_index=True)
    run_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True, db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=WAITING)

    class Meta:
        ordering = ('-completed_at', '-run_at')

    def __str__(self):
        return self.handler

    @staticmethod
    def create_scheduled_task(handler, schedule):
        if Task.objects.filter(handler=handler, schedule=schedule, completed_at=None).exists():
            log.warn('trying to schedule an already scheduled task: {0}'.format(handler))
            return

        scheduled_time = timezone.now() + timedelta(seconds=schedule)
        log.debug('scheduling task: {0} for {1}'.format(handler, scheduled_time))
        Task.objects.create(
            handler=handler,
            args={},
            kwargs={},
            schedule=schedule,
            run_at=scheduled_time,
        )
