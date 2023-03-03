from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import Account, Subscriptions


class TestAuthentication(APITestCase):

    def setUp(self) -> None:
        # arrange
        self.user = User(email='test@test.com', password='testtest')
        self.account = Account(user=self.user, subscription=Subscriptions.STANDARD)

    def test_account_creation_failure(self):
        # act
        res = self.client.post('/api/user/', data={'email': self.user.email, 'password': 'test'})
        # assert
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_account_creation_success(self):
        # act
        res = self.client.post('/api/user/', data={'email': self.user.email,
                                                   'password': self.user.password})
        # assert
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
