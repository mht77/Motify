import account_pb2
import account_pb2_grpc
from account.models import Account


class AccountService(account_pb2_grpc.AccountService):

    def GetAccounts(self, request, context, **kwargs):
        query = Account.objects.filter(id__in=request.id)
        res = [account_pb2.Account(id=account.id, username=account.user.username, email=account.user.email,
                                   date_joined=str(account.user.date_joined),
                                   subscription=account.subscription)
               for account in query]
        return account_pb2.GetAccountsResponse(accounts=res)
