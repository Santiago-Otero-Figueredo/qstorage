from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.test.files.test_crud import FileCRUDAPITest


URL_DETAIL_FILE = 'directories:files-detail'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderListTest(FileCRUDAPITest):

    def test_01_list_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        url_detail_folder = reverse(URL_DETAIL_FILE, kwargs={'pk': self.f_series_1000.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.post(url_detail_folder)
        response_2 = self.client.put(url_detail_folder)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_02_list_folder_not_exists(self):
        """ Testing no list folder if does not exists """

        url_detail_folder = reverse(URL_DETAIL_FILE, kwargs={'pk': 1000})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_detail_folder)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_03_list_children_folders_in_root(self):
        """ Testing the get info of files """

        url_detail_folder = reverse(URL_DETAIL_FILE, kwargs={'pk': self.f_series_1000.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_detail_folder)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], 'Series_1000.pdf')
        self.assertEqual(data['file'], 'http://testserver/media/10/Hardware/GPU/NVIDIA/Series_1000.pdf')
        self.assertEqual(dict(data)['details']['type'], 'pdf')
        self.assertEqual(dict(data)['details']['size'], 143774)
