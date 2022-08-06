from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.test.test_crud import FolderCRUDAPITest

URL_LIST_CHILDREN = 'directories:folders-children-folders'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderListTest(FolderCRUDAPITest):

    def test_01_list_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        url_list_folder = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.root_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.post(url_list_folder)
        response_2 = self.client.delete(url_list_folder)
        response_3 = self.client.put(url_list_folder)
        response_4 = self.client.patch(url_list_folder)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_4.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_list_folder_not_exists(self):
        """ Testing no list folder if does not exists """

        url_list_folder = reverse(URL_LIST_CHILDREN, kwargs={'pk': 1000})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_list_folder)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_03_list_children_folders_in_root(self):
        """ Testing the list of children folders in root """

        url_list_folder = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.root_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_list_folder)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Hardware')
        self.assertEqual(response.data[1]['name'], 'Operative system')

    def test_04_list_children_folders_in_parent_folder(self):
        """ Testing the list of children folders in parent folder """

        url_list_folder = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.hardware.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_list_folder)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Budget')
        self.assertEqual(response.data[1]['name'], 'CPU')
        self.assertEqual(response.data[2]['name'], 'GPU')
        self.assertEqual(response.data[3]['name'], 'Memories')
        self.assertEqual(response.data[4]['name'], 'Peripherals')
        self.assertEqual(response.data[5]['name'], 'Storage')

    def test_05_list_children_folders_in_child_of_parent_folder(self):
        """ Testing the list of children folders in root """

        url_list_folder = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.gpu.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_list_folder)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'AMD')
        self.assertEqual(response.data[1]['name'], 'GTX')
        self.assertEqual(response.data[2]['name'], 'NVIDIA')
        self.assertEqual(response.data[3]['name'], 'RTX')

    def test_06_list_children_folders_in_last_child_of_parent_folder(self):
        """ Testing the list of children folders in last child of parent folder """

        url_list_folder = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.ti_rtx.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_list_folder)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], '1070 TI')
        self.assertEqual(response.data[1]['name'], '1080 TI')
        self.assertEqual(response.data[2]['name'], '2060 TI')
        self.assertEqual(response.data[3]['name'], '3070 TI')

    def test_07_list_folders_without_children_folders(self):
        """ Testing the list of a folders without children folders """

        url_list_folder = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.ram.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_list_folder)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 0)
