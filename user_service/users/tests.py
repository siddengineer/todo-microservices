from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class AuthTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="sid",
            password="1234"
        )

    def test_login_returns_token(self):
        response = self.client.post('/api/login/', {
            "username": "sid",
            "password": "1234"
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_token_contains_custom_fields(self):
        response = self.client.post('/api/login/', {
            "username": "sid",
            "password": "1234"
        }, format='json')

        token = response.data['access']

        # decode token (simple way)
        from rest_framework_simplejwt.tokens import AccessToken
        decoded = AccessToken(token)

        self.assertIn('username', decoded)
        self.assertIn('role', decoded)