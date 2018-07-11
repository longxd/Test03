#encoding: utf-8

from django import forms
from django.shortcuts import redirect,reverse
from django.contrib import messages
from .models import User
from apps.forms import FormMixin
from utils import restful


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11,min_length=11,error_messages=
    {"required":"必须收入手机号码！", 'min_length': "手机号码个数必须为11位！", 'max_length':'手机号码个数必须为11位！'})
    password = forms.CharField(min_length=6,max_length=20,error_messages=
    {"required": "必须输入密码！", 'min_length': "密码最少不能少于6位！", 'max_length': "密码最多不能多于20位！"})
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11, error_messages=
    {"required": "必须收入手机号码！", 'min_length': "手机号码个数必须为11位！", 'max_length': '手机号码个数必须为11位！'})
    username = forms.CharField(max_length=20, min_length=3, error_messages={"required": "必须输入用户名！",
                                                                            'min_length': "用户名最少不能少于3个字符！",
                                                                            'max_length': "用户名最多不能超过20个字符！"})
    img_captcha = forms.CharField(max_length=4, min_length=4, error_messages={"required": "请输入图形验证码！"})
    password1 = forms.CharField(min_length=6, max_length=20, error_messages=
    {"required": "必须输入密码！", 'min_length': "密码最少不能少于6位！", 'max_length': "密码最多不能多于20位！"})
    password2 = forms.CharField(min_length=6, max_length=20, error_messages=
    {"required": "必须输入重复密码！", 'min_length': "密码最少不能少于6位！", 'max_length': "密码最多不能多于20位！"})
    sms_captcha = forms.CharField(max_length=4, min_length=4, error_messages={"required": "请输入短信验证码"})

    def validate_data(self, request):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        # 打印密码便于排错
        print('xfzzuth/forms里面的password1密码：%s' % password1)
        print('xfzzuth/forms里面的password2密码：%s' % password2)

        if password1 != password2:
            #  messages.info(request, '两次密码不一致')
            # 'xfzauth:register' 是urls里面的app_name和path里面的路径组合而成,这样比较安全。
            # return redirect(reverse('xfzauth:register'))
            # 以上是传统表单使用的方法
            return self.add_error('password1', '两次密码输入不一致！')

        img_captcha = cleaned_data.get('img_captcha')
        server_img_captcha = request.session.get('img_captcha')
        if img_captcha.lower() != server_img_captcha.lower():
            # messages.info(request, '图形验证码错误')
            # return redirect(reverse('xfzauth:register'))
            # 以上是传统表单使用的方法
            return self.add_error('img_captcha', '图形验证码错误')

        sms_captcha = cleaned_data.get('sms_captcha')
        # print('sms_captcha是: %s' % sms_captcha)
        server_sms_captcha = request.session.get('sms_captcha')
        # print('server_sms_captcha是：%s' % server_sms_captcha)
        if sms_captcha.lower() != server_img_captcha.lower():
            # messages.info(request, '短信验证码')
            # return redirect(reverse('xfzauth:register'))
            # 以上是传统表单使用的方法
            return self.add_error('sms_captcha', '短信验证码错误')

        # 验证这个用户是否存在
        telephone = cleaned_data.get('telephone')
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            # messages.info(request, '该手机号已被注册')
            # return redirect(reverse('xfzauth:register'))
            # 以上是传统表单使用的方法
            return self.add_error('telephone', '该手机号已被注册')
        return True
