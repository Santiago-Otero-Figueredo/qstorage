from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import Folder
from apps.directories.test.test_crud import FolderCRUDAPITest

import os.path

URL_CREATE_FOLDER = 'directories:folders-create-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderCreateTest(FolderCRUDAPITest):

    def test_01_create_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'name': 'new',
        }

        url_create_folder = reverse(URL_CREATE_FOLDER, kwargs={'pk': self.root_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.get(url_create_folder, payload)
        response_2 = self.client.delete(url_create_folder, payload)
        response_3 = self.client.put(url_create_folder, payload)
        response_4 = self.client.patch(url_create_folder, payload)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_4.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_create_folder_not_exists(self):
        """ Testing not create folder if does not exists """

        payload = {
            'name': 'new',
        }

        url_create_folder = reverse(URL_CREATE_FOLDER, kwargs={'pk': 1000})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.post(url_create_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_03_create_folder_in_root(self):
        """ Testing the creation of a folder in the root folder """
        payload = {
            'name': 'Software',
        }

        url_create_folder = reverse(URL_CREATE_FOLDER, kwargs={'pk': self.root_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_create_folder, payload)

        parent_folder = Folder.get_by_id(self.root_folder.pk)
        child_folder = Folder.objects.get(name='Software')

        media_path_new_folder = f'{settings.MEDIA_ROOT_TEST}{parent_folder.get_path_folder()}/{child_folder.name}'

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # Validation of change path in database
        self.assertEqual(child_folder.get_parent().name, parent_folder.name)
        self.assertEqual(child_folder.get_path_parent_folder(), parent_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(child_folder.is_child_of(parent_folder))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_new_folder))

    def test_04_create_folder_in_child_folder(self):
        """ Testing the creation of a folder inside another folder other than root folder """
        payload = {
            'name': 'Series 500',
        }

        url_create_folder = reverse(URL_CREATE_FOLDER, kwargs={'pk': self.g_amd.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_create_folder, payload)

        parent_folder = Folder.objects.get(pk=self.g_amd.pk)
        hardware_folder = Folder.objects.get(pk=self.hardware.pk)
        child_folder = Folder.objects.get(name='Series 500')

        media_path_new_folder = f'{settings.MEDIA_ROOT_TEST}{parent_folder.get_path_folder()}/{child_folder.name}'

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # Validation of change path in database
        self.assertEqual(child_folder.get_parent().name, parent_folder.name)
        self.assertEqual(child_folder.get_path_parent_folder(), parent_folder.get_path_folder())
        # Validation of changes in inheritance database
        self.assertTrue(child_folder.is_child_of(parent_folder))
        self.assertTrue(child_folder.is_descendant_of(hardware_folder))
        # Validation of folders move in media folder
        self.assertTrue(os.path.exists(media_path_new_folder))
