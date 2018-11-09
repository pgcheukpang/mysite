# -*- coding: utf-8 -*-
"""
开发框架公用方法
1. 页面输入内容转义（防止xss攻击）
from common.utils import html_escape, url_escape, texteditor_escape
2. 转义html内容
html_content = html_escape(input_content)
3. 转义url内容
url_content = url_escape(input_content)
"""
import math


def html_escape(html, is_json=False):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true, the quotation mark character (")
    is also translated.
    rewrite the cgi method
    @param html: html代码
    @param is_json: 是否为json串（True/False） ，默认为False
    """
    # &转换
    if not is_json:
        html = html.replace("&", "&amp;")  # Must be done first!
    # <>转换
    html = html.replace("<", "&lt;")
    html = html.replace(">", "&gt;")
    # 单双引号转换
    if not is_json:
        html = html.replace(' ', "&nbsp;")
        html = html.replace('"', "&quot;")
        html = html.replace("'", "&#39;")
    return html


def url_escape(url):
    url = url.replace("<", "")
    url = url.replace(">", "")
    url = url.replace(' ', "")
    url = url.replace('"', "")
    url = url.replace("'", "")
    return url


def custom_paginator(current_page, total_pages, max_page):
    # total_pages：总页数
    # max_page：页面显示可选择的页数
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
