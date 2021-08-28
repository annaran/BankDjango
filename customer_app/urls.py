from django.urls import path
from . import views


app_name = 'customer_app'

urlpatterns = [
    path('view_profile/', views.view_profile, name='view_profile'),
    path('view_account_details/<int:account_id>',
         views.view_account_details, name='view_account_details'),
    path('form_make_loan_payment/', views.form_make_loan_payment,
         name='form_make_loan_payment'),
    path('view_my_accounts/', views.view_my_accounts, name='view_my_accounts'),
    path('form_take_a_loan/', views.form_take_a_loan, name='form_take_a_loan'),
    path('form_transfer_money/', views.form_transfer_money,
         name='form_transfer_money'),
    path('access_denied/', views.access_denied, name='access_denied'),
]
