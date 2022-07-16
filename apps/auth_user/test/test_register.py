from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from apps.directories.models import Folder


URL_REGISTER = reverse('auth:register')


class RegisterAPITestCase(APITestCase):

    def test_register_successfully(self):
        user_register = {
            "first_name": "Test",
            "last_name": "Testing",
            "username": "TT",
            "email": "Test@xyz.com",
            "password": "_:Tolomeo:_",
            "password2": "_:Tolomeo:_"
        }

        response = self.client.post(URL_REGISTER, user_register)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data['value'])
        self.assertTrue(response.data['success'])

    def test_register_duplicate(self):
        user_register = {
            "first_name": "Test",
            "last_name": "Testing",
            "username": "TT",
            "email": "Test@xyz.com",
            "password": "_:Tolomeo:_",
            "password2": "_:Tolomeo:_"
        }

        self.client.post(URL_REGISTER, user_register)
        response = self.client.post(URL_REGISTER, user_register)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data['value'])
        self.assertFalse(response.data['success'])

    def test_register_required_fields(self):
        user_register = {
            "first_name": "Test",
            "last_name": "Testing",
            "username": "TT",
            "email": "",
            "password": "_:Tolomeo:_",
            "password2": "_:Tolomeo:_"
        }

        response = self.client.post(URL_REGISTER, user_register)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data['value'])
        self.assertFalse(response.data['success'])

    def test_register_different_passwords(self):
        user_register = {
            "first_name": "Test",
            "last_name": "Testing",
            "username": "TT",
            "email": "",
            "password": "_:Tolomeo:_",
            "password2": "paswword2"
        }

        response = self.client.post(URL_REGISTER, user_register)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data['value'])
        self.assertFalse(response.data['success'])

    def test_register_method_not_allowed(self):
        user_register = {
            "first_name": "Test",
            "last_name": "Testing",
            "username": "TT",
            "email": "",
            "password": "_:Tolomeo:_",
            "password2": "_:Tolomeo:_"
        }

        response = self.client.get(URL_REGISTER, user_register)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_register_successfully_root_folder(self):
        user_register = {
            "first_name": "Test2",
            "last_name": "Testing2",
            "username": "TT2",
            "email": "Test2@xyz.com",
            "password": "_:Tolomeo:_",
            "password2": "_:Tolomeo:_"
        }

        response = self.client.post(URL_REGISTER, user_register)

        user = get_user_model().get_user_by_email('Test2@xyz.com')
        root_folder = Folder.get_root_folder_by_user(user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(root_folder.is_root())
