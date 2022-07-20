from django.contrib.auth import get_user_model
from django.conf import settings
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


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderCRUDAPITest(APITestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super(FolderCRUDAPITest, cls).setUpClass()
        cls.user = get_user_model().objects.create(
            pk=1,
            first_name='test',
            last_name='testing',
            username='TT',
            email='testing@xyz.com',
            password='contrasenia@123456'
        )

        cls.token, _ = Token.objects.get_or_create(user=cls.user)
        cls.root_folder = Folder.get_root_folder_by_user(cls.user)
        cls.test_folder = cls.root_folder.add_child(owner_user=cls.user, name='test_1', route='/')

        cls.root_folder.add_child(owner_user=cls.user, name='test_2', route='/')
        cls.root_folder.add_child(owner_user=cls.user, name='test_file', route='/')

        cls.nested_test_folder = cls.test_folder.add_child(owner_user=cls.user, name='test_1_nested', route='/')
        cls.nested_test_folder = cls.test_folder.add_child(owner_user=cls.user, name='test_2_nested', route='/')

    def test_create_folder_in_root(self):
        """ Testing the creation of a folder in the root folder """
        payload = {
            'name': 'folder_test',
            'owner_user': self.user.pk
        }

        url_create_folder = reverse(URL_CREATE_FOLDER, kwargs={'pk': self.root_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url_create_folder, payload)

        child_folder = Folder.objects.get(name='folder_test')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(child_folder.is_child_of(self.root_folder))

    def test_create_folder_in_child_folder(self):
        """ Testing the creation of a folder inside another folder other than root folder """
        payload = {
            'name': 'folder_test_nested',
            'owner_user': self.user.pk
        }

        url_create_folder = reverse(URL_CREATE_FOLDER, kwargs={'pk': self.test_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url_create_folder, payload)

        child_folder = Folder.objects.get(name='folder_test_nested')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(child_folder.is_child_of(self.test_folder))
        self.assertEqual(child_folder.route, '1/test_1/')

    def test_update_name_file(self):
        """ Testing the update name and the update of paths of the children folders """

        update_data = {
            'name': 'update_name',
        }

        url_detail_folder = reverse(URL_DETAIL_FOLDER, kwargs={'pk': self.test_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(url_detail_folder, update_data)

        child_folder = Folder.objects.get(name='test_1_nested')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.root_folder.get_first_child().name, 'update_name')
        self.assertEqual(child_folder.route, '1/update_name/')
        self.assertTrue(child_folder.is_child_of(self.root_folder.get_first_child()))

    def test_no_exists_pk_folder(self):
        """ Testing a pk folder that does not exists """

        url_list_children = reverse(URL_LIST_CHILDREN, kwargs={'pk': 100})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(url_list_children)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_children_folders_in_root(self):
        """ Testing the list of children folders in root """

        url_list_children = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.root_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_list_children)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'test_1')
        self.assertEqual(response.data[1]['name'], 'test_2')
        self.assertEqual(response.data[2]['name'], 'test_file')

    def test_list_children_folders_in_nested_folder(self):
        """ Testing the list of children folders in another folder different of root """

        url_list_children = reverse(URL_LIST_CHILDREN, kwargs={'pk': self.test_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(url_list_children)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'test_1_nested')
        self.assertEqual(response.data[1]['name'], 'test_2_nested')

    @classmethod
    def tearDownClass(cls):
        """ Remove the test file in media"""
        super(FolderCRUDAPITest, cls).tearDownClass()
        rmtree(settings.MEDIA_ROOT_TEST, ignore_errors=True)
# Create your tests here.
