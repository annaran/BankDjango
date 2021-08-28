from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Account, Transaction, User, UserType, UserProfile
from django.db.models import Sum, F
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import django_rq
from . generate_pdf import generatePDF
import uuid


def view_users(request):
    users = User.objects.filter(groups__name='Clients')
    context = {
        'users': users
    }
    return render(request, 'bank_app/view_users.html', context)


def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    phone_number = user_profile.phone_number
    user_rank = user_profile.user_type.text
    bankAcccounts = user_profile.accounts
    context = {
        'user_details': user,
        'bank_accounts': bankAcccounts,
        'phone_number': phone_number,
        'user_rank': user_rank
    }

    return render(request, 'bank_app/view_details.html', context)


def view_accounts(request):
    bankAcccounts = Account.objects.annotate(
        ammount=Sum('transaction__ammount'))
    context = {
        'bankAcccounts': bankAcccounts
    }
    return render(request, 'bank_app/view_accounts.html', context)


def create_user(request):
    userTypes = UserType.objects.all()
    context = {
        "user_types": userTypes
    }
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_name = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        type_id = request.POST['type']
        user_type = UserType.objects.get(id=type_id)
        if password == confirm_password:
            userProfile = UserProfile()
            userProfile.create_user_profile(
                user_name, first_name, last_name, email, password, user_type, phone_number)

            messages.success(request, 'User created successfully!')
            return HttpResponseRedirect(reverse('bank_app:view_users'))

        else:
            messages.warning(
                request, 'Passwords did not match. Please try again.')
            context = {
                'error': 'Passwords did not match. Please try again.'
            }
    return render(request, 'bank_app/create_user.html', context)


def create_account(request):
    if request.method == "POST":
        initial_ammount = request.POST['initial_ammount']
        user_id = request.POST['name_user_id']
        user = get_object_or_404(User, id=user_id)
        bank_acccount = Account()
        bank_acccount.create_bank_account(user, initial_ammount)
        messages.success(request, 'Account was successfully created!')
        return HttpResponseRedirect(f'../view_users/{user_id}')
    return render(request, 'bank_app/user_details.html')


def user_types(request):
    if request.method == "POST":
        userType = UserType()
        loan_permission = request.POST['loan_permission']
        user_type = request.POST['user_type']
        userType.create_user_type(loan_permission, user_type)
        messages.success(request, 'Successfully added new user type!')
        return HttpResponseRedirect(f'../user_types')
    userType = UserType.objects.all()
    context = {
        'userType': userType,
    }
    return render(request, 'bank_app/user_types.html', context)


def view_account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    accountTransactions = Transaction.objects.select_related().filter(
        account_id=str(account_id))
    context = {
        'account': account,
        'accountTransactions': accountTransactions
    }

    return render(request, 'bank_app/view_account_details.html', context)


def send_notification(request):
    if request.method == "POST":
        message = request.POST['message']

        messages.success(request, 'Notfication was successfully sent!')
        channel_layer = get_channel_layer()
        # Pass any data based on your requirement
        data = message
        # Trigger message sent to group
        async_to_sync(channel_layer.group_send)(
            "notifications",  # Group Name, Should always be string
            {
                "type": "notify",   # Custom Function written in the consumers.py
                "text": data,
            },
        )
        return render(request, 'bank_app/send_notification.html')

    return render(request, 'bank_app/send_notification.html')


def access_denied(request):
    return render(request, 'bank_app/access_denied.html')


def generate_pdf_with_account_details(request, account_id):

    pdf_id = uuid.uuid4()
    source_html = 'bank_app/pdf-tmpl.html'
    output_filename = 'pdf/' + str(pdf_id) + '.pdf'

    django_rq.enqueue(generatePDF, source_html,
                      output_filename, account_id)

    return HttpResponseRedirect(reverse('bank_app:view_account_details', args=[account_id]))
