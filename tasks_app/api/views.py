from rest_framework import viewsets
from tasks_app.models import Task
from .serializers import TaskListSerializer
from .permissions import TaskPermission


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [TaskPermission]
