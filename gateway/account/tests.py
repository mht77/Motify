from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import Account, Subscriptions


class TestAuthentication(APITestCase):

    def setUp(self) -> None:
        # arrange
        self.user = User(email='test@test.com', password='testtest')
        self.account = Account(user=self.user, subscription=Subscriptions.STANDARD)
        self.USER_URL = '/api/user/'

    def test_user_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.USER_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_user_creation_failure(self):
        # act
        res = self.client.post(self.USER_URL, data={'email': self.user.email, 'password': 'test'})
        # assert
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_success(self):
        # act
        res = self.client.post(self.USER_URL, data={'email': self.user.email,
                                                    'password': self.user.password})
        # assert
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_put(self):
        updated_user_data = {
            "email": self.user.email,
            "password": "updatedpassword"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.USER_URL, updated_user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, updated_user_data['email'])
