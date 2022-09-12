"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/3/14
 * @Environment: Anaconda3
"""
import re
from app01 import models
from django import forms
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm  # 导入bootstrap类，用于继承其方法
from app01.utils.encrypt import md5  # 导入自定义加密方法
from django.core.exceptions import ValidationError  # 导入ValidationError类，用于数据验证错误返回


# 登录Form类
# 考虑到用户登录不需要保存数据到数据库，选择使用form组件.
class Login(BootStrapForm):
    # 外部创建字段
    name = forms.CharField(
        label="用户名",
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True)
    )

    imgcode = forms.CharField(
        label="验证码",
        widget=forms.TextInput(),
    )

    # flag = forms.ChoiceField(
    #     label="是否记住密码",
    #     widget=forms.CheckboxInput(),
    # )

    def clean_password(self):
        txt_pwd = md5(self.cleaned_data.get("password"))
        return txt_pwd


# 管理员ModelFrom类
class Admin(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["name", "password"]
        # widgets只支持数据库字段，自定义字段无法操作，自定义方法中参数操作即可.
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    confirm_pwd = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    def clean_password(self):
        txt_pwd = md5(self.cleaned_data.get("password"))
        return txt_pwd  # 返回加密值并存入数据库

    def clean_confirm_pwd(self):
        txt_pwd = self.cleaned_data.get("password")
        txt_confirm_pwd = md5(self.cleaned_data.get("confirm_pwd"))
        if txt_pwd != txt_confirm_pwd:
            raise ValidationError("密码输入不一致！")
        return txt_confirm_pwd

    def clean_name(self):
        txt_name = self.cleaned_data.get("name")
        if not re.findall(r"[a-zA-Z0-9_-]+", txt_name):
            raise ValidationError("管理员用户名只能是字母或数字组合！")
        return txt_name


# 管理员ModelFrom编辑类_只允许修改用户名
class AdminEdit(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["name"]


# 管理员密码重置ModelFrom类
class AdminReset(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["name", "password"]
        # widgets只支持数据库字段，自定义字段无法操作，自定义方法中参数操作即可.
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    name = forms.CharField(
        label="用户名",
        disabled=True,
    )

    confirm_pwd = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    def clean_password(self):
        txt_pwd = md5(self.cleaned_data.get("password"))
        return txt_pwd  # 返回加密值txt_pwd,并存入数据库，但txt_confirm_pwd未存进去。

    def clean_confirm_pwd(self):
        txt_pwd = self.cleaned_data.get("password")
        txt_confirm_pwd = md5(self.cleaned_data.get("confirm_pwd"))
        if txt_pwd != txt_confirm_pwd:
            raise ValidationError("密码输入不一致！")
        exist = models.Admin.objects.filter(id=self.instance.pk, password=txt_confirm_pwd).exists()
        if exist:
            raise ValidationError("重置密码不能与上次设置相同！")
        return txt_confirm_pwd


# 部门ModelFrom类
class Depart(BootStrapModelForm):
    class Meta:
        model = models.Department
        fields = ["title"]

    def clean_title(self):
        txt_title = self.cleaned_data.get("title")
        # 重复验证
        get_id = self.instance.pk
        exists = models.Department.objects.exclude(id=get_id).filter(title=txt_title).exists()
        if exists:
            raise ValidationError("部门已存在！")
        # 格式验证
        if not re.findall(r'\w+', txt_title):
            raise ValidationError("部门只能是字母、数字、汉字或下划线！")
        return txt_title


# 用户ModelFrom类
class User(BootStrapModelForm):
    """ 创建UserModelForm类 """
    imgcode = forms.CharField(
        label="验证码",
        widget=forms.TextInput(),
    )

    class Meta:
        model = models.UserInfo  # 指定模型类
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput()
        }

        # 不用钩子添加样式widgets写法，关键字【有s】：widgets
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    def clean_name(self):
        txt_name = self.cleaned_data.get("name")
        # 格式验证
        if not re.findall(r'\w+', txt_name):
            raise ValidationError("姓名只能是字母、数字或汉字！")
        if "_" in txt_name or "—" in txt_name:
            raise ValidationError("姓名格式不正确！")
        return txt_name


class UserLogin(BootStrapModelForm):
    """ 登录ModelForm类 """
    imgcode = forms.CharField(
        label="验证码",
        widget=forms.TextInput(),
    )

    class Meta:
        model = models.UserInfo  # 指定模型类
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput()
        }


# 靓号ModelFrom类
class PrettyNum(BootStrapModelForm):
    """ 创建PrettyNum类 """

    # forms包支持自定义新增字段：forms.Charfield(label="自定义")

    # 数据验证方法一：正则表达式验证器
    # phonenum = forms.CharField(
    #     disabled=True,  # 是否可以修改
    #     label="手机号",  # 不加会在前端直接显示字段名
    #     validators=[RegexValidator(r'1[3-9]\d{9}', '手机号格式错误！')],
    # )

    # 数据验证方法二：钩子方法，写入类函数
    # 钩子方法虽然代码复杂，但是推荐使用，因为可以实现对数据重复的校验
    # self表示forms对象本身
    def clean_phonenum(self):
        # 获取到当前用户输入手机号
        txt_phonenum = self.cleaned_data.get("phonenum")
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


class Task(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            "detail": forms.TextInput(attrs={"class": "form-control"}),
        }


class Order(BootStrapModelForm):
    class Meta:
        model = models.Order
        exclude = ["oid", "name"]