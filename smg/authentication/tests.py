from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import User


class SigninTestCase(TestCase):
    user_data = {
        'username': 'test.account',
        'password': 'strong-password',
        'email': 'test-account@example.com',
        'skype': 'test.account',
        'phone': '+384732847',
        'birthday': datetime(year=1994, month=12, day=15),
        'employment_date': datetime(year=2015, month=10, day=22),
        'first_name': 'Test',
        'last_name': 'Test',
        'patronymic': 'Test'
    }

    def setUp(self):
        self.user = User.objects.create(**self.user_data)

    def test_returns_existing_token_and_user(self):
        token = Token.objects.create(user=self.user)
        response = self.client.post(reverse('auth:sign_in'),
                                    data={
                                        'username': self.user_data['username'],
                                        'password': self.user_data['password']
                                    })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['token'], token.key)
        self.assertIn('id', response.data)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_creates_new_token(self):
        response = self.client.post(reverse('auth:sign_in'),
                                    data={
                                        'username': self.user_data['username'],
                                        'password': self.user_data['password']
                                    })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertTrue(response.data['token'])
        self.assertIn('id', response.data)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_returns_400_for_non_existent_user(self):
        response = self.client.post(reverse('auth:sign_in'),
                                    data={
                                        'username': self.user_data['username'][:-1],
                                        'password': self.user_data['password']
                                    })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AccountsTestCase(TestCase):
    pass
