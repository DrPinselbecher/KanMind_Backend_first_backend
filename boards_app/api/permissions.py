from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

class IsMemberOrOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated("Du bist nicht eingeloggt. Bitte melde dich zuerst an.")
        
        if request.user.is_superuser:
            return True
        if request.user == obj.owner:
            return True
        if request.user in obj.members.all():
            return True
        
        raise PermissionDenied("Du hast keine Berechtigung, dieses Board zu sehen.")
