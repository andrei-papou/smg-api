import json
from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from common.factories import UserFactory, DepartmentFactory
from .models import User


class SigninTestCase(APITestCase):
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


class AccountsTestCase(APITestCase):

    def setUp(self):
        self.department1 = DepartmentFactory()
        self.department2 = DepartmentFactory()
        self.accounts = []
        for i in range(10):
            self.accounts.append(UserFactory(department=self.department1))
        for i in range(5):
            self.accounts.append(UserFactory(department=self.department2))

    def test_returns_department_accounts_for_non_manager(self):
        me = UserFactory(department=self.department2)
        self.client.force_authenticate(user=me)
        response = self.client.get(reverse('auth:accounts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_returns_all_accounts_to_manager(self):
        me = UserFactory(department=self.department2, is_manager=True)
        self.client.force_authenticate(user=me)
        response = self.client.get(reverse('auth:accounts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 16)

    def test_returns_400_to_anon(self):
        response = self.client.get(reverse('auth:accounts'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_self(self):
        new_name = 'Carl'
        me = UserFactory(department=self.department2)
        self.client.force_authenticate(user=me)
        response = self.client.patch(reverse('auth:accounts-detail', kwargs={'pk': me.pk}),
                                     data=json.dumps({'first_name': new_name}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        me.refresh_from_db()
        self.assertEqual(me.first_name, new_name)

    def test_other_cannot_update(self):
        new_name = 'Carl'
        account = self.accounts[0]
        old_name = account.first_name
        self.client.force_authenticate(user=account)
        response = self.client.patch(reverse('auth:accounts-detail', kwargs={'pk': self.accounts[1].pk}),
                                     data=json.dumps({'first_name': new_name}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        account.refresh_from_db()
        self.assertEqual(account.first_name, old_name)

    def test_anon_cannot_update(self):
        new_name = 'Carl'
        account = self.accounts[0]
        old_name = account.first_name
        response = self.client.patch(reverse('auth:accounts-detail', kwargs={'pk': account.pk}),
                                     data=json.dumps({'first_name': new_name}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        account.refresh_from_db()
        self.assertEqual(account.first_name, old_name)
