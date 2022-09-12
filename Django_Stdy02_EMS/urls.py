"""Django_Stdy02_EMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path
from app01.views import depart, user, prettynum, admin, task, order, chart, person, logout, image, auth

urlpatterns = [
    # path('admin/', admin.site.urls),
    # ###################### 部门管理 #######################
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/<int:nid>/delete/', depart.depart_delete),
    # Django支持含正则表达式的写法方便传递nid值
    # http://127.0.0.1:8000/depart/1/edit/
    # http://127.0.0.1:8000/depart/2/edit/
    # http://127.0.0.1:8000/depart/3/edit/
    path('depart/<int:nid>/edit/', depart.depart_edit),
    # ####################### 普通用户管理 ###################
    path('user/list/', user.user_list),
    path('user/<int:nid>/delete/', user.user_delete),
    # ######## 新增用户及编辑用户（MdodelForm）#################
    path('user/add/', user.user_add),
    path('user/<int:nid>/edit/', user.user_edit),
    # path('user/login/', user.user_login),
    re_path(r'^$', user.user_login),  # 设置为默认首页
    path('user/register/', user.user_register),
    # ####################### 靓号管理 ######################
    path('prettynum/list/', prettynum.prettynum_list),
    path('prettynum/add/', prettynum.prettynum_add),
    path('prettynum/<int:nid>/delete/', prettynum.prettynum_delete),
    path('prettynum/<int:nid>/edit/', prettynum.prettynum_edit),
    # ####################### 管理员模块 #######################
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/reset/', admin.admin_reset),
    # ####################### 管理员登录 #######################
    path('admin/login/', admin.admin_login),
    # ####################### 退出登录清除Cookie #######################
    path('logout/', logout.logout),
    # ####################### 验证码模块 #######################
    path('image/code/', image.code),
    # ####################### Ajax实现任务管理 #######################
    path('task/test/', task.task_test),
    path('task/list/', task.task_list),
    path('task/<int:nid>/delete/', task.task_delete),
    # ####################### 订单管理 #######################
    path('order/list/', order.order_list),
    path('order/delete/', order.order_delete),
    path('order/edit/', order.order_edit),
    path('order/editget/', order.order_editget),
    # ####################### 数据统计 #######################
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    # ####################### 个人中心 #######################
    path('person/info/', person.person_info),
    path('person/modpwd/', person.person_modpwd),
    path('person/photo/', person.person_photo),
    path('person/num/', person.person_num),
    # ################## Auth模块实现登录注册 ##################
    path('auth/login/', auth.auth_login),
    path('auth/register/', auth.auth_register),

]
