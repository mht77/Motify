from django.contrib.auth.models import User
from django.test import TestCase

import account_pb2
from grpc_services.account_service import AccountService


class AccountServiceTest(TestCase):

    def setUp(self) -> None:
        self.service = AccountService()
        self.user = User(username='test', password='test')
        self.user.save()

    def test_get_accounts(self):
        # arrange
        self.user.account.refresh_from_db()
        # act
        res = self.service.GetAccounts(
            account_pb2.GetAccountsRequest(id=[self.user.account.id]), target=None)
        # assert
        self.assertEqual(len(res.accounts), 1)
