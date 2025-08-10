# internship/permissions.py
from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    """Allow only users with role='admin'."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
