"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 
 * @Environment: Anaconda3
"""
from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    """自定义分页组件"""

    def __init__(self, request, queryset, page_size=10, page_jump_error="", plus=5, page_param="page"):
        """
        :param request: request包
        :param queryset: 传入一个queryset对象
        :param page_size: 设置页面显示行数，默认10行
        :param page_jump_error: 跳转框错误提示
        :param plus: 显示当前页及前5页后5页
        :param page_param: get请求传入的name属性值

        Viesws.py中用法说明：
        from app01.utils.pagination import Pagination
        page_obj = Pagination(request, queryset, plus=3)  # 实例化对象(页头已经导入)，参数初始化
        page_queryset = page_obj.page_queryset  # 显示行方法**[x:y]
        page_str = page_obj.html()  # 生成html代码
        context = {
            "page_queryset": page_queryset,  # 设置显示条件及行数
            "search_data": search_data,  # 搜索框value值
            "page_str": page_str,  # 封装的html代码
            "page_jump_error": page_obj.page_jump_error, # 页码数据校验错误提示
            "page": page_obj.page,  # 页码显示值(value)
            ... ...
        }
        return render(request, "pretty_list.html", context)
        """

        # 自定义增加url-get请求
        self.page_param = page_param
        query_dict = copy.deepcopy(request.GET)
        query_dict_mutable = True
        self.query_dict = query_dict  # url里边原有参数,注意：只是?后边参数部分，如：srch=4645
        # query_dict.setlist("page", [1]) #增加page=1,变为：<QueryDict: {'srch': ['sada'], 'page': ['1'],}>
        # print(query_dict.urlencode()) # 参数变为：srch=4645&page=1

        # 总行数：total_count
        total_count = queryset.count()
        # 总页数：total_page_count
        self.page_size = page_size
        total_page_count, remainder = divmod(total_count, self.page_size)
        if remainder:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.remainder = remainder

        page = request.GET.get(page_param)  # 默认"page"传入
        # 跳转页码数据验证
        # 字符串.isdigit()判断字符串是否只有数字且在页码范围
        self.page_jump_error = page_jump_error

        if page == "" or page is None or self.total_page_count == 0:
            self.page_jump_error = ""
            page = 1  # 验证失败显示第一页

        else:
            if (not page.isdecimal()) or (page.isdecimal() and (int(page) <= 0 or int(page) > total_page_count)):
                self.page_jump_error = "输入错误！整数页码[1~" + str(self.total_page_count) + "]"
                page = 1  # 验证失败显示第一页
            else:
                page = int(page)  # 当前页

        self.page = page
        self.page_size = page_size

        # 显示id对应行数的起始值
        self.start = (self.page - 1) * self.page_size  # 区间最小值-此处page为传入参数，不是对象本身的page。
        self.end = self.page * self.page_size  # 区间最大值[不含]-此处page为传入参数，不是对象本身的page。
        self.page_queryset = queryset[self.start:self.end]
        self.plus = plus

    def html(self):
        # 数据<=11页，显示到最大页
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据>11页,当前页<=5时不能变化
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页>5且当前页+5大于总页数，则最后页=总页数，起始页=总页数-10
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    # 正常情况
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 生成页码按钮,附带首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_lst = ['<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())]
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_lst.append(prev)
        # 页码
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_lst.append(ele)
        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_lst.append(prev)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_lst.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        # 字符转html代码处理
        page_str = mark_safe("".join(page_str_lst))
        # 返回生成的html代码
        return page_str
