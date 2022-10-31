from rest_framework import permissions

from users.models import User


class UserPermission(permissions.BasePermission):
    """Give access if user is authenticated"""
    def has_object_permission(self, request, view, obj) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and obj == request.user
        )


class AdminPermission(permissions.BasePermission):
    """Give access if user is admin"""
    def has_object_permission(self, request, view, obj) -> bool:
        return (
            request.user
            and request.user.role == User.Roles.ADMIN
            and request.user.is_authenticated
        )


class CuratorPermission(permissions.BasePermission):
    """Give access if user is curator"""
    def has_object_permission(self, request, view, obj) -> bool:
        return (
            request.user
            and request.user.role == User.Roles.CURATOR
            and request.user.is_authenticated
        )


class AdminOrReadOnly(permissions.BasePermission):
    """Give access if user use safe methods or admin"""
    def has_object_permission(self, request, view, obj) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user
                and request.user.role == User.Roles.ADMIN
                and request.user.is_authenticated
            )
        )
