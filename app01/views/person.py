"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/3/21
 * @Environment: Anaconda3
"""
from django.shortcuts import render, redirect


def person_info(request):
    return render(request, "person_info.html")


def person_modpwd(request):
    return render(request, "person_modpwd.html")


def person_photo(request):
    return render(request, "person_photo.html")


def person_num(request):
    return render(request, "person_num.html")
