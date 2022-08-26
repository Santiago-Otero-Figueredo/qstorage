from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status

from apps.directories.models import Folder
from apps.directories.test.files.test_crud import FileCRUDAPITest, upload_file_temporally

from rest_framework.authtoken.models import Token


URL_LIST_CHILDREN = 'directories:files-children-files'
URL_LIST_FILES = 'directories:files-list'
URL_DETAIL_FOLDER = 'directories:files-detail'
URL_MOVE_FOLDER = 'directories:files-move-files'
URL_MOVE_TO_RECICLE_BIN = 'directories:files-move-to-recycle-bin'
URL_RECOVER_FOLDER = 'directories:files-recover-files'
URL_DELETE_FOLDER = 'directories:files-delete-file'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class PermissionsAPITestCase(FileCRUDAPITest):

    @classmethod
    def setUpClass(cls) -> None:
        """
            Initial structure of directories for the testing
                ...
                |- 21/ (user_2)
                    |- user_2_test_1

        """
        super(PermissionsAPITestCase, cls).setUpClass()

        cls.user_2 = get_user_model().objects.create(
            pk=21,
            first_name='other test',
            last_name='another testing',
            username='OTTP',
            email='anothertestingpermission@xyz.com',
            password='contrasenia@123456'
        )

        cls.token_2, _ = Token.objects.get_or_create(user=cls.user_2)

        cls.root_folder_2 = Folder.get_root_folder_by_user(cls.user_2)
        cls.user_2_test_folder_1 = cls.root_folder_2.add_child(
            owner_user=cls.user_2,
            name='user_2_test_1',
            route='/'
        )

    def test_01_create_file_not_permissions(self):
        """ Testing the permissions for create file action.
        The user have to be the owner of the parent folder """

        payload = {
            'parent_folder': self.ti_gtx.pk,
            'file': upload_file_temporally('new_file.png')
        }

        url_list_children_folders = reverse(URL_LIST_FILES)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_2}')

        response = self.client.post(url_list_children_folders, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_02_update_name_not_permissions(self):
        """ Testing the permissions for update files action.
        The user have to be the owner of the file """

        payload = {
            'name': 'update_name',
        }

        url_update_folders = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.f_linux.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_2}')

        response = self.client.patch(url_update_folders, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_03_move_folder_not_user_owner(self):
        """ Testing the permissions for move folder. The user only can move
        if he is the owner of it """

        payload = {
            'parent_folder': self.user_2_test_folder_1.pk,
            'files_to_move': [self.f_linux.pk]
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_04_move_folder_to_recicle_bin_not_user_owner(self):
        """ Testing the permissions for move folder to recicle bin. The user only can move
        if he is the owner of it """

        payload = {
            'files_to_disable': [self.f_linux.pk]
        }

        url_move_folder = reverse(URL_MOVE_TO_RECICLE_BIN)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_2}')

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_05_recover_folder_not_user_owner(self):
        """ Testing the permissions for recover folder. The user only can move
        if he is the owner of it """

        payload = {
            'files_to_recover': [self.f_linux.pk]
        }

        url_recover_folder = reverse(URL_RECOVER_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_2}')

        response = self.client.patch(url_recover_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_06_delete_folder_not_user_owner(self):
        """ Testing the permissions for delete folder. The user only can move
        if he is the owner of it """

        payload = {
            'files_to_delete': [self.f_linux.pk]
        }

        url_delete_folder = reverse(URL_DELETE_FOLDER)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_2}')

        response = self.client.delete(url_delete_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
