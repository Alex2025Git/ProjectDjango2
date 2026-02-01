from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        """Проверяет, явыляется ли пользователь модератором"""

        return request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Проверяет, явыляется ли пользователь владельцем"""

        if request.user.is_staff:
            return True
        return request.user == obj.owner
