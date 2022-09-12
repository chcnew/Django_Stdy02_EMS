"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/3/14
 * @Environment: Anaconda3
"""
from django import forms


class BootStrap(object):
    # 给前端添加样式快速写法,与Meta类同级【工作必须使用】
    def __init__(self, *args, **kwargs):  # 有self，代表本函数内参数传递
        super().__init__(*args, **kwargs)  # 无self，使用父类方法，其实就是使用类Meta的对象
        # 循环找到所有插件，字典对象
        for name, field in self.fields.items():
            field.widget.attrs = {
                "class": "form-control",
                "placeholder": field.label,
            }


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass


class BootStrapForm(BootStrap, forms.Form):
    pass
