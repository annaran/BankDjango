from rest_framework import serializers
from .models import UserProfile, User, UserType, Transaction, Account


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserProfilesSerializer(serializers.ModelSerializer):
    user_type = serializers.SlugRelatedField(
        many=False, slug_field='text', read_only=True)
    user = UsersSerializer(many=False, read_only=False)

    class Meta:
        model = UserProfile
        fields = ('user_id', 'user_type', 'phone_number', 'user')
        lookup_field = 'user_id'


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('__all__')


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('__all__')
