"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/03/14
 * @Environment: Anaconda3
"""
import pandas as pd
from app01 import models
from django.shortcuts import render, redirect
from app01.utils.usedform import User, UserLogin
from app01.utils import var_glo
from django.http import JsonResponse
from app01.utils.pagination import Pagination  # 自定义分页组件
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def user_login(request):
    """ 普通用户登录 """
    if request.method != "POST":
        form = UserLogin()
        return render(request, "user_login.html", {"form": form})

    # Ajax实现
    get_usr = dict(request.POST)["username"][0]
    get_pwd = dict(request.POST)["password"][0]
    form = UserLogin(data=request.POST)
    if form.is_valid():
        usr_obj = models.UserInfo.objects.filter(username=get_usr, password=get_pwd).first()
        if usr_obj:
            # 验证码验证
            if request.session.get("keycode", "").upper() != form.cleaned_data.get("imgcode").upper():
                form.add_error("imgcode", "验证码不正确！")
                return JsonResponse({"status": False, "errors": form.errors})
            # 验证码验证成功，登陆成功，存入session
            request.session["info"] = {"id": usr_obj.id, "name": usr_obj.name}
            request.session.set_expiry(60 * 60 * 24 * 7)
            return JsonResponse({"status": True})
        form.add_error("password", "用户名或密码错误！")
        return JsonResponse({"status": False, "errors": form.errors})
    return JsonResponse({"status": False, "errors": form.errors})


@csrf_exempt
def user_register(request):
    """  普通用户注册 """
    if request.method != "POST":
        form = User()
        return render(request, "user_register.html", {"form": form})


def user_list(request):
    """ 用户列表 """
    # 添加测试数据
    # for i in range(2, 300):
    #     models.UserInfo.objects.create(
    #         id=i,
    #         name="test" + str(i),
    #         password="test" + str(i),
    #         age=random.randint(24, 55),
    #         account=random.randint(1000, 100000) + random.random(),
    #         create_time=random_date.get_randate("2021-01-01 00:00:00","2022-03-20 00:00:00"),
    #         gender=random.choice((0, 1)),
    #         depart_id=random.choice((1, 2, 3, 20, 27, 31, 36, 37, 38)),
    #     )

    if request.FILES.get("file"):
        file_obj = request.FILES.get("file")
        # print(type(file_obj))
        # f = open(file_obj.name, 'wb')
        # for chunk in file_obj.chunks():  # chunks()--获取文件区块方法
        #     f.write(chunk)  # 写入文件区块到本地
        # f.close()
        # excel传入对象可以直接使用
        df = pd.read_excel(file_obj, sheet_name=0)
        for i in range(len(df)):
            models.UserInfo.objects.create(**dict(df.iloc[i]))
        return redirect("/user/list/")

    data_dict = {}
    search_data = request.GET.get("srch", "")
    if search_data:
        data_dict["name__contains"] = search_data
    # 指定显示行数 ，作为参数传入
    queryset = models.UserInfo.objects.filter(**data_dict).order_by("id")  # filter不传入值，同样获取全部。
    page_obj = Pagination(request, queryset, plus=3)  # 实例化对象(页头已经导入)，参数初始化
    page_queryset = page_obj.page_queryset  # 显示行方法**[x:y]
    page_str = page_obj.html()  # 生成html代码
    # 存入全局变量
    var_glo.GLO_PAGE = page_obj.page
    var_glo.REMAINDER = page_obj.remainder
    context = {
        "search_placeholder": "请按姓名搜索...",
        "search_data": search_data,
        "addtext": "新建用户",
        "addhref": "/user/add/",
        "page_queryset": page_queryset,
        "page_str": page_str,
        "page_jump_error": page_obj.page_jump_error,
        "page": page_obj.page,

    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """ ModelForm实现新建用户 """
    if request.method == "GET":
        form = User()
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "新建用户"})

    # UserModelForm实例化：data参数接收POST提交的数据并进行封装
    form = User(data=request.POST)
    # 数据校验，如果数据合法，则使用save方法保存到数据库;反之提示错误信息。
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    else:
        # 如果数据不合法，则回到原页面，内部会自动识别为不合法且在前端输出显示
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "新建用户"})


def user_delete(request, nid):
    """ 删除用户 """
    models.UserInfo.objects.filter(id=nid).delete()
    if var_glo.REMAINDER == 1:  # 全局变量为1时，点击删除触发减1
        if var_glo.GLO_PAGE > 1:
            return redirect("/user/list/?page=" + str(var_glo.GLO_PAGE - 1))
    return redirect("/user/list/?page=" + str(var_glo.GLO_PAGE))


def user_edit(request, nid):
    """ ModelForm实现编辑用户 """
    row_obj = models.UserInfo.objects.filter(id=nid).first()  # 获取querySet的第一个对象行数据。
    if request.method == "GET":
        # instance；实例；使用该参数直接对接数据库行数据即可。
        form = User(instance=row_obj)
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "编辑用户"})

    form = User(data=request.POST, instance=row_obj)  # data数据更新覆盖实例instance。
    if form.is_valid():
        # 默认保存Meta类里的fields变量参数字段，假设未设置全部字段，此处想增加字段语法如下：
        # form.instance.字段名 = 值
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "编辑用户"})

# 原始方法
# def user_add(request):
#     """ 新建用户 """
#     if request.method == "GET":
#         var_dict = {
#             "gender_choices": models.UserInfo.gender_choices,
#             "department": models.Department.objects.all()
#         }
#         return render(request, "temp/add_edit_temp.html", var_dict)
#
#     name = request.POST.get("name")
#     password = request.POST.get("password")
#     age = request.POST.get("age")
#     account = request.POST.get("account")
#     create_time = request.POST.get("create_time")
#     gender = request.POST.get("gender")
#     depart_id = request.POST.get("depart_id")
#     models.UserInfo.objects.create(
#         name=name,
#         password=password,
#         age=age,
#         account=account,
#         create_time=create_time,
#         gender=gender,
#         depart_id=depart_id
#     )
#     return redirect("/user/list/")  # 重定向至list页
#
#
# def user_edit(request, nid):  # 正则表达式传值作为参数，不必使用GET请求获取
#     """ 编辑用户 """
#     if request.method == "GET":
#         row_obj = models.UserInfo.objects.filter(id=nid).first()  # 获取行对象
#         return render(request, "user_edit.html", {"row_obj": row_obj})  # 传入querySet值；[row_obj, ]
#
#     name = request.POST.get("name")
#     password = request.POST.get("password")
#     age = request.POST.get("age")
#     account = request.POST.get("account")
#     create_time = request.POST.get("create_time")
#     gender = request.POST.get("gender")
#     depart_id = request.POST.get("depart_id")
#     models.UserInfo.objects.filter(id=nid).update(
#         name=name,
#         password=password,
#         age=age,
#         account=account,
#         create_time=create_time,
#         gender=gender,
#         depart_id=depart_id
#     )
#     return redirect("/user/list/")
