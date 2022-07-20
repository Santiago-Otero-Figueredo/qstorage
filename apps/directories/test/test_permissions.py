from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.directories.models import Folder

from shutil import rmtree

URL_CREATE_FOLDER = 'directories:folders-create-folder'
URL_LIST_CHILDREN = 'directories:folders-children-folders'
URL_DETAIL_FOLDER = 'directories:folders-detail'
URL_MOVE_FOLDER = 'directories:folders-move-folder'

@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class PermissionsAPITestCase(APITestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
            Initial structure of directories for the testing
                |- 20/ (user_1)
                    |- user_1_test_1
                        |- user_1_test_1_nested
                        |- user_1_test_2_nested
                    |- user_1_test_2
                    |- user_1_test_3
                |- 21/ (user_2)
                    |- user_2_test_1

        """
        super(PermissionsAPITestCase, cls).setUpClass()
        cls.user_1 = get_user_model().objects.create(
            pk=20,
            first_name='test',
            last_name='testing',
            username='TTP',
            email='testingpermissions@xyz.com',
            password='contrasenia@123456'
        )

        cls.user_2 = get_user_model().objects.create(
            pk=21,
            first_name='other test',
            last_name='another testing',
            username='OTTP',
            email='anothertestingpermission@xyz.com',
            password='contrasenia@123456'
        )

        cls.token_1, _ = Token.objects.get_or_create(user=cls.user_1)
        cls.token_2, _ = Token.objects.get_or_create(user=cls.user_2)

        cls.root_folder_1 = Folder.get_root_folder_by_user(cls.user_1)
        cls.user_1_test_folder_1 = cls.root_folder_1.add_child(
            owner_user=cls.user_1,
            name='user_1_test_1',
            route='/'
        )
        cls.user_1_test_folder_2 = cls.root_folder_1.add_child(
            owner_user=cls.user_1,
            name='user_1_test_2',
            route='/'
        )
        cls.user_1_test_folder_3 = cls.root_folder_1.add_child(
            owner_user=cls.user_1,
            name='user_1_test_3',
            route='/'
        )

        cls.user_1_nested_test_folder_1 = cls.user_1_test_folder_1.add_child(
            owner_user=cls.user_1,
            name='user_1_test_1_nested',
            route='/'
        )
        cls.user_1_nested_test_folder_2 = cls.user_1_test_folder_1.add_child(
            owner_user=cls.user_1,
            name='user_1_test_2_nested',
            route='/'
        )

        cls.root_folder_2 = Folder.get_root_folder_by_user(cls.user_2)
        cls.user_2_test_folder_1 = cls.root_folder_2.add_child(
            owner_user=cls.user_2,
            name='user_2_test_1',
            route='/'
        )

    def test_list_children_folders_not_permissions(self):
        """ Testing the permissions for list children folder action.
        The user have to be the owner of the parent folder """

        url_list_children_folders = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.root_folder_1.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_2}')

        response = self.client.get(url_list_children_folders)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_folders_not_permissions(self):
        """ Testing the permissions for create folder action.
        The user have to be the owner of the parent folder """

        payload = {
            'name': 'folder_test_nested',
            'owner_user': self.user_1.pk
        }

        url_list_children_folders = reverse(URL_CREATE_FOLDER, kwargs={'pk': self.root_folder_1.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_2}')

        response = self.client.post(url_list_children_folders, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_name_not_permissions(self):
        """ Testing the permissions for update folder action.
        The user have to be the owner of the parent folder """

        update_data = {
            'name': 'update_name'
        }

        url_update_folders = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.root_folder_1.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_2}')

        response = self.client.patch(url_update_folders, update_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_root_name_not_permissions(self):
        """ Testing the permissions for update the root folder action.
        The user can not modify this folder even if he is the owner """

        update_data = {
            'name': 'update_name'
        }

        url_update_folders = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.root_folder_1.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_1}')

        response = self.client.patch(url_update_folders, update_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_move_folder_not_user_owner(self):
        """ Testing the permissions for move folder. The user only can move
        if he is the owner of it """

        payload = {
            'new_parent_folder': self.user_2_test_folder_1.pk
        }

        url_move_folder = reverse(
            URL_MOVE_FOLDER,
            kwargs={'pk': self.user_1_test_folder_1.pk}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_1}')

        response = self.client.post(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @classmethod
    def tearDownClass(cls):
        """ Remove the test file in media"""
        super(PermissionsAPITestCase, cls).tearDownClass()
        rmtree(settings.MEDIA_ROOT_TEST, ignore_errors=True)
