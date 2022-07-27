from typing import TYPE_CHECKING

from django.conf import settings

import os
import shutil

if TYPE_CHECKING:
    from ..models import Folder


class FolderManager():

    def __init__(self, folder: 'Folder', *args, **kwargs) -> None:
        self.media_root_path = settings.MEDIA_ROOT
        self.folder = folder

    def __get_old_path_folder(self) -> str:
        """
            Return the path
        """
        if self.folder.is_leaf():
            route_children = self.folder.route.split('/')
        else:
            first_children = self.folder.get_first_child()
            route_children = first_children.route.split('/')

        route_children = route_children[:-1]
        old_path_children = "/".join(route_children)

        return old_path_children

    def _join_with_media_root(self, *args) -> str:
        elements = list(args)
        elements.insert(0, self.media_root_path)
        return os.path.join(*elements)

    def _get_complete_path_folder(self) -> str:
        """ Return the path folder join with the path media folder """
        ancestors = self.folder.get_ancestors_folder()
        path_folder = self.folder.get_path_parent_folder()
        patch_folder = self._join_with_media_root(path_folder)
        if ancestors:
            patch_folder = self._join_with_media_root(path_folder, self.folder.name)
        return patch_folder

    def _join_paths(self, *args) -> str:
        return os.path.join(*args)

    def _create_folder(self, path_folder: str) -> None:
        os.umask(0)
        os.makedirs(path_folder, mode=0o777)

    def _rename_folder(self, old_path: str, new_path: str) -> None:
        os.rename(old_path, new_path)

    def _move_folders(self, path_actual_folder, path_new_parent_folder):
        actual_path = self.__join_paths(self.media_root_path, path_actual_folder)
        new_path = self.__join_paths(self.media_root_path, path_new_parent_folder)
        shutil.move(actual_path, new_path)

    def _update_folder_paths(self):
        """Update the route of actual folder and his children folders"""

        old_path_children = self.__get_old_path_folder()
        media_old_path = self._join_paths(self.media_root_path, old_path_children)

        if self.folder.is_leaf() and not self.folder.is_root():
            media_old_path = self._join_paths(media_old_path, self.folder.old_name)

        media_new_patch = self._join_paths(self.media_root_path, self.folder.route)
        if self.folder.name != settings.ROOT_NAME_FOLDER:
            media_new_patch = self._join_paths(media_new_patch, self.folder.name)

        self._rename_folder(media_old_path, media_new_patch)

        self.folder.update_route_parent_folder_and_children()

    def _execute_pre_save_function(self) -> None:

        path_folder = self.folder.get_path_parent_folder()

        media_patch_folder = self._get_complete_path_folder()

        if self.folder.pk is None:
            self._create_folder(media_patch_folder)
        elif self.folder.get_children_count() > 0 or (self.folder.is_leaf() and not self.folder.is_root()):
            self._update_folder_paths()

        self.folder.route = f'{path_folder}/'
        self.folder.old_name = self.folder.name

    def _delete_folder(self) -> None:

        path_folder = self._get_complete_path_folder()
        shutil.rmtree(path_folder)
        self.folder.delete()


def move_folders_in_media(path_actual_folder, path_new_parent_folder):
    media_root_path = settings.MEDIA_ROOT
    media_actual_folder = os.path.join(media_root_path, path_actual_folder)
    media_new_parent_folder = os.path.join(media_root_path, path_new_parent_folder)
    shutil.move(media_actual_folder, media_new_parent_folder)
