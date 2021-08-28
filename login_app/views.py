from django.shortcuts import render, reverse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http import HttpResponseRedirect
from . import models
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import django_rq
from . messaging import email_message


def login(request):
    context = {}

    if request.method == "POST":
        user = authenticate(
            request, username=request.POST['user'], password=request.POST['password'])
        if user:
            if user.groups.filter(name='Clients').exists():
                dj_login(request, user)
                return HttpResponseRedirect(reverse('customer_app:view_profile'))
            elif user.groups.filter(name='Employees').exists():
                dj_login(request, user)
                return HttpResponseRedirect(reverse('bank_app:view_users'))
        else:
            context = {
                'error': 'Bad username or password.'
            }
    return render(request, 'login_app/login.html', context)


def logout(request):
    dj_logout(request)
    return render(request, 'login_app/login.html')


def password_reset(request):
    context = {}

    if request.method == "POST":
        email = request.POST['email']
        user = User.objects.get(email=email)
        reset_request = models.PasswordResetRequest()
        reset_request.user = user
        reset_request.save()
        url = reverse('login_app:password_reset_secret',
                      args=[f'{reset_request.token}'])
        url = f'{request.scheme}://{request.META["HTTP_HOST"]}{url}'
        print(url)
        context = {
            'message': 'Please click the link in the email we sent to you.'}
        django_rq.enqueue(email_message, {
            'reset-link': url,
            'email_reveiver': email,
        })
        return HttpResponseRedirect(reverse('login_app:password_reset'))

    return render(request, 'login_app/password_reset.html', context)


def password_reset_secret(request, secret):
    context = {'secret': secret}
    return render(request, 'login_app/new_password.html', context)


def password_reset_form(request):
    context = {}
    email = request.POST['email']
    token = request.POST['secret']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    user = User.objects.get(email=email)
    reset_request = models.PasswordResetRequest.objects.get(
        user=user, token=token)
    if password == confirm_password:
        user.set_password(password)
        user.save()
        reset_request.save()
    else:
        print("error")

    return render(request, 'login_app/new_password.html', context)


def password_change(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('customer_app:view_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'login_app/change_password.html', {
        'form': form
    })
