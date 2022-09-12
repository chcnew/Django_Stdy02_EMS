from django.shortcuts import render, redirect
from app01 import models
from django import forms
import re
# from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# ####################### 部门管理 ######################
def depart_list(request):
    """ 部门列表 """
    querySet = models.Department.objects.all()  # 获取全部数据
    return render(request, 'depart_list.html', {"querySet": querySet})


def depart_add(request):
    """ 新增部门 """
    if request.method == "GET":
        return render(request, "depart_add.html")
    get_title = request.POST.get("title")
    # 先不考虑数据校验，后边后端组件实现。
    models.Department.objects.create(title=get_title)
    return redirect("/depart/list/")  # 重定向至list页


def depart_delete(request):
    """ 删除部门 """
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):  # 正则表达式传值作为参数，不必使用GET请求获取
    """ 编辑部门 """
    if request.method == "GET":
        row_obj = models.Department.objects.filter(id=nid).first()  # 获取行对象
        return render(request, "depart_edit.html", {"row_obj": row_obj})  # 传入querySet值；[row_obj, ]
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")


# ####################### 用户管理 ######################
def user_list(request):
    """ 用户列表 """
    querySet = models.UserInfo.objects.all()  # 获取全部数据
    return render(request, 'user_list.html', {"querySet": querySet})


def user_add(request):
    """ 新增用户 """
    if request.method == "GET":
        var_dict = {
            "gender_choices": models.UserInfo.gender_choices,
            "department": models.Department.objects.all()
        }
        return render(request, "user_add.html", var_dict)

    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    create_time = request.POST.get("create_time")
    gender = request.POST.get("gender")
    depart_id = request.POST.get("depart_id")
    models.UserInfo.objects.create(
        name=name,
        password=password,
        age=age,
        account=account,
        create_time=create_time,
        gender=gender,
        depart_id=depart_id
    )
    return redirect("/user/list/")  # 重定向至list页


def user_delete(request, nid):
    """ 删除用户 """
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def user_edit(request, nid):  # 正则表达式传值作为参数，不必使用GET请求获取
    """ 编辑用户 """
    if request.method == "GET":
        row_obj = models.UserInfo.objects.filter(id=nid).first()  # 获取行对象
        return render(request, "user_edit.html", {"row_obj": row_obj})  # 传入querySet值；[row_obj, ]

    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    create_time = request.POST.get("create_time")
    gender = request.POST.get("gender")
    depart_id = request.POST.get("depart_id")
    models.UserInfo.objects.filter(id=nid).update(
        name=name,
        password=password,
        age=age,
        account=account,
        create_time=create_time,
        gender=gender,
        depart_id=depart_id
    )
    return redirect("/user/list/")


# modelForm实现新增用户和编辑用户
class UserModelForm(forms.ModelForm):
    """ 创建UserModelForm类 """

    class Meta:
        model = models.UserInfo  # 为数据上传数据库准备
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        # 给前端添加样式widgets原理写法【实际开发不使用】
        # 关键字【有s】：widgets
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    # 给前端添加样式快速写法,与Meta类同级【工作必须使用】
    def __init__(self, *args, **kwargs):  # 有self，代表本函数内参数传递
        super().__init__(*args, **kwargs)  # 无self，使用父类方法，其实就是使用类Meta的对象
        # 循环找到所有插件，字典对象
        for name, field in self.fields.items():
            print(name, field)
            field.widget.attrs = {
                "class": "form-control",
                "placeholder": field.label
            }


def user_model_form_add(request):
    """ ModelForm实现新增用户 """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    # UserModelForm实例化：data参数接收POST提交的数据并进行封装
    form = UserModelForm(data=request.POST)
    # 数据校验，如果数据合法，则使用save方法保存到数据库;反之提示错误信息。
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    else:
        # 如果数据不合法，则回到原页面，内部会自动识别为不合法且在前端输出显示
        return render(request, "user_model_form_add.html", {"form": form})


# ####################### 靓号管理 #######################
def user_model_form_edit(request, nid):
    """ ModelForm实现编辑用户 """

    if request.method == "GET":
        # instance；实例；使用该参数直接对接数据库行数据即可。
        row_obj = models.UserInfo.objects.filter(id=nid).first()  # 获取querySet的第一个对象行数据。
        models.UserInfo.objects.filter(id=12)  # 等于
        models.UserInfo.objects.filter(id__gt=12)  # 大于
        models.UserInfo.objects.filter(id__gte=12)  # 大于等于
        models.UserInfo.objects.filter(id__lt=12)  # 小于
        models.UserInfo.objects.filter(id__lte=12)  # 小于等于
        models.UserInfo.objects.filter(name__startswith="张")  # 开头是
        models.UserInfo.objects.filter(name__endsswith="空")  # 结尾是
        models.UserInfo.objects.filter(name__contains="备")  # 包含

        form = UserModelForm(instance=row_obj)
        return render(request, "user_model_form_edit.html", {"form": form})

    row_obj = models.UserInfo.objects.filter(id=nid).first()  # 获取querySet的第一个对象行数据。
    form = UserModelForm(data=request.POST, instance=row_obj)  # data数据更新覆盖实例instance。
    if form.is_valid():
        # 默认保存Meta类里的fields变量参数字段，假设未设置全部字段，此处想增加字段语法如下：
        # form.instance.字段名 = 值
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, "user_model_form_add.html", {"form": form})


def prettynum_list(request):
    """ 靓号列表 """
    # Mysql数据库升/降序排序：select * from 表名 order by id asc/desc
    # querySet = models.PrettyNum.objects.all().order_by("-level")  # 按级别降序排序，带负号，升序不带符号。
    data_dict = {}
    search_data = request.GET.get("srch", "")
    if search_data:
        data_dict["phonenum__contains"] = search_data
    querySet = models.PrettyNum.objects.filter(**data_dict).order_by("-level")  # fillter不传入值，同样获取全部。
    return render(request, "pretty_list.html", {"querySet": querySet, "search_data": search_data})


class PrettyNum(forms.ModelForm):
    """ 创建PrettyNum类 """

    # 数据验证方法一：正则表达式验证器
    # phonenum = forms.CharField(
    #     disabled=True,  # 是否可以修改
    #     label="手机号",  # 不加会在前端直接显示字段名
    #     validators=[RegexValidator(r'1[3-9]\d{9}', '手机号格式错误！')],
    # )

    # 数据验证方法二：钩子方法，写入类函数
    # 钩子方法虽然代码复杂，但是推荐使用，因为可以实现对数据重复的校验
    def clean_phonenum(self):
        # 获取到当前用户输入手机号
        txt_phonenum = self.cleaned_data["phonenum"]
        # 手机号重复验证
        get_id = self.instance.pk
        exists = models.PrettyNum.objects.exclude(id=get_id).filter(phonenum=txt_phonenum).exists()
        if exists:
            raise ValidationError("手机号已存在！")
        # 手机号格式验证
        if not re.findall(r'1[3-9]\d{9}', txt_phonenum):
            raise ValidationError("手机号格式错误！")

        return txt_phonenum

    class Meta:
        model = models.PrettyNum
        # fields = ["phonenum", "price", "level", "status"] # 选取指定字段
        fields = "__all__"  # 选取全部字段
        # exclude = ["price"]  # 排除字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {
                "class": "form-control",
                "placeholder": field.label,
            }


def prettynum_add(request):
    """ 新建靓号 """
    if request.method == "GET":
        form = PrettyNum()
        return render(request, "pretty_add.html", {"form": form})

    form = PrettyNum(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/prettynum/list/")
    else:
        return render(request, "pretty_add.html", {"form": form})


def prettynum_delete(request, nid):
    """ 删除靓号 """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/prettynum/list/")


def prettynum_edit(request, nid):
    row_obj = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyNum(instance=row_obj)
        return render(request, "pretty_edit.html", {"form": form})

    form = PrettyNum(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/prettynum/list/")
    else:
        return render(request, "pretty_edit.html", {"form": form})
