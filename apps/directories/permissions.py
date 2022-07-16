from django.conf import settings

from rest_framework import permissions


class IsOwnerUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if obj.owner_user.pk != request.user.pk:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return obj.name != settings.ROOT_NAME_FOLDER

        if request.method in ('POST', ):
            return True
