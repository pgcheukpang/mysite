"""
@author: GZP
@contact: 449336625@qq.com
@file: utils.py
@time: 2018/9/9 21:24
"""

import math


# total_pages：总页数
# max_page：页面显示可选择的页数


def custom_paginator(current_page, total_pages, max_page):
    middle = math.ceil(max_page / 2)

    # 偶数页
    if max_page % 2 == 0:
        if total_pages <= max_page:
            start = 1
            end = total_pages
        elif current_page <= middle:
            start = 1
            end = max_page
        elif middle < current_page < total_pages - middle + 1:
            start = current_page - middle + 1
            end = current_page + middle
        else:
            start = total_pages - max_page + 1
            end = total_pages
        return start, end

    # 奇数页
    else:
        if total_pages <= max_page:
            start = 1
            end = total_pages
        elif current_page <= middle:
            start = 1
            end = max_page
        elif middle < current_page < total_pages - middle + 1:
            start = current_page - middle + 1
            end = current_page + middle - 1
        else:
            start = total_pages - max_page + 1
            end = total_pages
        return start, end
