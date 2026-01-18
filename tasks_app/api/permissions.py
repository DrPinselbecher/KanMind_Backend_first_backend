from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotFound
from tasks_app.models import Task
from boards_app.models import Board


class TaskPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        # Liste aller Tasks nur für Admins
        if request.method == "GET" and view.action == "list":
            raise PermissionDenied("Only admins can list all tasks.")

        # Task erstellen → Board muss existieren & User Mitglied sein
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
        user = request.user
        board = obj.board

        if user.is_superuser:
            return True

        # Lesen
        if request.method == "GET":
            return board.owner == user or user in board.members.all()

        # Bearbeiten
        if request.method in ["PUT", "PATCH"]:
            return board.owner == user or user in board.members.all()

        # Löschen → Task-Ersteller ODER Board-Owner
        if request.method == "DELETE":
            if board.owner == user or obj.created_by_id == user.id:
                return True
            raise PermissionDenied(
                "Only the task creator or the board owner can delete this task."
            )

        return False


class IsBoardMemberForTaskComments(BasePermission):
    message = "Only board members can manage comments on this task."

    def has_permission(self, request, view):
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
        user = request.user
        board = obj.task.board

        if request.method == "DELETE":
            if (
                user.is_superuser
                or obj.author == user.username
                or board.owner == user
            ):
                return True
            raise PermissionDenied(
                "Only the comment author, board owner, or admin can delete this comment."
            )

        return user.is_superuser or board.owner == user or user in board.members.all()
