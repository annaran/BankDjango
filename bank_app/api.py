from rest_framework import viewsets
from rest_framework.response import Response
from .models import UserProfile, User, UserType, Account, Transaction
from .serializers import UserProfilesSerializer, UsersSerializer, TransactionsSerializer, AccountsSerializer
from .permissions import IsOwnerOrNoAccess

# customer per id


class UserProfileDetail(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfilesSerializer
    lookup_field = 'user_id'


# customers all
class UserProfileList(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfilesSerializer

    def get_queryset(self):
        user_type_id = UserType.objects.get(
            text=self.kwargs['user_type_text']).id
        print(self.kwargs['user_type_text'])
        print(user_type_id)
        queryset = UserProfile.objects.filter(user_type_id=user_type_id)
        return queryset


# transactions all
class TransactionsList(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer


# transactions per account
class TransactionsPerAccountList(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer

    def get_queryset(self):
        account_id = Account.objects.get(
            account_number=self.kwargs['account_number']).id
        print(self.kwargs['account_number'])
        print(account_id)
        queryset = Transaction.objects.filter(account_id=account_id)
        return queryset

# accounts all


class AccountsList(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountsSerializer


# accounts per type (loan or standard)
class AccountsPerTypeList(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountsSerializer

    def get_queryset(self):
        queryset = Account.objects.filter(
            account_type=self.kwargs['account_type'])
        return queryset
