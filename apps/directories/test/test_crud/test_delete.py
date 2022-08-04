from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import Folder
from apps.directories.test.test_crud import FolderCRUDAPITest

import os.path

URL_DELETE_FOLDER = 'directories:folders-delete-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderRecicleBinTest(FolderCRUDAPITest):

    def test_01_move_recicle_bin_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        url_move_folder = reverse(
            URL_DELETE_FOLDER,
            kwargs={'pk': self.hardware.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.post(url_move_folder)
        response_2 = self.client.get(url_move_folder)
        response_3 = self.client.put(url_move_folder)
        response_4 = self.client.patch(url_move_folder)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_4.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_move_recicle_bin_folder_not_exists(self):
        """ Testing no list folder if does not exists """

        url_move_folder = reverse(
            URL_DELETE_FOLDER,
            kwargs={'pk': 1000}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.delete(url_move_folder)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_03_not_allow_delete_root_folder(self):
        """ Testing that the root folder can't be deleted even by the owner """

        url_move_folder = reverse(
            URL_DELETE_FOLDER,
            kwargs={'pk': self.root_folder.pk}
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.delete(url_move_folder)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_04_delete_leaf_folder(self):
        """ Testing the delete folder and children """

        url_move_folder = reverse(
            URL_DELETE_FOLDER,
            kwargs={'pk': self.operative_system.pk}
        )

        media_path_folder = f'{settings.MEDIA_ROOT_TEST}{self.operative_system.get_path_folder()}'

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url_move_folder)

        folder_deleted = Folder.get_by_id(self.operative_system.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Validation of deleting folder in database
        self.assertIsNone(folder_deleted)
        # Validation of deleting folders move in media folder
        self.assertFalse(os.path.exists(media_path_folder))


    def test_05_delete_parent_folder(self):
        """ Testing the delete folder and children """

        url_move_folder = reverse(
            URL_DELETE_FOLDER,
            kwargs={'pk': self.cpu.pk}
        )

        media_path_cpu_folder = f'{settings.MEDIA_ROOT_TEST}{self.cpu.get_path_folder()}'
        media_path_intel_folder = f'{settings.MEDIA_ROOT_TEST}{self.intel.get_path_folder()}'
        media_path_i5_folder = f'{settings.MEDIA_ROOT_TEST}{self.i5.get_path_folder()}'
        media_path_i3_folder = f'{settings.MEDIA_ROOT_TEST}{self.i3.get_path_folder()}'
        media_path_i7_folder = f'{settings.MEDIA_ROOT_TEST}{self.i7.get_path_folder()}'
        media_path_c_amd_folder = f'{settings.MEDIA_ROOT_TEST}{self.c_amd.get_path_folder()}'
        media_path_r_2600_folder = f'{settings.MEDIA_ROOT_TEST}{self.r_2600.get_path_folder()}'
        media_path_r_3600_folder = f'{settings.MEDIA_ROOT_TEST}{self.r_3600.get_path_folder()}'
        media_path_r_3700_folder = f'{settings.MEDIA_ROOT_TEST}{self.r_3700.get_path_folder()}'

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url_move_folder)

        test_parent_folder = Folder.get_by_id(self.operative_system.pk)


        cpu_deleted = Folder.get_by_id(self.cpu.pk)
        intel_deleted = Folder.get_by_id(self.intel.pk)
        i5_deleted = Folder.get_by_id(self.i5.pk)
        i3_deleted = Folder.get_by_id(self.i3.pk)
        i7_deleted = Folder.get_by_id(self.i7.pk)
        c_amd_deleted = Folder.get_by_id(self.c_amd.pk)
        r_2600_deleted = Folder.get_by_id(self.r_2600.pk)
        r_3600_deleted = Folder.get_by_id(self.r_3600.pk)
        r_3700_deleted = Folder.get_by_id(self.r_3700.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Validation of deleting folder in database
        self.assertIsNone(cpu_deleted)
        self.assertIsNone(intel_deleted)
        self.assertIsNone(i5_deleted)
        self.assertIsNone(i3_deleted)
        self.assertIsNone(i7_deleted)
        self.assertIsNone(c_amd_deleted)
        self.assertIsNone(r_2600_deleted)
        self.assertIsNone(r_3600_deleted)
        self.assertIsNone(r_3700_deleted)
        # Validation of deleting folders move in media folder
        self.assertFalse(os.path.exists(media_path_cpu_folder))
        self.assertFalse(os.path.exists(media_path_intel_folder))
        self.assertFalse(os.path.exists(media_path_i5_folder))
        self.assertFalse(os.path.exists(media_path_i3_folder))
        self.assertFalse(os.path.exists(media_path_i7_folder))
        self.assertFalse(os.path.exists(media_path_c_amd_folder))
        self.assertFalse(os.path.exists(media_path_r_2600_folder))
        self.assertFalse(os.path.exists(media_path_r_3600_folder))
        self.assertFalse(os.path.exists(media_path_r_3700_folder))




