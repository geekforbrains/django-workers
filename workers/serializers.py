from rest_framework import serializers

from .models import Task


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('status',)
