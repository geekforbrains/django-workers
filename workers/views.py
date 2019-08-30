from rest_framework import generics

from .models import Task
from .serializers import TaskStatusSerializer


class TaskStatus(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskStatusSerializer
