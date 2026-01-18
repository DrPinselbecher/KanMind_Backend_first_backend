from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from tasks_app.models import Task, Comments
from .serializers import TaskListSerializer, CommentSerializer
from .permissions import TaskPermission, IsBoardMemberForTaskComments


class TasksViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks.

    Provides CRUD operations for tasks with permission handling.
    On creation, the current user is stored as the task creator.
    """

    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [TaskPermission]

    def perform_create(self, serializer):
        """
        Create a task and set the requesting user as the creator.
        """
        serializer.save(created_by=self.request.user)


class TaskAssignedToCurrentUser(generics.ListAPIView):
    """
    List API view returning tasks assigned to the current user.
    """

    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return tasks where the current user is the assignee.
        """
        user = self.request.user
        filtred_tasks = Task.objects.filter(assignee=user)
        return filtred_tasks


class TaskReviewingCurrentUser(generics.ListAPIView):
    """
    List API view returning tasks where the current user is the reviewer.
    """

    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return tasks where the current user is the reviewer.
        """
        user = self.request.user
        filtred_tasks = Task.objects.filter(reviewer=user)
        return filtred_tasks


class TaskCommentsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing task comments.

    Comments are created for a specific task (via URL kwarg `task_pk`).
    Only authenticated board members are allowed to access or modify comments.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberForTaskComments]
    queryset = Comments.objects.all()

    def perform_create(self, serializer):
        """
        Create a comment for the given task and set the author username.
        """
        task_id = self.kwargs.get("task_pk")
        task = get_object_or_404(Task, pk=task_id)
        serializer.save(task=task, author=self.request.user.username)

    def get_object(self):
        """
        Retrieve a comment instance and enforce object-level permissions.
        """
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj
