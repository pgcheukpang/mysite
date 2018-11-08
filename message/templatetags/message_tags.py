"""
@author: GZP
@contact: 449336625@qq.com
@file: message_tags.py
@time: 2018/9/12 0012 9:14
"""
from django import template
from django.db.models import Count, Q

from message.models import LeaveMessage

register = template.Library()


# 获取最新留言
@register.simple_tag
def get_recent_messages(limit=5):
    return LeaveMessage.objects.order_by('-created_time')[:limit]


# 获取热门留言
@register.simple_tag
def get_hot_messages(limit=5):
    return LeaveMessage.objects.annotate(favor_count=Count("favorites")).filter(~Q(reviewed_status="2")).order_by(
        "-favor_count", "-created_time")[:limit]
