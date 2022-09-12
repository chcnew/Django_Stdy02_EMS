"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/3/19
 * @Environment: Anaconda3
"""
import numpy as np
import pandas as pd
from app01 import models
from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    return render(request, "chart_list.html")


def chart_bar(request):
    """柱状图"""
    queryset = models.UserInfo.objects.all()
    if not queryset:
        data_dict = {"status": False, "error": "数据为空，请刷新重试！"}
        return JsonResponse(data_dict)

    df = pd.DataFrame(queryset.values())
    # 获取全部部门名称，排除重复存入列表
    title_name = []
    for obj in queryset:
        title_name.append(obj.depart.title)
    df["部门名称"] = title_name
    df["count"] = 1
    df["account"] = df["account"].astype("float")
    df = pd.pivot_table(df, index=["部门名称"], values=["account", "count"], aggfunc=np.sum)
    text = "部门实时数据"
    legend = ['资产（万元）', '人数']
    xAxis = df.index.values.tolist()  # 部门名称列表
    series = [
        {
            "name": legend[0],
            "type": "bar",
            "data": (round(df['account'] / 10000, 2)).tolist(),
            "itemStyle": {
                "normal": {
                    "label": {
                        "show": True,  # 开启显示
                        "position": 'top',  # 在上方显示
                        "textStyle": {  # 数值样式
                            "color": 'black',
                            "fontSize": 16
                        }
                    }
                }
            }

        },
        {
            "name": legend[1],
            "type": "bar",
            "data": df['count'].tolist(),
            "itemStyle": {
                "normal": {
                    "label": {
                        "show": True,  # 开启显示
                        "position": 'top',  # 在上方显示
                        "textStyle": {  # 数值样式
                            "color": 'black',
                            "fontSize": 16
                        }
                    }
                }
            }
        },
    ]

    data_dict = {
        "status": True,
        "text": text,
        "legend": legend,
        "xAxis": xAxis,
        "series": series
    }
    return JsonResponse(data_dict)
