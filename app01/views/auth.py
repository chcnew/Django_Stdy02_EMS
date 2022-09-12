# _*_ Anaconda3-Python3.8 _*_
from django.contrib import auth
from django.shortcuts import render, redirect
# 使用自带模块的用户数据库模型
from django.contrib.auth.models import User as auth_models_User


def auth_login(request):
    if request.method != "POST":
        return render(request, "auth_login.html")
    usr = request.POST.get("username")
    pwd = request.POST.get("password")
    ver = request.POST.get("imgcode")
    print(usr, pwd, ver)
    # 自动拿到对应值，进行加密后，与数据库比对校验
    row_obj = auth.authenticate(request, username=usr, password=pwd)
    if row_obj:
        if request.session.get("keycode").upper() == ver.upper():
            return redirect("/user/list/")
        else:
            return render(request, "auth_login.html")
    else:
        return render(request, "auth_login.html")


def auth_register(request):
    if request.method != "POST":
        return render(request, "auth_register.html")
    usr = request.POST.get("username")
    pwd = request.POST.get("password")
    eml = request.POST.get("email")
    ver = request.POST.get("verification")
    print(usr)
    # 创建普通加密用户
    try:
        auth_models_User.objects.create_user(
            username=usr,  # 设置超级管理员权限
            password=pwd,  # 设置密码,密码会自动加密的
            email=eml,  # 设置邮箱,可以不做设置
        )
    except RuntimeError:
        "系统异常！注册用户失败..."
