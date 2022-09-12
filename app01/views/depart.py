"""

 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/03/14
 * @Environment: Anaconda3
"""

from app01 import models
from django.shortcuts import render, redirect
from app01.utils.usedform import Depart
from app01.utils import var_glo
from app01.utils.pagination import Pagination


# ####################### 部门管理 ######################
def depart_list(request):
    """ 部门列表 """
    data_dict = {}
    search_data = request.GET.get("srch", "")
    if search_data:
        data_dict["title__contains"] = search_data
    # 指定显示行数 ，作为参数传入
    queryset = models.Department.objects.filter(**data_dict).order_by("id")  # filter不传入值，同样获取全部。
    # 自定义分页类的使用
    page_obj = Pagination(request, queryset, plus=3)  # 实例化对象(页头已经导入)，参数初始化
    page_queryset = page_obj.page_queryset  # 显示行方法**[x:y]
    page_str = page_obj.html()  # 生成html代码
    # 存入全局变量
    var_glo.GLO_PAGE = page_obj.page
    var_glo.REMAINDER = page_obj.remainder
    context = {
        "search_placeholder": "请按部门搜索...",
        "search_data": search_data,
        "addtext": "新建部门",
        "addhref": "/depart/add/",
        "page_queryset": page_queryset,
        "page_str": page_str,
        "page_jump_error": page_obj.page_jump_error,
        "page": page_obj.page,
    }
    return render(request, "depart_list.html", context)


def depart_add(request):
    """ 新建部门 """
    if request.method == "GET":
        form = Depart()
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "新建部门"})

    # 对通过POST将返回的txt_title获取，data参数接收
    form = Depart(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/depart/list/")  # 重定向至list页
    else:
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "新建部门"})


def depart_delete(request,nid):
    """ 删除部门 """
    models.Department.objects.filter(id=nid).delete()
    if var_glo.REMAINDER == 1:  # 全局变量为1时，点击删除触发减1
        if var_glo.GLO_PAGE > 1:
            return redirect("/depart/list/?page=" + str(var_glo.GLO_PAGE - 1))
    return redirect("/depart/list/?page=" + str(var_glo.GLO_PAGE))


def depart_edit(request, nid):  # 正则表达式传值作为参数，不必使用GET请求获取
    """ 编辑部门 """
    row_obj = models.Department.objects.filter(id=nid).first()  # 获取行对象

    if request.method == "GET":
        form = Depart(instance=row_obj)
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "编辑部门"})

    form = Depart(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/depart/list/")
    else:
        return render(request, "temp/add_edit_temp.html", {"form": form, "title_name": "编辑部门"})
