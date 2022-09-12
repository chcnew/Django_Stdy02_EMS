"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/3/18
 * @Environment: Anaconda3
"""
import random
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils import var_glo
from app01.utils.usedform import Order

from app01.utils.pagination import Pagination


@csrf_exempt
def order_list(request):
    """ 订单列表&新建订单 """
    if request.method != "POST":
        form = Order()
        data_dict = {}
        search_data = request.GET.get("srch", "")
        if search_data:
            data_dict["oid__contains"] = search_data
        # 指定显示行数 ，作为参数传入
        queryset = models.Order.objects.filter(**data_dict).order_by("-oid")  # filter不传入值，同样获取全部。
        page_obj = Pagination(request, queryset, plus=3)  # 实例化对象(页头已经导入)，参数初始化
        page_queryset = page_obj.page_queryset  # 显示行方法**[x:y]
        page_str = page_obj.html()  # 生成html代码
        # 存入全局变量
        var_glo.GLO_PAGE = page_obj.page
        var_glo.REMAINDER = page_obj.remainder
        context = {
            "form": form,
            "search_placeholder": "请按订单号搜索...",
            "search_data": search_data,
            "addtext": "新建订单",
            "page_queryset": page_queryset,
            "page_str": page_str,
            "page_jump_error": page_obj.page_jump_error,
            "page": page_obj.page,

        }
        return render(request, 'order_list.html', context)
    form = Order(data=request.POST)
    # 自定义赋值给留空的订单号oid值
    form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
    form.instance.name_id = request.session["info"]["id"]
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "errors": form.errors})


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get("uid")
    page = request.GET.get("page")
    exist = models.Order.objects.filter(id=uid).exists()
    if not exist:
        return JsonResponse({"status": False, "error": "该订单不存在,请刷新重试！"})
    models.Order.objects.filter(id=uid).delete()
    if var_glo.REMAINDER == 1:  # 全局变量为1时，点击删除触发减1
        if var_glo.GLO_PAGE > 1:
            return JsonResponse({"status": True, "page_num": var_glo.GLO_PAGE - 1})
    return JsonResponse({"status": True, "page_num": var_glo.GLO_PAGE})


def order_editget(request):
    uid = request.GET.get('uid')
    print(uid)
    # 行可以用filter筛选，列数据用value筛选
    # queryset = [行，行，行, ... ...]
    # queryset.values = [{"id":xxx}, {name:"xxx"}, {age:"xxx"}... ...]
    # queryset.values_list = [(1,"xxx"), (2:"xxx"), (3:"xxx")... ...]
    row_obj = models.Order.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_obj:
        return JsonResponse({"status": False, "error": "该订单不存在,请刷新重试！"})
    return JsonResponse({"status": True, "data": row_obj})


@csrf_exempt
def order_edit(request):
    uid = request.GET.get('uid')
    row_obj = models.Order.objects.filter(id=uid).first()
    # data更新instance,现在更新以前
    form = Order(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "errors": form.errors})
