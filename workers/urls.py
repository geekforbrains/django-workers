from django.urls import path

from .views import TaskStatus

urlpatterns = [
    path('task/<int:pk>', TaskStatus.as_view(), name='task-status')
]
