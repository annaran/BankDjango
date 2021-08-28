from django.contrib.auth.models import Group
from bank_app.models import Account, Transaction, User, UserType, UserProfile
from django.db.models import Sum, F, Count
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from decimal import Decimal
from django.core.exceptions import ValidationError


def form_make_loan_payment(request):
    accounts = Account.objects.filter(
        user_id=request.user, account_type="standard")
    loans = Account.objects.filter(user_id=request.user, account_type="loan")
    context = {
        'accounts': accounts,
        'loans': loans
    }

    if request.method == "POST":
        standard_account_number = request.POST['standard_account_number']
        loan_account_number = request.POST['loan_account_number']
        amount = request.POST['amount']
        standard_account = get_object_or_404(
            Account, account_number=standard_account_number)
        loan_account = get_object_or_404(
            Account, account_number=loan_account_number)
        try:
            transaction = Transaction()
            transaction.transfer(
                standard_account, loan_account, "loan payment", Decimal(amount), is_loan=False)
            messages.success(request, "Loan payment successful.")
            return HttpResponseRedirect(reverse('customer_app:view_my_accounts'))
        except ValidationError as err:
            messages.warning(
                request, err.messages)
            return render(request, 'customer_app/form_make_loan_payment.html', context)
    else:
        return render(request, 'customer_app/form_make_loan_payment.html', context)


def form_take_a_loan(request):

    accounts = Account.objects.filter(
        user_id=request.user, account_type="standard")

    context = {
        'accounts': accounts
    }

    if request.method == "POST":
        try:
            number_account_to = request.POST['account']
            amount = request.POST['amount']
            account_to = get_object_or_404(
                Account, account_number=number_account_to)
            request.user.userprofile.take_loan(account_to, amount)
            messages.success(request, "Successfully added a new loan.")
            return HttpResponseRedirect(reverse('customer_app:view_my_accounts'))
        except ValidationError as err:
            messages.warning(
                request, err.messages)
            return render(request, 'customer_app/form_take_a_loan.html', context)
    else:
        return render(request, 'customer_app/form_take_a_loan.html', context)


def form_transfer_money(request):
    accounts = Account.objects.filter(
        user_id=request.user, account_type="standard")
    context = {
        'accounts': accounts
    }

    if request.method == "POST":
        standard_account_number = request.POST['standard_account_number']
        receiver_account_number = request.POST['receiver_account_number']
        bank_code = request.POST['bank_code']
        standard_account = get_object_or_404(
            Account, account_number=standard_account_number)
        if(bank_code == "10"):
            print("internal")
            receiver_account = get_object_or_404(
                Account, account_number=receiver_account_number)
        else:
            print("external")
            receiver_account = get_object_or_404(
                Account, account_number=28694578)

        description = request.POST['description']
        amount = request.POST['amount']
        try:
            transaction = Transaction()
            transaction.transfer(
                standard_account, receiver_account, description, Decimal(amount), is_loan=False)
            messages.success(request, "Transfer successful.")
            channel_layer = get_channel_layer()
            # Pass any data based on your requirement
            data = "You have just received money from " + standard_account.user_id.username
            # Trigger message sent to group
            print(receiver_account.user_id.pk)
            async_to_sync(channel_layer.group_send)(
                # Group Name, Should always be string
                str(receiver_account.user_id.pk),
                {
                    "type": "notifyAboutTransfer",   # Custom Function written in the consumers.py
                    "text": data,
                },
            )
            return HttpResponseRedirect(reverse('customer_app:view_my_accounts'))
        except ValidationError as err:
            messages.warning(
                request, err.messages)
            return render(request, 'customer_app/form_transfer_money.html', context)

    else:
        return render(request, 'customer_app/form_transfer_money.html', context)


def view_account_details(request, account_id):
    account = Account.objects.filter(id=str(account_id))
    accountTransactions = Transaction.objects.select_related().filter(
        account_id=str(account_id))
    accountBalance = Account.objects.filter(user_id=request.user, id=account_id).annotate(
        ammount=Sum('transaction__ammount'))
    context = {
        'account': account,
        'accountBalance': accountBalance,
        'accountTransactions': accountTransactions
    }

    return render(request, 'customer_app/view_account_details.html', context)


def view_my_accounts(request):
    bankAccounts = Account.objects.filter(user_id=request.user).annotate(
        ammount=Sum('transaction__ammount'))
    context = {
        'bankAccounts': bankAccounts

    }
    # print(request.user)
    return render(request, 'customer_app/view_my_accounts.html', context)


def view_profile(request):
    customer = User.objects.filter(username=request.user)
    phone_number = UserProfile.objects.get(user=request.user).phone_number
    user_rank = UserProfile.objects.get(user=request.user).user_type.text
    context = {
        'customer': customer,
        'phone_number': phone_number,
        'user_rank': user_rank
    }
    return render(request, 'customer_app/view_profile.html', context)


def access_denied(request):
    return render(request, 'customer_app/access_denied.html')
