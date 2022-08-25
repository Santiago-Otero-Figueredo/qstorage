from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import File, Folder
from apps.directories.test.files.test_crud import FileCRUDAPITest, upload_file_temporally

import os.path

URL_LIST_FILE = 'directories:files-list'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderCreateTest(FileCRUDAPITest):

    def test_01_create_file_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'parent_folder': self.software.pk,
            'file': upload_file_temporally('new_file.png')
        }

        url_create_folder = reverse(URL_LIST_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.delete(url_create_folder, payload)
        response_2 = self.client.put(url_create_folder, payload)
        response_3 = self.client.patch(url_create_folder, payload)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_create_file_folder_not_exists(self):
        """ Testing not create folder if does not exists """

        payload = {
            'parent_folder': [1000],
            'file': upload_file_temporally('new_file.png')
        }

        url_create_folder = reverse(URL_LIST_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_create_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_03_create_file_in_leaf_folder(self):
        """ Testing the creation of a file in leaf folder """

        payload = {
            'parent_folder': self.software.pk,
            'file': upload_file_temporally("new_file.pdf")
        }

        url_create_folder = reverse(URL_LIST_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_create_folder, payload, format='multipart'
        )

        parent_folder = Folder.get_by_id(self.software.pk)

        media_path_new_file = f'{settings.MEDIA_ROOT_TEST}{parent_folder.get_path_folder()}/new_file.pdf'

        new_file = File.get_all_files_by_user_and_name(self.user, 'new_file.pdf').first()

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # Validation of change path in database
        self.assertTrue(parent_folder.is_file_child(new_file.pk))
        self.assertTrue(File.get_all_files_by_user_and_name(self.user, 'new_file.pdf').exists())
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_new_file))

    def test_04_create_file_in_parent_folder(self):
        """ Testing the creation of a folder inside another folder other than root folder """
        payload = {
            'parent_folder': self.nvidia.pk,
            'file': upload_file_temporally("new_file.pdf")
        }

        url_create_folder = reverse(URL_LIST_FILE)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_create_folder, payload, format='multipart'
        )

        parent_folder = Folder.get_by_id(self.nvidia.pk)

        media_path_new_file = f'{settings.MEDIA_ROOT_TEST}{parent_folder.get_path_folder()}/new_file.pdf'

        new_file = File.get_all_files_by_user_and_name(self.user, 'new_file.pdf').first()

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # Validation of change path in database
        self.assertTrue(parent_folder.is_file_child(new_file.pk))
        self.assertTrue(File.get_all_files_by_user_and_name(self.user, 'new_file.pdf').exists())
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_new_file))
