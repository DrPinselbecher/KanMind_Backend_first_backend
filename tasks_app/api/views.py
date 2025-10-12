from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status 
from django.shortcuts import get_object_or_404

from tasks_app.models import Task, Comments
from .serializers import TaskListSerializer, CommentSerializer
from .permissions import TaskPermission, IsBoardMemberForTaskComments


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
    

class TaskReviewingCurrentUser(generics.ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        filtred_tasks = Task.objects.filter(reviewer=user)
        return filtred_tasks
    


class TaskCommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberForTaskComments]
    queryset = Comments.objects.all()

    def perform_create(self, serializer):
        task_id = self.kwargs.get("task_pk")
        task = get_object_or_404(Task, pk=task_id)
        serializer.save(task=task, author=self.request.user.username)


    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
