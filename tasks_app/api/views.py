from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from tasks_app.models import Task
from .serializers import TaskListSerializer
from .permissions import TaskPermission


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [TaskPermission]


class TaskAssignedToCurrentUser(generics.ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        filtred_tasks = Task.objects.filter(assignee=user)
        return filtred_tasks
    
class TaskreviewingCurrentUser(generics.ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        filtred_tasks = Task.objects.filter(reviewer=user)
        return filtred_tasks