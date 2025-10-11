from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class TaskPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        action = view.action

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if action == "list":
            raise PermissionDenied("Only Admins can list all tasks.")

        if action == "create":
            board_id = request.data.get("board")
            if not board_id:
                raise PermissionDenied("Board ID is required to create a task.")
            from boards_app.models import Board
            try:
                board = Board.objects.get(pk=board_id)
            except Board.DoesNotExist:
                raise PermissionDenied("Board does not exist.")
            if board.owner == user or user in board.members.all():
                return True
            raise PermissionDenied("You do not have permission to create a task on this board.")
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        board = obj.board
        action = view.action

        if user.is_superuser:
            return True

        if action == "retrieve":
            if board.owner == user or user in board.members.all():
                return True
            raise PermissionDenied("Only board members can view this task.")

        if action in ["update", "partial_update"]:
            if board.owner == user or user in board.members.all():
                return True
            raise PermissionDenied("Only board members can modify this task.")

        if action == "destroy":
            if obj.created_by == user or board.owner == user:
                return True
            raise PermissionDenied("Only the task creator or board owner can delete this task.")

        return False
