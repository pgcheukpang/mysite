"""
@author: GZP
@contact: 449336625@qq.com
@file: urls.py
@time: 2018/9/17 0017 9:32
"""
from django.conf.urls import url

from photo import views

urlpatterns = [
    # 相册列表
    url(r'^albums/$', views.PhotoAlbumListView.as_view(), name="albums"),
    # 相册详情列表
    url(r'^albums/(?P<albums_id>\d+)/', views.PhotoAlbumDetailView.as_view(), name="albums_detail"),
    # 照片上传的连接(个人使用)
    url(r'^uploads/$', views.PhotoView.as_view(), name="uploads"),
]
