# _*_ Anaconda3-Python3.8 _*_
from io import BytesIO
from django.shortcuts import HttpResponse
from app01.utils.checkcode import check_code


def code(request):
    """ 生成图片验证码 """
    img, code_str = check_code()
    # 图片的文字存入session
    request.session["keycode"] = code_str
    # session设置keycode秒超时
    request.session.set_expiry(60)
    # 存入内存数据流BytesIO()
    stream = BytesIO()
    img.save(stream, "png")
    return HttpResponse(stream.getvalue(), content_type="image/png")
