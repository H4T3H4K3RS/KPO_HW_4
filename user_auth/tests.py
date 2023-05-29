from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer

User = get_user_model()


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration(self):
        """
        Test user registration.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post('/api/user/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(pk=response.data['user_id'])
        self.assertEqual(user.username, 'testuser')

    def test_login(self):
        """
        Test user login.
        """
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post('/api/user/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_login_invalid_credentials(self):
        """
        Test user login with invalid credentials.
        """
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/user/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user(self):
        """
        Test retrieving user details.
        """
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/user/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
