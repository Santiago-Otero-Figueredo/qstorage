from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import File
from apps.directories.test.files.test_crud import FileCRUDAPITest

import os.path

URL_DETAIL_FILE = 'directories:files-detail'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderUpdateTest(FileCRUDAPITest):

    def test_01_update_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'name': 'update_name',
        }

        url_detail_folder = reverse(URL_DETAIL_FILE, kwargs={'pk': self.f_budget.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.put(url_detail_folder, payload)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_update_folder_not_exists(self):
        """ Testing not update file if does not exists """

        payload = {
            'name': 'update_name',
        }

        url_detail_folder = reverse(URL_DETAIL_FILE, kwargs={'pk': 1000})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_detail_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_03_do_not_allow_duplicate_names(self):
        """ Testing that do not allow update name of an existing file in the folder parent"""

        update_data = {
            'name': 'linux'
        }

        url_update_folders = reverse(URL_DETAIL_FILE, kwargs={'pk': self.f_windows.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.patch(url_update_folders, update_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_04_update_name_leaf_file_in_root(self):
        """ Testing the update name and the update of paths of the leaf file in root
            new structure:
                |- / (root)
                    ...
                    |- linux_rename.pdf
        """

        update_data = {
            'name': 'linux_rename',
        }

        url_detail_folder = reverse(URL_DETAIL_FILE, kwargs={'pk': self.f_linux.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)

        update_file = File.objects.get(pk=self.f_linux.pk)

        media_path_new_file = update_file.get_full_path()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(update_file.name, 'linux_rename.pdf')
        self.assertTrue(self.root_folder.is_file_child(update_file.pk))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_new_file))

    def test_04_update_name_of_file_in_parent_folder(self):
        """ Testing the update name and the update of paths of the leaf file in root
            new structure:
                |- / (root)
                    ...
                    |- Hardware
                        ...
                        |- NVIDIA
                                |- Series_1000_old_gen.pdf
                                ...
        """

        update_data = {
            'name': 'Series_1000_old_gen',
        }

        url_detail_folder = reverse(URL_DETAIL_FILE, kwargs={'pk': self.f_series_2000.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)

        update_file = File.objects.get(pk=self.f_series_2000.pk)

        media_path_new_file = update_file.get_full_path()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Validation of change path in database
        self.assertEqual(update_file.name, 'Series_1000_old_gen.pdf')
        self.assertTrue(self.nvidia.is_file_child(update_file.pk))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_new_file))
