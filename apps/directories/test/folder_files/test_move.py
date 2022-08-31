from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import Folder, File
from apps.directories.test.files.test_crud import FileCRUDAPITest

import os.path

URL_MOVE_FOLDER = 'directories:folders-move-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderFileMoveTest(FileCRUDAPITest):

    def test_01_move_folder_with_files(self):
        """ Testing to move a folder with files to another folder
            new structure:
                ...
                |- NVIDIA
                    |- RTX
                        |- TI
                            |- 2060_TI.png
                            |- 3060_TI.png
                            |- 1070_TI.png
                            |- 1080_TI.png
                        |- 2060.jpg
                    |- GTX
                        |- TI
                        |- 1030.pdf
                    |- Series_1000.pdf
                    |- Series_2000.pdf
                ...

        """

        payload = {
            'folders_to_move': [self.rtx.pk, self.gtx.pk],
            'new_parent_folder': self.nvidia.pk
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_move_folder, payload)

        new_parent_folder = Folder.get_by_id(self.nvidia.pk)

        folder_gtx_moved = Folder.get_by_id(self.gtx.pk)
        folder_gtx_ti_moved = Folder.get_by_id(self.ti_gtx.pk)
        file_1030_moved = File.get_by_id(self.f_1030.pk)

        folder_rtx_moved = Folder.get_by_id(self.rtx.pk)
        folder_ti_rtx_moved = Folder.get_by_id(self.ti_rtx.pk)
        file_2060 = File.get_by_id(self.f_2060.pk)
        file_1070_ti = File.get_by_id(self.f_1070_ti.pk)
        file_1080_ti = File.get_by_id(self.f_1080_ti.pk)
        file_2060_ti = File.get_by_id(self.f_2060_ti.pk)
        file_3060_ti = File.get_by_id(self.f_3060_ti.pk)

        media_path_gtx = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{folder_gtx_moved.name}'
        media_path_gtx_ti = f'{media_path_gtx}/{folder_gtx_ti_moved.name}'
        media_path_rtx = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{folder_rtx_moved.name}'
        media_path_rtx_ti = f'{media_path_rtx}/{folder_ti_rtx_moved.name}'

        media_file_1030_path = f'{media_path_gtx}/{file_1030_moved.name}'
        media_file_2060_path = f'{media_path_rtx}/{file_2060.name}'
        media_file_1070_ti_path = f'{media_path_rtx_ti}/{file_1070_ti.name}'
        media_file_1080_ti_path = f'{media_path_rtx_ti}/{file_1080_ti.name}'
        media_file_2060_ti_path = f'{media_path_rtx_ti}/{file_2060_ti.name}'
        media_file_3060_ti_path = f'{media_path_rtx_ti}/{file_3060_ti.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(folder_gtx_moved.get_parent().name, new_parent_folder.name)
        self.assertEqual(folder_gtx_moved.get_path_parent_folder(), new_parent_folder.get_path_folder())
        self.assertEqual(folder_rtx_moved.get_parent().name, new_parent_folder.name)
        self.assertEqual(folder_rtx_moved.get_path_parent_folder(), new_parent_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(folder_gtx_moved.is_child_of(new_parent_folder))
        self.assertTrue(folder_gtx_ti_moved.is_descendant_of(new_parent_folder))
        self.assertTrue(folder_rtx_moved.is_child_of(new_parent_folder))
        self.assertTrue(folder_ti_rtx_moved.is_descendant_of(new_parent_folder))

        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_gtx))
        self.assertTrue(os.path.exists(media_path_rtx))
        self.assertTrue(os.path.exists(media_path_rtx_ti))
        self.assertTrue(os.path.exists(media_path_gtx_ti))

        self.assertTrue(os.path.exists(media_file_1030_path))
        self.assertTrue(os.path.exists(media_file_2060_path))
        self.assertTrue(os.path.exists(media_file_1070_ti_path))
        self.assertTrue(os.path.exists(media_file_1080_ti_path))
        self.assertTrue(os.path.exists(media_file_2060_ti_path))
        self.assertTrue(os.path.exists(media_file_3060_ti_path))

    def test_02_move_folder_with_files(self):
        """ Testing to move a folder with files to another folder
            new structure:
                ...
                |- Peripherals
                    |- Keyboard.png
                    |- Mouse.png
                    |- Headphones.png
                    |- Storage
                        |- HDD.png
                        |- MV_2.png
                ...
        """

        payload = {
            'folders_to_move': [self.storage.pk],
            'new_parent_folder': self.peripherals.pk
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_move_folder, payload)

        new_parent_folder = Folder.get_by_id(self.peripherals.pk)

        folder_storage_moved = Folder.get_by_id(self.storage.pk)
        file_hdd = File.get_by_id(self.f_hdd.pk)
        file_mv_2 = File.get_by_id(self.f_mv_2.pk)

        media_path_storage = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{folder_storage_moved.name}'
        media_path_hdd = f'{media_path_storage}/{file_hdd.name}'
        media_path_mv_2 = f'{media_path_storage}/{file_mv_2.name}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(folder_storage_moved.get_parent().name, new_parent_folder.name)
        # Validation of changes in inheritance database
        self.assertTrue(folder_storage_moved.is_descendant_of(new_parent_folder))
        self.assertTrue(file_hdd.parent_folder.is_child_of(new_parent_folder))
        self.assertTrue(file_mv_2.parent_folder.is_child_of(new_parent_folder))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_storage))
        self.assertTrue(os.path.exists(media_path_hdd))
        self.assertTrue(os.path.exists(media_path_mv_2))
