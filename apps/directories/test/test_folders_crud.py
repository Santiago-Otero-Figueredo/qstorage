from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.directories.models import Folder

from django.conf import settings

#URL_LIST_CREATE_FOLDER = reverse('directories:create-folder')
#URL_DETAIL_FOLDER = reverse('directories:folders-detail')


@override_settings(MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class FolderCRUDAPITest(APITestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            first_name='test',
            last_name='testing',
            username='TT',
            email='testing@xyz.com',
            password='contrasenia@123456'
        )

        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.root_folder = Folder.get_root_folder_by_user(self.user)
        self.test_folder = self.root_folder.add_child(owner_user=self.user, name='test_1', route=2)


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

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(URL_LIST_CREATE_FOLDER, payload)        

        child_folder = Folder.objects.get(name='folder_test_nested')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(child_folder.is_child_of(self.test_folder))
        self.assertEqual(child_folder.route, '1/test_1/')

# Create your tests here.
