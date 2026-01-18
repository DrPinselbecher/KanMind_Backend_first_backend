# permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsMemberOrOwnerOrAdmin(BasePermission):
    """
    Object-level permission for board access.

    Grants access to superusers, board owners, and board members
    depending on the HTTP method.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user has permission
        to access or modify the given board object.

        Permissions:
        - Superusers: full access
        - SAFE methods (GET, HEAD, OPTIONS): owner or member
        - PUT / PATCH: owner or member
        - DELETE: owner only
        """
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if request.method in (*SAFE_METHODS, "PUT", "PATCH"):
            return (
                user == obj.owner
                or user in obj.members.all()
                or user.is_superuser
            )

        if request.method == "DELETE":
            return user == obj.owner or user.is_superuser

        return False
