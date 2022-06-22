from urllib import response
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.users.models import User

URL_REGISTER = reverse('auth:register')
URL_LOGIN = reverse('auth:login')
URL_LOGOUT = reverse('auth:logout')

class LoginAPITestCase(APITestCase):

    def setUp(self):
        user_register = {
            "first_name": "Test",
            "last_name": "Testing",
            "username": "TT",
            "email": "Test@xyz.com",
            "password": "_:Tolomeo:_"
        }

        self.user = User.objects.create_user(**user_register)

    def test_login_successfully(self):

        response = self.client.post(URL_LOGIN, {'username':self.user.email, 'password':'_:Tolomeo:_'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    
    def test_login_wrong_user(self):

        response = self.client.post(URL_LOGIN, {'username':'bademail@xyz.com', 'password':'_:Tolomeo:_'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    
    def test_login_method_not_allowed(self):

        response = self.client.get(URL_LOGIN, {'username':self.user.email, 'password':'_:Tolomeo:_'})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertNotIn('token', response.data)


class LogoutTestCase(APITestCase):

    def setUp(self):
        user_register = {
            "first_name": "Test",
            "last_name": "Testing",
            "username": "TT",
            "email": "Test@xyz.com",
            "password": "_:Tolomeo:_"
        }

        self.user = User.objects.create_user(**user_register)
        self.token, _ = Token.objects.get_or_create(user=self.user)


    def test_logout_successfully(self):

        self.client.login(username=self.user.email, password="_:Tolomeo:_")
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post(URL_LOGOUT)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    
    def test_logout_authenticated(self):

        self.client.login(username=self.user.email, password="_:Tolomeo:_")
        
        response = self.client.post(URL_LOGOUT)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Token.objects.filter(user=self.user).exists())

    
    def test_logout_wrong_token(self):

        self.client.login(username=self.user.email, password="_:Tolomeo:_")
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + "testintesttestingtestesign")

        response = self.client.post(URL_LOGOUT)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Token.objects.filter(user=self.user).exists())

    
    def test_logout_method_not_allowed(self):

        self.client.login(username=self.user.email, password="_:Tolomeo:_")
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.get(URL_LOGOUT)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Token.objects.filter(user=self.user).exists())


    
            

