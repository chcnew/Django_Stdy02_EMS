# _*_ Anaconda3-Python3.8 _*_
from django.shortcuts import redirect


def logout(request):
    request.session.clear()
    return redirect("/user/login/")
