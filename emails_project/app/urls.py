from django.urls import path
from .views import register, user_login, user_logout, confirm_account, confirmation_sent, account_not_confirmed, home

urlpatterns = [
    path('home/', home, name='home'),
    path('', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('confirm/<str:token>/', confirm_account, name='confirm_account'),
    path('confirmation_sent/', confirmation_sent, name='confirmation_sent'),
    path('account_not_confirmed/', account_not_confirmed, name='account_not_confirmed'),
]
