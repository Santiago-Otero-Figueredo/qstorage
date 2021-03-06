from django.conf import settings

from rest_framework import permissions


class IsAuthenticatedOwnerUser(permissions.IsAuthenticated):

    def has_permission(self, request, view) -> bool:
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):

        if not request.user.is_owner_folder(obj.pk):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return obj.name != settings.ROOT_NAME_FOLDER

        if request.method in ('POST', ):
            return True

        return False
