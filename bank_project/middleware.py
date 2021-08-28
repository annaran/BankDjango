
import re
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import Group

EXEMPT_URLS = settings.EXEMPT_URLS

BANK_RESTRICTED_URLS = re.compile(r'/bank/(.*)$')
CUSTOMER_RESTRICTED_URLS = re.compile(r'/customer/(.*)$')
API_URLS = re.compile(r'/bank/api/v1/(.*)$')


class LoginRequiredMiddleware:
    # get_response is a function passed to the middleware class
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    # process view is going to run when Django is about to call one of the view functions
    # view_func is a function object that is about to be called
    # check what is veiw args and view kwargs
    def process_view(self, request, view_func, view_args, view_kwargs):
        # check if req obj has an att user, it checks if request.user exists
        # if request.user doesn't exist, it will frow an error
        assert hasattr(request, 'user')
        path = request.path_info

        # authenticated() - returns a boolean value
        if not request.user.is_authenticated:
            if path not in EXEMPT_URLS and not API_URLS.match(path):
                return redirect(reverse('login_app:login'))
        else:
            if BANK_RESTRICTED_URLS.match(path):
                if not request.user.groups.filter(
                        name='Employees').exists():
                    return redirect(reverse('customer_app:access_denied'))
            elif CUSTOMER_RESTRICTED_URLS.match(path):
                if not request.user.groups.filter(
                        name='Clients').exists():
                    return redirect(reverse('bank_app:access_denied'))
