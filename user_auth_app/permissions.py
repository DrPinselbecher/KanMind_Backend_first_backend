from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission for user profile access.

    Rules:
    - Admins have full access.
    - Users may read or update their own profile.
    - Deleting user accounts is not allowed via the API.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check whether the requesting user has permission
        to access or modify the given user object.
        """
        if request.user and request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS or request.method in ["PUT", "PATCH"]:
            return obj == request.user

        if request.method == "DELETE":
            return False

        return False
