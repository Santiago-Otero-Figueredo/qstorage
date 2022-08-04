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
URL_MOVE_TO_RECICLE_BIN = 'directories:folders-move-to-recycle-bin'
URL_RECOVER_FOLDER = 'directories:folders-recover-folder'
URL_DELETE_FOLDER = 'directories:folders-delete-folder'


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class AuthenticationAPITestCase(APITestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
            Initial structure of directories for the testing
                |- / (root)
                    |- user_1_test_1
                        |- user_1_test_1_nested
                        |- user_1_test_2_nested
                    |- user_1_test_2
                    |- user_1_test_3
        """
        super(AuthenticationAPITestCase, cls).setUpClass()
        cls.user_1 = get_user_model().objects.create(
            pk=10,
            first_name='test',
            last_name='testing',
            username='TT1',
            email='testing1@xyz.com',
            password='contrasenia@123456'
        )

        cls.token_1, _ = Token.objects.get_or_create(user=cls.user_1)

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

    def test_01_list_children_folders_not_authenticated(self):
        """ Testing the authorization for access to the list children folder function.
        The user have to be log in """

        url_list_children_folders = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.root_folder_1.pk})

        response = self.client.get(url_list_children_folders)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_02_create_folders_not_authenticated(self):
        """ Testing the authorization for create folder action. The user have to be log in """

        payload = {
            'name': 'folder_test_nested',
            'owner_user': self.user_1.pk
        }

        url_list_children_folders = reverse(URL_CREATE_FOLDER, kwargs={'pk': self.root_folder_1.pk})

        response = self.client.post(url_list_children_folders, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_03_update_name_not_authenticated(self):
        """ Testing the authorization for update folder action. The user have to be log in """

        update_data = {
            'name': 'update_name'
        }

        url_update_folders = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.root_folder_1.pk})

        response = self.client.patch(url_update_folders, update_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_04_move_folder_not_authenticated(self):
        """ Testing the authorization for move folder action. The user have to be log in """

        payload = {
            'folders_to_move': [self.user_1_nested_test_folder_2.pk],
            'new_parent_folder': self.user_1_test_folder_1.pk
        }

        url_move_folder = reverse(URL_MOVE_FOLDER)

        response = self.client.patch(url_move_folder, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_05_move_folder_to_recicle_bin_authenticated(self):
        """ Testing the authorization for move folder to recicle bin action. The user have to be log in """

        url_move_folder = reverse(
            URL_MOVE_TO_RECICLE_BIN,
            kwargs={'pk': self.user_1_nested_test_folder_2.pk}
        )

        response = self.client.patch(url_move_folder)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_06_move_folder_to_recover_folder_authenticated(self):
        """ Testing the authorization for recover folder action. The user have to be log in """

        url_recover_folder = reverse(
            URL_RECOVER_FOLDER,
            kwargs={'pk': self.user_1_nested_test_folder_2.pk}
        )

        response = self.client.patch(url_recover_folder)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_07_delete_folder_authenticated(self):
        """ Testing the authorization for delete folder action. The user have to be log in """

        url_delete_folder = reverse(
            URL_DELETE_FOLDER,
            kwargs={'pk': self.user_1_nested_test_folder_2.pk}
        )

        response = self.client.delete(url_delete_folder)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @classmethod
    def tearDownClass(cls):
        """ Remove the test file in media"""
        super(AuthenticationAPITestCase, cls).tearDownClass()
        rmtree(settings.MEDIA_ROOT_TEST, ignore_errors=True)
