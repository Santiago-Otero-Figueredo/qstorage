from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import Folder, File
from apps.directories.test.files.test_crud import FileCRUDAPITest

import os.path

URL_MOVE_FILE = 'directories:files-move-files'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FileMoveTest(FileCRUDAPITest):

    def test_01_move_file_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'parent_folder': self.software.pk,
            'files_to_move': [self.f_windows.pk, self.f_linux.pk]
        }

        url_move_folder = reverse(URL_MOVE_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.get(url_move_folder, payload)
        response_2 = self.client.delete(url_move_folder, payload)
        response_3 = self.client.put(url_move_folder, payload)
        response_4 = self.client.post(url_move_folder, payload)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_4.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_move_file_missing_field(self):
        """ Testing the validation of required parent_folder field """

        payload = {
            'files_to_move': [self.f_windows.pk, self.f_linux.pk]
        }

        url_move_folder = reverse(URL_MOVE_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_03_move_file_missing_field(self):
        """ Testing the validation of required files_to_move field """

        payload = {
            'parent_folder': self.software.pk
        }

        url_move_folder = reverse(URL_MOVE_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_04_move_file_not_exists_parent_folder(self):
        """ Testing the validation of required new parent folder exists """

        payload = {
            'parent_folder': 1000,
            'files_to_move': [self.f_windows.pk, self.f_linux.pk]
        }

        url_move_folder = reverse(URL_MOVE_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_05_move_file_not_actual_parent_folder_different_of_new_parent_folder(self):
        """ Testing the validation of precondition:
         new parent folder must be different of actual parent folder """

        payload = {
            'parent_folder': self.peripherals.pk,
            'files_to_move': [self.f_keyboard.pk, self.f_mouse.pk, self.f_headphones.pk]
        }

        url_move_folder = reverse(URL_MOVE_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_06_move_file_not_different_name_file_children(self):
        """ Testing the validation of precondition:
         the actual files must to have a different name of the children files folders
         in the new parent folder """

        payload = {
            'parent_folder': self.software.pk,
            'files_to_move': [self.f_windows.pk, self.f_linux.pk]
        }

        url_move_folder = reverse(URL_MOVE_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)

    def test_07_move_files_from_leaf_folder(self):
        """ Testing to move many files from leaf folder
            new structure:
                ...
                |- Software
                    |- Operative system
                        |- Windows.pdf
                        |- linux.pdf
                    ...
        """

        payload = {
            'parent_folder': self.ops.pk,
            'files_to_move': [self.f_windows.pk, self.f_linux.pk]
        }

        url_move_folder = reverse(URL_MOVE_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_move_folder, payload)

        new_parent_folder = Folder.get_by_id(self.ops.pk)
        file_linux_move = File.get_by_id(self.f_linux.pk)
        file_windows_move = File.get_by_id(self.f_windows.pk)
        media_linux_path = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{file_linux_move.get_full_name()}'
        media_windows_path = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{file_windows_move.get_full_name()}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertTrue(new_parent_folder.has_this_file(file_linux_move.pk))
        self.assertTrue(new_parent_folder.has_this_file(file_windows_move.pk))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_linux_path))
        self.assertTrue(os.path.exists(media_windows_path))

    def test_08_move_many_files_of_parent_folder(self):
        """ Testing to move many files from parent folder
            new structure:
                ...
                |- GTX
                    |- TI
                        |- 1070 TI.png
                        |- 1080 TI.png
                ...
        """

        payload = {
            'parent_folder': self.ti_gtx.pk,
            'files_to_move': [self.f_1070_ti.pk, self.f_1080_ti.pk]
        }

        url_move_folder = reverse(URL_MOVE_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_move_folder, payload)

        new_parent_folder = Folder.get_by_id(self.ti_gtx.pk)
        file_1070_moved = File.get_by_id(self.f_1070_ti.pk)
        file_1080_moved = File.get_by_id(self.f_1080_ti.pk)
        media_path_1070 = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{file_1070_moved.get_full_name()}'
        media_path_1080 = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{file_1080_moved.get_full_name()}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertTrue(new_parent_folder.has_this_file(file_1070_moved.pk))
        self.assertTrue(new_parent_folder.has_this_file(file_1080_moved.pk))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_1070))
        self.assertTrue(os.path.exists(media_path_1080))

    def test_09_move_many_files_of_different_folders(self):
        """ Testing to move many files from parent folder
            new structure:
                ...
                |- NVIDIA
                    |- Series_1000.pdf
                    |- Series_2000.pdf
                    |- 2060 TI.png
                    |- 3070 TI.png
                    |- 1070 TI.png
                    |- 1080 TI.png
                    |- 2060.jpg
                    |- 1030.pdf
                ...
                |- RTX
                    |- TI
                |- GTX
                    |- TI
                ...
        """

        payload = {
            'parent_folder': self.nvidia.pk,
            'files_to_move': [self.f_2060.pk,
                            self.f_2060_ti.pk,
                            self.f_3060_ti.pk,
                            self.f_1030.pk]
        }

        url_move_folder = reverse(URL_MOVE_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_move_folder, payload)

        new_parent_folder = Folder.get_by_id(self.nvidia.pk)
        file_2060_moved = File.get_by_id(self.f_2060.pk)
        file_2060_ti_moved = File.get_by_id(self.f_2060_ti.pk)
        file_3060_moved = File.get_by_id(self.f_3060_ti.pk)
        file_1030_moved = File.get_by_id(self.f_1030.pk)

        media_path_2060 = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{file_2060_moved.get_full_name()}'
        media_path_2060_ti = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{file_2060_ti_moved.get_full_name()}'
        media_path_3060 = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{file_3060_moved.get_full_name()}'
        media_path_1030 = f'{settings.MEDIA_ROOT_TEST}{new_parent_folder.get_path_folder()}/{file_1030_moved.get_full_name()}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertTrue(new_parent_folder.has_this_file(file_2060_moved.pk))
        self.assertTrue(new_parent_folder.has_this_file(file_2060_ti_moved.pk))
        self.assertTrue(new_parent_folder.has_this_file(file_3060_moved.pk))
        self.assertTrue(new_parent_folder.has_this_file(file_1030_moved.pk))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_2060))
        self.assertTrue(os.path.exists(media_path_2060_ti))
        self.assertTrue(os.path.exists(media_path_3060))
        self.assertTrue(os.path.exists(media_path_1030))
