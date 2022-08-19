from typing import TYPE_CHECKING, Tuple

from django.conf import settings

import os
import shutil

if TYPE_CHECKING:
    from ..models import File


class FileManager():

    def __init__(self, actual_file: 'File', old_file: 'File' = None) -> None:
        self.media_root_path = settings.MEDIA_ROOT
        self.actual_file = actual_file
        self.old_file = old_file

    def __get_old_path_folder(self) -> str:
        """
            Return the path
        """
        return self.old_file.parent_folder.get_absolute_path_folder()

    def __get_new_path_folder(self) -> str:
        return self.actual_file.parent_folder.get_absolute_path_folder()

    def _join_paths(self, *args) -> str:
        return os.path.join(*args)

    def _rename_folder(self, old_path: str, new_path: str) -> None:
        os.rename(old_path, new_path)

    def _move_folders(self, path_actual_file, path_new_file):
        shutil.move(path_actual_file, path_new_file)

    def __process_paths(self) -> Tuple[str, str]:
        """ Return the old an new path in that order like a tuple"""

        old_folder_path = self.__get_old_path_folder()
        new_folder_path = self.__get_new_path_folder()

        new_file_name = self.actual_file.get_full_name()
        old_file_name = self.old_file.get_full_name()

        old_rename = self._join_paths(old_folder_path, old_file_name)
        new_rename = self._join_paths(new_folder_path, new_file_name)
        return (old_rename, new_rename)

    def _update_file_paths(self):
        """Update the path of actual file """

        paths_processed = self.__process_paths()
        old_rename = paths_processed[0]
        new_rename = paths_processed[1]

        self._move_folders(old_rename, new_rename)
        self.actual_file.file = f'{self.actual_file.parent_folder.get_path_folder()}/{self.actual_file.get_full_name()}'

    def _update_file_name(self):
        """Update the name of actual file """

        paths_processed = self.__process_paths()
        old_rename = paths_processed[0]
        new_rename = paths_processed[1]

        self._rename_folder(old_rename, new_rename)
        self.actual_file.file = f'{self.actual_file.parent_folder.get_path_folder()}/{self.actual_file.get_full_name()}'
        self.actual_file.name = self.actual_file.get_full_name()

    def _process_save(self):

        old_folder = self.old_file.parent_folder.get_absolute_path_folder()
        new_folder = self.actual_file.parent_folder.get_absolute_path_folder()

        new_file_name = self.actual_file.get_full_name()
        old_file_name = self.old_file.get_full_name()

        if old_folder != new_folder:
            self._update_file_paths()

        if old_file_name != new_file_name:
            self._update_file_name()

    def _delete_folder(self) -> None:

        pass
