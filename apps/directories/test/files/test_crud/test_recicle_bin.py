from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.test.files.test_crud import FileCRUDAPITest


URL_MOVE_TO_RECICLE_BIN = 'directories:folder-move-to-recycle-bin'
URL_RECOVER_FOLDER = 'directories:files-recover-files'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderRecicleBinTest(FileCRUDAPITest):

    def test_01_move_recicle_bin_folder_method_not_allowed(self):
        """ Testing not allow methods in function """

        payload = {
            'files_to_disable': [self.f_s_linux.pk]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response_1 = self.client.post(url_move_folder, payload)
        response_2 = self.client.get(url_move_folder, payload)
        response_3 = self.client.put(url_move_folder, payload)
        response_4 = self.client.delete(url_move_folder, payload)

        self.assertEqual(response_1.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_2.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_3.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_4.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
