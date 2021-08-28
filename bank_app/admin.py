from django.contrib import admin
from .models import Account, Transaction, UserType, UserProfile


admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(UserType)
admin.site.register(UserProfile)
