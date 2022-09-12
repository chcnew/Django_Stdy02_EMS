# _*_ Anaconda3-Python3.8 _*_
from app01 import models
from app01.utils.usedform import Login
from app01.utils.usedform import Admin, AdminEdit, AdminReset
from django.shortcuts import render, redirect
from app01.utils import var_glo
from app01.utils.pagination import Pagination


def admin_login(request):
    """ 管理员登录 """
    if request.method == "GET":
        form = Login()
        return render(request, "admin_login.html", {"form": form})

    form = Login(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data) ——> 字典
        # {'name': 'cenhongchang', 'password': '8760cffa7ea313bf75c6cd6e468ed033'}
        # 防止后期在session中加入数据，建议.filter()直接对应字段赋值，不要使用字典格式
        admin_obj = models.Admin.objects.filter(name=form.cleaned_data.get("name"), password=form.cleaned_data.get("password")).first()  # [行1,]
        if not admin_obj:
            # 增加自定义错误提示
            form.add_error("password", "用户名或密码错误！")
            return render(request, "admin_login.html", {"form": form})

        else:  # 用户名密码验证通过，还需验证验证码
            if request.session.get("keycode", "").upper() != form.cleaned_data.get("imgcode").upper():
                form.add_error("imgcode", "验证码不正确！")
                return render(request, "admin_login.html", {"form": form})
            # 服务器上网站生成随机字符，写入用户浏览器,同时写入服务器session
            request.session["info"] = {"id": admin_obj.id, "name": admin_obj.name}
            # 此时还需要设置验证码加长有效时间7天
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect("/admin/list/")
    else:
        return render(request, "admin_login.html", {"form": form})



def admin_list(request):
    """ 管理员列表 """
    # for i in range(1000):
    #     models.Admin.objects.create(name="test" + str(i), password=str(i))

    # Mysql数据库升/降序排序：select * from 表名 order by id asc/desc
    # querySet = models.PrettyNum.objects.all().order_by("-level")  # 按级别降序排序，带负号，升序不带符号。
    data_dict = {}
    search_data = request.GET.get("srch", "")
    if search_data:
        data_dict["name__contains"] = search_data
    # 指定显示行数 ，作为参数传入
    queryset = models.Admin.objects.filter(**data_dict).order_by("id")  # filter不传入值，同样获取全部。

    # 自定义分页类的使用
    page_obj = Pagination(request, queryset, plus=3)  # 实例化对象(页头已经导入)，参数初始化
    page_queryset = page_obj.page_queryset  # 显示行方法**[x:y]
    page_str = page_obj.html()  # 生成html代码
    # 存入全局变量
    var_glo.GLO_PAGE = page_obj.page
    var_glo.REMAINDER = page_obj.remainder
    context = {
        "search_placeholder": "请按用户名搜索...",
        "search_data": search_data,
        "addtext": "新建管理员",
        "addhref": "/admin/add/",
        "page_queryset": page_queryset,
        "page_str": page_str,
        "page_jump_error": page_obj.page_jump_error,
        "page": page_obj.page,
    }
    return render(request, "admin_list.html", context)


def admin_add(request):
    if request.method == "GET":
        form = Admin()
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "新建管理员"})

    form = Admin(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")  # 重定向至list页
    else:
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "新建管理员"})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    if var_glo.REMAINDER == 1:  # 全局变量为1时，点击删除触发减1
        if var_glo.GLO_PAGE > 1:
            return redirect("/admin/list/?page=" + str(var_glo.GLO_PAGE - 1))
    return redirect("/admin/list/?page=" + str(var_glo.GLO_PAGE))


def admin_edit(request, nid):
    row_obj = models.Admin.objects.filter(id=nid).first()
    # 获取到为对象，反之为None
    # 考虑多用户使用，可能会删除数据，而这边编辑没有获取到，重定向至本页刷新
    if not row_obj:
        return redirect("/admin/list/?page=" + str(var_glo.GLO_PAGE))

    if request.method == "GET":
        form = AdminEdit(instance=row_obj)
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "编辑管理员"})

    form = AdminEdit(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    else:
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "编辑管理员"})


def admin_reset(request, nid):
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return redirect("/admin/list/?page=" + str(var_glo.GLO_PAGE))

    if request.method == "GET":
        row_obj.password = ""
        form = AdminReset(instance=row_obj)
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "密码重置"})

    form = AdminReset(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    else:
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "密码重置"})
