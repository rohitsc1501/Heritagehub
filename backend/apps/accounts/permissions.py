"""Custom permissions for role-based access control."""
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Allows access only to admin users."""
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and
                request.user.role == 'admin')


class IsVisitor(BasePermission):
    """Allows access only to visitor users."""
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and
                request.user.role == 'visitor')


class IsOwnerOrAdmin(BasePermission):
    """Object-level permission: owner or admin."""
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
