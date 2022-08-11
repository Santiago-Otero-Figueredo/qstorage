from django.conf import settings

from rest_framework import permissions


class IsAuthenticatedOwnerFolderUser(permissions.IsAuthenticated):

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


class IsAuthenticatedOwnerFolderFileUser(permissions.IsAuthenticated):

    def has_permission(self, request, view) -> bool:
        data = dict(request.data)

        if super().has_permission(request, view):
            user_folders = request.user.get_all_folders().values_list('pk', flat=True)

            actual_folder = data.get('parent_folder', None)
            print('user_folders: ', user_folders, 'actual_folder: ', actual_folder)
            if actual_folder is not None:
                return int(actual_folder[0]) in user_folders

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):

        if not request.user.is_owner_file(obj.pk):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return True

        if request.method in ('POST', ):
            return True

        return False
