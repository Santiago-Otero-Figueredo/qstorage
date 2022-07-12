from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.directories.models import Folder

from shutil import rmtree

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
        cls.nested_test_folder = cls.test_folder.add_child(owner_user=cls.user, name='test_1_nested', route='/')


    def test_create_folder_in_root(self):
        payload = {
            'name':'folder_test',
            'owner_user':self.user.pk
        }

        URL_LIST_CREATE_FOLDER = reverse('directories:folders-create-folder', kwargs={'pk':self.root_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(URL_LIST_CREATE_FOLDER, payload)

        child_folder = Folder.objects.get(name='folder_test')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(child_folder.is_child_of(self.root_folder))
    

    def test_create_folder_in_child_folder(self):
        payload = {
            'name':'folder_test_nested',
            'owner_user':self.user.pk
        }

        URL_LIST_CREATE_FOLDER = reverse('directories:folders-create-folder', kwargs={'pk':self.test_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(URL_LIST_CREATE_FOLDER, payload)        

        child_folder = Folder.objects.get(name='folder_test_nested')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(child_folder.is_child_of(self.test_folder))
        self.assertEqual(child_folder.route, '1/test_1/')

    
    def test_update_name_file(self):
        
        update_data = {
            'name':'update_name',
        }

        URL_DIRECTORIES_CRUD = reverse('directories:folders-detail', kwargs={'pk':self.test_folder.pk})

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(URL_DIRECTORIES_CRUD, update_data)

        child_folder = Folder.objects.get(name='test_1_nested')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.root_folder.get_first_child().name, 'update_name')
        self.assertEqual(child_folder.route, '1/update_name/')
        self.assertTrue(child_folder.is_child_of(self.root_folder.get_first_child()))
        

    @classmethod
    def tearDownClass(cls):
       super(FolderCRUDAPITest, cls).tearDownClass()
       """ Remove test file in media"""
       rmtree(settings.MEDIA_ROOT_TEST, ignore_errors=True)
# Create your tests here.
