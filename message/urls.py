"""
@author: GZP
@contact: 449336625@qq.com
@file: urls.py
@time: 2018/8/24 0024 10:27
"""

from django.conf.urls import url
from message import views

urlpatterns = [
    url(r'^leaveword/', views.MessageListView.as_view(), name="leaveword"),
    url(r'^addmsg/$', views.MessageCreateView.as_view(), name="addmsg"),
    # 留言正文的点赞逻辑
    url(r'^addfavor/(?P<msgid>\d+)/', views.FavorView.as_view(), name="addfavor"),
    # 侧边栏最热榜的点赞逻辑
    url(r'^hottest_like/(?P<msgid>\d+)/', views.HottestLikeView.as_view(), name="hottest_like"),
    # 留言删除
    url(r'^delmsg/', views.MessageDeleteView.as_view(), name="delmsg"),
]
