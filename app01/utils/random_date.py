"""
 * @Description: Python3.8
 * @Author: chc
 * @CreateDate: 2022/3/20
 * @Environment: Anaconda3
"""
import random
from datetime import datetime


def get_randate(t1, t2):
    # 设置开始和结束日期时间字符串
    # t1 = "2021-01-01 00:00:00"
    # t2 = "2022-03-20 00:00:00"
    # 字符串=>时间元组=>时间戳
    start = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S').timestamp()
    end = datetime.strptime(t2, '%Y-%m-%d %H:%M:%S').timestamp()
    # 在开始和结束时间戳中随机取一个
    dt = random.randint(int(start), int(end))
    # 时间戳=>时间元组=>字符串
    str_dt = datetime.fromtimestamp(dt).strftime("%Y-%m-%d")
    return str_dt

# if __name__ == '__main__':
#     print(str_dt)
