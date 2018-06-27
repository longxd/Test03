# encoding: utf-8

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.views.generic import View


# def login_view(request):
#     if request.method == 'GET':
#         return render(request, 'auth/login.html')

# 用类

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')