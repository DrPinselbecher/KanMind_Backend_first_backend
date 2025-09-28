# third party imports
from rest_framework import viewsets, status
from rest_framework.response import Response

# local imports
from tasks_app.models import Task
from .serializers import TaskListSerializer

class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer

    