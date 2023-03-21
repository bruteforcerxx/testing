from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('', views.home_page, name=' '),
    path('about', views.about, name='about'),
    path('test', views.test, name='test'),
    path('otp', views.otp, name='otp'),
    path('', views.home_page, name='index'),
    path('support', views.support, name='support'),
    path('loans', views.loans, name='loans'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('create-password', views.password, name='password'),
    path('about', views.home_page, name='about'),
    path('contact', views.contact, name='contact'),
    path('home', views.test, name='home'),
]
