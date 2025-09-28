
from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsOwnerOrAdmin(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS or request.method in ['PUT', 'PATCH']:
            return obj == request.user

        if request.method == 'DELETE':
            return False

        return False