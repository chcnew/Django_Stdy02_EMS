"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/3/16
 * @Environment: Anaconda3
"""

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


# 中间件按顺序先全部进再全部出
class AuthMiddleware(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self, request):
        # request.path_info可以获取当前用户访问的地址
        if request.path_info in ["/admin/login/", "/user/login/", "/image/code/", "/user/register/"]:
            return
        # 方法中没有返回值，返回None，可以继续往下走
        # 有返回值则直接返回数据（如页面或重定向），结束中间件M1
        # 读取用户session值，如果存在，则登录反之继续返回登陆页面
        info_dict = request.session.get("info")  # 获取用户浏览器是否存在相应的cookie
        #  如果info获取到数据，则继续往下走
        if info_dict:
            return
        else:
            # 如果获取到info字典为空，返回登陆页面
            return redirect("/admin/login/")
