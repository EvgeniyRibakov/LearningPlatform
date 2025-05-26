from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import CustomUser


class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'TestPass123',
            'role': 'student'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'testuser')

    def test_register_invalid_data(self):
        data = {
            'username': '',
            'email': 'invalid',
            'password': 'short',
            'role': 'invalid'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
