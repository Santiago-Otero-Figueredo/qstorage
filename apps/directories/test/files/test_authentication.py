from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.test.files.test_crud import FileCRUDAPITest, upload_file_temporally


URL_LIST_FILES_FOLDER = 'directories:files-list-files'
URL_CREATE_LIST_FILES = 'directories:files-list'
URL_DETAIL_FILE = 'directories:files-detail'
URL_MOVE_FILES = 'directories:files-move-files'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class AuthenticationAPITestCase(FileCRUDAPITest):

    def test_01_list_children_files_not_authenticated(self):
        """ Testing the authorization for access to the list files in folder function.
        The user have to be log in """

        payload = {
            'parent_folder': self.root_folder.pk,
        }

        url_list_children_folders = reverse(URL_LIST_FILES_FOLDER)

        response = self.client.get(url_list_children_folders, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_02_create_files_not_authenticated(self):
        """ Testing the authorization for create file action. The user have to be log in """

        payload = {
            'parent_folder': self.root_folder.pk,
            'file': upload_file_temporally('Mouse.png')
        }

        url_list_children_folders = reverse(URL_CREATE_LIST_FILES)

        response = self.client.post(url_list_children_folders, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_03_update_name_not_authenticated(self):
        """ Testing the authorization for update file action. The user have to be log in """

        update_data = {
            'name': 'update_name'
        }

        url_update_folders = reverse(URL_DETAIL_FILE, kwargs={'pk': self.f_windows.pk})

        response = self.client.patch(url_update_folders, update_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_04_move_file_not_authenticated(self):
        """ Testing the authorization for move files action. The user have to be log in """

        payload = {
            'parent_folder': [self.storage.pk],
            'files_to_move': [self.f_windows.pk, self.f_linux.pk]
        }

        url_move_folder = reverse(URL_MOVE_FILES)

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_05_move_file_to_recicle_bin_authenticated(self):
    #     """ Testing the authorization for move files to recicle bin action. The user have to be log in """

    #     payload = {
    #         'folders_to_disable': [self.user_1_nested_test_file_2.pk]
    #     }

    #     url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)
    #     response = self.client.patch(url_move_folder, payload)

    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_06_move_file_to_recover_file_authenticated(self):
    #     """ Testing the authorization for recover files action. The user have to be log in """

    #     payload = {
    #         'folders_to_recover': [self.user_1_nested_test_file_2.pk]
    #     }

    #     url_recover_folder = reverse(URL_RECOVER_FOLDER)
    #     response = self.client.patch(url_recover_folder, payload)

    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_07_delete_file_authenticated(self):
    #     """ Testing the authorization for delete files action. The user have to be log in """

    #     payload = {
    #         'folders_to_delete': [self.user_1_nested_test_file_2.pk]
    #     }

    #     url_delete_folder = reverse(URL_DELETE_FOLDER)

    #     response = self.client.delete(url_delete_folder, payload)

    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
