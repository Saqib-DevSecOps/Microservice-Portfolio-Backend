from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class VerifyUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow GET, HEAD, OPTIONS requests

        user_id = request.headers.get('X-User-Id')
        if not user_id:
            raise PermissionDenied("User information missing")

        # Attach user info to the request for later use
        request.user_info = {'id': user_id}
        return True