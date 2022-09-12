"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/3/15
 * @Environment: Anaconda3
"""
import hashlib
from django.conf import settings


def md5(data_str):
    obj = hashlib.md5(settings.SECRET_KEY.encode("UTF-8"))  # 自定义字符部分
    obj.update(data_str.encode("utf-8"))  # 连接编码
    return obj.hexdigest()  # 加密编码并返回
