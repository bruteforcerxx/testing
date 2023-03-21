from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_user, name='login'),
    path('dash', views.dash, name='dash'),
    path('send', views.send, name='send'),
    path('AUC-token', views.otp, name='otp'),
    path('AUC-token-resent', views.resend_otp, name='resend_otp'),
path('loan', views.loans, name='loan'),
    path('sent', views.sent, name='sent'),
    path('transactions', views.transactions, name='transactions'),
    path('profile', views.profile, name='profile'),
]

