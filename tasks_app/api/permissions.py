from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotFound

from tasks_app.models import Task
from boards_app.models import Board


class TaskPermission(BasePermission):
    """
    Permission class for task access and modifications.

    Rules:
    - Admins (superusers) have full access.
    - Listing all tasks is restricted to admins.
    - Creating a task requires a valid board and membership (owner or member).
    - Reading/updating a task requires board membership (owner or member).
    - Deleting a task is restricted to the task creator or the board owner.
    """

    def has_permission(self, request, view):
        """
        Check whether the requesting user has general permission
        for the current action (before object-level checks).
        """
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if request.method == "GET" and getattr(view, "action", None) == "list":
            raise PermissionDenied("Only admins can list all tasks.")

        if request.method == "POST":
            board_id = request.data.get("board")

            if not board_id:
                raise PermissionDenied("Board ID is required to create a task.")

            try:
                board = Board.objects.get(pk=board_id)
            except Board.DoesNotExist:
                raise NotFound("Board does not exist.")

            if board.owner == user or user in board.members.all():
                return True

            raise PermissionDenied(
                "You do not have permission to create a task on this board."
            )

        return True

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user has permission
        for the specific task instance.
        """
        user = request.user
        board = obj.board

        if user.is_superuser:
            return True

        if request.method in ["GET", "PUT", "PATCH"]:
            return board.owner == user or user in board.members.all()

        if request.method == "DELETE":
            if board.owner == user or obj.created_by_id == user.id:
                return True

            raise PermissionDenied(
                "Only the task creator or the board owner can delete this task."
            )

        return False


class IsBoardMemberForTaskComments(BasePermission):
    """
    Permission class for managing task comments.

    Access is granted to board members, the board owner, or admins.
    The permission resolves the task from the nested route kwarg `task_pk`.
    """

    message = "Only board members can manage comments on this task."

    def has_permission(self, request, view):
        """
        Check whether the requesting user may access the comments endpoint
        for the given task (resolved by `task_pk`).
        """
        task_id = view.kwargs.get("task_pk")

        if not task_id:
            raise NotFound("Task id missing.")

        try:
            task = Task.objects.select_related("board").get(pk=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task not found.")

        user = request.user
        board = task.board

        if user.is_superuser or board.owner == user or user in board.members.all():
            return True

        raise PermissionDenied(self.message)

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user may perform an action
        on a specific comment instance.
        """
        user = request.user
        board = obj.task.board

        if request.method == "DELETE":
            if user.is_superuser or obj.author == user.username or board.owner == user:
                return True

            raise PermissionDenied(
                "Only the comment author, board owner, or admin can delete this comment."
            )

        return user.is_superuser or board.owner == user or user in board.members.all()
