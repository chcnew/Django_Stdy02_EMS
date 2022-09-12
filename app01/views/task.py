"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/3/17
 * @Environment: Anaconda3
"""
import json
from app01 import models
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from app01.utils import var_glo
from app01.utils.pagination import Pagination
from app01.utils.usedform import Task


@csrf_exempt  # 免除csrf_coken认证
def task_test(request):
    if request.method != "POST":
        return render(request, "task_test.html")
    print(request.POST)
    # 若要向前端传送数据，需要转为json格式
    # data_dict = {"status": True, "data": [11, 22, 33, 44]}
    # 转换JSON格式数据，其实就是JSON格式的字符串,反过来用loads方法，无s方法表示要对文件操作。
    return HttpResponse(json.dumps(request.POST))


@csrf_exempt
def task_list(request):  # 增加数据与列表页面同步显示
    if request.method != "POST":
        form = Task()
        data_dict = {}
        search_data = request.GET.get("srch", "")
        if search_data:
            data_dict["title__contains"] = search_data
        # 指定显示行数 ，作为参数传入
        queryset = models.Task.objects.filter(**data_dict).order_by("id")
        page_obj = Pagination(request, queryset, plus=3)  # 实例化对象(页头已经导入)，参数初始化
        page_queryset = page_obj.page_queryset  # 显示行方法**[x:y]
        page_str = page_obj.html()  # 生成html代码
        # 自定义分页类的使用
        page_obj = Pagination(request, queryset, plus=3)  # 实例化对象(页头已经导入)，参数初始化
        page_queryset = page_obj.page_queryset  # 显示行方法**[x:y]
        page_str = page_obj.html()  # 生成html代码
        # 存入全局变量
        var_glo.GLO_PAGE = page_obj.page
        var_glo.REMAINDER = page_obj.remainder
        context = {
            "form": form,
            "search_placeholder": "任务标题搜索...",
            "search_data": search_data,
            "title_name": "新建任务",
            "addhref": "/task/add/",
            "page_queryset": page_queryset,
            "page_str": page_str,
            "page_jump_error": page_obj.page_jump_error,
            "page": page_obj.page,
        }
        return render(request, "task_list.html", context)

    print(request.POST)
    form = Task(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {"status": False, "errors": form.errors}
    return HttpResponse(json.dumps(data_dict))


def task_delete(request, nid):
    models.Task.objects.filter(id=nid).delete()
    if var_glo.REMAINDER == 1:  # 全局变量为1时，点击删除触发减1
        if var_glo.GLO_PAGE > 1:
            return redirect("/task/list/?page=" + str(var_glo.GLO_PAGE - 1))
    return redirect("/task/list/?page=" + str(var_glo.GLO_PAGE))
