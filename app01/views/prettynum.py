"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/3/14
 * @Environment: Anaconda3
"""
from app01 import models
from django.shortcuts import render, redirect
from app01.utils.usedform import PrettyNum
from app01.utils import var_glo
from app01.utils.pagination import Pagination  # 自定义分页组件


# ####################### 靓号管理 #######################
def prettynum_list(request):
    """ 靓号列表 """
    # Mysql数据库升/降序排序：select * from 表名 order by id asc/desc
    # querySet = models.PrettyNum.objects.all().order_by("-level")  # 按级别降序排序，带负号，升序不带符号。
    data_dict = {}
    search_data = request.GET.get("srch", "")
    if search_data:
        data_dict["phonenum__contains"] = search_data
    # 指定显示行数 ，作为参数传入
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("id")  # filter不传入值，同样获取全部。
    # 自定义分页类的使用
    page_obj = Pagination(request, queryset, plus=3)  # 实例化对象(页头已经导入)，参数初始化
    page_queryset = page_obj.page_queryset  # 显示行方法**[x:y]
    page_str = page_obj.html()  # 生成html代码
    # 存入全局变量
    var_glo.GLO_PAGE = page_obj.page
    var_glo.REMAINDER = page_obj.remainder
    context = {
        "search_placeholder": "请按靓号搜索...",
        "search_data": search_data,
        "addtext": "新建靓号",
        "addhref": "/prettynum/add/",
        "page_queryset": page_queryset,
        "page_str": page_str,
        "page_jump_error": page_obj.page_jump_error,
        "page": page_obj.page,
    }
    return render(request, "pretty_list.html", context)


def prettynum_add(request):
    """ 新建靓号 """
    if request.method == "GET":
        form = PrettyNum()
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "新建靓号"})

    form = PrettyNum(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/prettynum/list/")
    else:
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "新建靓号"})


def prettynum_delete(request, nid):
    """ 删除靓号 """
    models.PrettyNum.objects.filter(id=nid).delete()
    if var_glo.REMAINDER == 1:  # 全局变量为1时，点击删除触发减1
        if var_glo.GLO_PAGE > 1:
            return redirect("/prettynum/list/?page=" + str(var_glo.GLO_PAGE - 1))
    return redirect("/prettynum/list/?page=" + str(var_glo.GLO_PAGE))


def prettynum_edit(request, nid):
    """ 编辑靓号 """
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyNum(instance=row_obj)
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "编辑靓号"})

    form = PrettyNum(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/prettynum/list/")
    else:
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "编辑靓号"})
