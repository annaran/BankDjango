from django.db import models, transaction
from django.contrib.auth.models import User
from random import randint
from phone_field import PhoneField
from decimal import Decimal
from django.contrib.auth.models import Group
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


def random_number():
    return randint(10000000, 99999999)


class Account(models.Model):
    account_number = models.IntegerField(default=random_number)
    open_date = models.DateTimeField(auto_now_add=True)
    account_type = models.CharField(max_length=20,  default="standard")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def create_bank_account(cls, user, initial_ammount):
        account = cls()
        account.user_id = user
        account.save()
        if(initial_ammount):
            transaction = Transaction()
            transaction.ammount = initial_ammount
            transaction.account = account
            transaction.transaction_id = str(uuid4())
            transaction.description = "Bank bonus :)"
            transaction.save()

    @property
    def balance(self):
        balance = Transaction.objects.filter(account=self).aggregate(
            models.Sum('ammount'))['ammount__sum'] or Decimal('0')
        balance = '{:0.2f}'.format(balance)
        return balance

    @property
    def movements(self):
        return Transaction.objects.filter(account=self)

    def __str__(self):
        return f"{self.account_number} / {self.open_date}"


class Transaction(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, default="no description")
    transaction_id = models.CharField(max_length=36, default=str(uuid4()))
    ammount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    @ classmethod
    def transfer(cls, from_account, to_account, description, amount, is_loan=False):
        with transaction.atomic():
            if Decimal(from_account.balance) >= amount or is_loan:
                transaction_id = str(uuid4())

                cls(account=from_account, transaction_id=transaction_id,
                    ammount=-amount, description=description).save()
                cls(account=to_account, transaction_id=transaction_id,
                    ammount=amount, description=description).save()
            else:
                raise ValidationError('Not enough money on the account.')

    @ classmethod
    def add_bank_bonus(cls, to_account, to_description, amount):
        transaction_id = str(uuid4())
        cls(account=to_account, transaction_id=transaction_id,
            amount=amount, description=to_description).save()

    def __str__(self):
        return f"{self.date} / {self.ammount}"


class UserType(models.Model):
    text = models.CharField(max_length=200)
    loan_permission = models.BooleanField(default=False)

    @ classmethod
    def create_user_type(cls, loan_permission, user_type):
        userType = cls()
        if loan_permission == "true":
            userType.loan_permission = True
        else:
            userType.loan_permission = False
        userType.text = user_type
        userType.save()

    def __str__(self):
        return f"{self.text}"


class UserProfile(models.Model):
    phone_number = PhoneField(blank=True)
    user_type = models.ForeignKey(
        UserType, on_delete=models.RESTRICT, null=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    @ property
    def accounts(self):
        return Account.objects.filter(user_id=self.user)

    @ classmethod
    def create_user_profile(cls, user_name, first_name, last_name, email, password, user_type, phone_number):
        user = User.objects.create_user(user_name, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        userProfile = cls()
        userProfile.user = user
        userProfile.user_type = user_type
        userProfile.phone_number = phone_number
        userProfile.save()
        clients = Group.objects.get(name='Clients')
        clients.user_set.add(user)

    def take_loan(self, account_to, amount):
        if(self.user_type.loan_permission):
            account = Account()
            account.account_type = "loan"
            account.user_id = self.user
            account.save()
            Transaction.transfer(account, account_to,
                                 "New loan", Decimal(amount), is_loan=True)
        else:
            raise ValidationError('Your rank is too loa to take a loan')
