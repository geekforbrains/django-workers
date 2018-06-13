from django.db import models


class Task(models.Model):
    handler = models.CharField(max_length=255)
    args = models.TextField()
    kwargs = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_at = models.DateTimeField(blank=True, null=True, db_index=True)

    def __str__(self):
        return self.name
