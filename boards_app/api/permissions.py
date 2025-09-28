# permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsMemberOrOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if request.method in (*SAFE_METHODS, "PUT", "PATCH"):
            return (user == obj.owner) or (user in obj.members.all())
        
        if request.method == "DELETE":
            return user == obj.owner or user.is_superuser

        return False
