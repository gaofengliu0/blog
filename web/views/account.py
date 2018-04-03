# -*- coding:utf-8 -*-
import json
from django.shortcuts import render,redirect,HttpResponse
from repository import models
from ..forms.account import LoginForm,RegisterForm
from io import BytesIO
from utils.check_code import create_validate_code


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img,code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

def login(request):
    """
    登录系统
    :param request:
    :return:
    """

    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        result = {'status': False, 'message': None, 'data': None}
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info = models.UserInfo.objects.filter(
                username=username,password=password
            ).values(
                'nid', 'nickname',
                       'username', 'email',
                       'avatar',
                       'blog__nid',
                       'blog__site'
            ).first()
            if user_info:
                result['status'] = True
                request.session['user_info'] = user_info
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 7)
            else:
                result['message'] = '用户名或密码错误'
            print(form.data,form.cleaned_data,user_info)
        else:
            print(form.errors)
            if 'ckeck_code' in form.errors:
                result['message'] = '验证码错误或者过期'
            else:
                result['message'] = '用户名或密码错误'

        return HttpResponse(json.dumps(result))



def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        form = RegisterForm(request=request, data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            nickname = form.cleaned_data.get('nickname')
            # models.UserInfo.objects.create(username=username,email=email,password=password,nickname=nickname)
            # print(info)
            # if info:
            #     return redirect('/login.html')
            # else:
            #     print('数据插入失败')
            #     return redirect('/login.html')
            return redirect('/login.html')
        else:
            return HttpResponse('错误')


def logout(request):
    request.session.clear()
    return redirect('/')









