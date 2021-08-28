from django.urls import path, include
from . import views
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from .api import UserProfileDetail, UserProfileList, AccountsList, AccountsPerTypeList, TransactionsList, TransactionsPerAccountList


app_name = 'bank_app'

urlpatterns = [
    path('view_accounts/', views.view_accounts, name='view_accounts'),
    path('view_users/', views.view_users, name='view_users'),
    path('view_users/<str:user_id>', views.user_details, name='user_details'),
    path('create_user/', views.create_user, name='create_user'),
    path('create_account/', views.create_account, name='create_account'),
    path('user_types/', views.user_types, name='user_types'),
    path('view_account_details/<str:account_id>',
         views.view_account_details, name='view_account_details'),
    path('send_notification/', views.send_notification, name='send_notification'),
    path('access_denied/', views.access_denied, name='access_denied'),
    path('generate_pdf_with_account_details/<str:account_id>',
         views.generate_pdf_with_account_details, name='generate_pdf_with_account_details'),
    path('api/v1/accounts/', AccountsList.as_view({'get': 'list'})),
    path('api/v1/accounts/<str:account_type>/',
         AccountsPerTypeList.as_view({'get': 'list'})),
    #path('api/v1/accounts/<int:account_id>/', AccountsList.as_view({'get':'retrieve'})),
    path('api/v1/transactions/', TransactionsList.as_view({'get': 'list'})),
    path('api/v1/transactions/<int:account_number>/',
         TransactionsPerAccountList.as_view({'get': 'list'})),
    path('api/v1/customers/<int:user_id>/',
         UserProfileDetail.as_view({'get': 'retrieve'})),
    path('api/v1/customers/<str:user_type_text>/',
         UserProfileList.as_view({'get': 'retrieve'})),
    path('api/v1/rest-auth/', include('rest_auth.urls')),

]
