from rest_framework import permissions


class IsAdminOrSuperUserSafe(permissions.BasePermission):
    """
    Permissions for Admins and SuperUsers. (SAFE)
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsAdminUser(permissions.BasePermission):

    """
    Permissions for Admins and SuperUsers.
    """
    def has_permission(self, request, view):
        return request.user.is_admin


class IsSelf(permissions.BasePermission):
    """
    Permissions for self user.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsOwnerOrAdminRole(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author
                or request.user.is_moderator)
