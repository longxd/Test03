# # encoding: utf-8
#
# from django.shortcuts import render
#
# # Create your views here.
#
# from django.shortcuts import render, redirect, reverse
# from django.views.generic import View
# from .forms import LoginForm
# from django.contrib.auth import authenticate, login
#
#
# # def login_view(request):
# #     if request.method == 'GET':
# #         return render(request, 'auth/login.html')
#
# # 用类
#
# class LoginView(View):
#     def get(self, request):
#         return render(request, 'auth/login.html')
#
#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             telephone = form.cleaned_data.get('telephone')
#             password = form.cleaned_data.get('password')
#             remember = form.cleaned_data.get('remember')
#             user = authenticate(request, username=telephone, password=password)
#             if user:
#                 login(request, user)
#                 if remember:
#                     request.session.set_expiry(None)
#                 else:
#                     request.session.set_expiry(0)
#                 #  成功之后跳转到首页
#                 return redirect(reverse('news:index'))
#             else:
#                 return redirect(reverse('xfzauth:login'))
#
#         else:
#             return redirect(reverse('xfzauth:login'))

#encoding: utf-8

from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from utils.captcha.hycaptcha import Captcha
from io import BytesIO


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get("telephone")
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = authenticate(request, username=telephone, password=password)
            if user:
                login(request,user)
                if remember:
                    # 如果设置过期时间为None，那么就会使用默认的过期时间
                    # 默认的过期时间是2个礼拜，也就是14天
                    request.session.set_expiry(None)
                else:
                    # 如果设置过期时间为0，那么浏览器关闭以后就会结束
                    request.session.set_expiry(0)
                # 如果登录成功，让他跳转到首页
                return redirect(reverse('news:index'))
            else:
                messages.info(request, '用户名或密码错误')
                return redirect(reverse('xfzauth:login'))
        else:
            messages.info(request, '表单失败！')
            return redirect(reverse('xfzauth:login'))


class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')


def img_captcha(request):
    text, image = Captcha.gene_code()
    #  image不是一个HttpResponse可以识别的对象
    #  因此先要将image变成一个数据流才能放到HttpResponse上
    out = BytesIO()
    # ByteIO: 相当于一个管道，可以用来存储字节流
    image.save(out, 'png')
    out.seek(0)
    # 将文件指针设置到0的位置

    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    return response
