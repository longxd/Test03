# encoding: utf-8

from django.urls import path
from . import views

app_name = 'xfzauth'

urlpatterns = [
    # path('login/', views.login_view, name='login')
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
]