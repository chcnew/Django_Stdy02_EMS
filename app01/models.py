from django.db import models


class Admin(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.name


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="部门", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    username = models.CharField(verbose_name="用户名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    name = models.CharField(verbose_name="姓名", max_length=16)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2)  # 最大长度10，2位小数，默认值0
    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")
    # 数据固定选择写法
    # 使用时直接获取到对应中文的语法格式：对象名.get_字段名_display()
    # Python中：obj.get_gender_display()
    # html模板语言不能存在括号：obj.get_gender_display
    gender_choices = (
        (0, "女"),
        (1, "男")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")

    # 有约束
    #  1.参数
    #   to="关联表名"
    #   to_field="关联表的列名"
    #  2.Django自动处理列名
    #   depart会自动改为depart_id
    # depart = models.ForeignKey(to="Department", to_field="id")
    #  3.假设某个部门被删除，那在员工表中对应被删除部门的员工数据如何处理？
    #   3.1 级联删除处理
    # depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    #   3.2 置空处理
    # 模板语言中直接使用depart作为对象获取到depar_id对应的行又作为对象再获取到其中的某个信息，如：obj.depart.title
    depart = models.ForeignKey(verbose_name="所属部门", to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class PrettyNum(models.Model):
    """ 靓号表 """
    phonenum = models.CharField(verbose_name="号码", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (0, "未使用"),
        (1, "已使用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=0)


class Task(models.Model):
    """ 任务管理 """
    choices = (
        (0, "普通"),
        (1, "重要"),
        (2, "紧急"),
    )
    level = models.SmallIntegerField(verbose_name="任务级别", choices=choices, default=0)
    title = models.CharField(verbose_name="任务标题", max_length=64)
    detail = models.TextField(verbose_name="详细说明", max_length=300)
    responsible = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)

    def __str__(self):
        return self.level


class Order(models.Model):
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")
    status = models.SmallIntegerField(verbose_name="状态", choices=(
        (0, "待支付"),
        (1, "已支付"),
    ), default=0)
    name = models.ForeignKey(verbose_name="管理员", to="Admin", to_field="id", on_delete=models.CASCADE)
