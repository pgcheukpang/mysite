"""
@author: GZP
@contact: t: 449336625@qq.com
@file: urls.py
@time: 2018/8/15 0015 15:33
"""

from django.conf.urls import url

from home import views

urlpatterns = [
    url('index/$', views.index, name="index"),
    url('map/$', views.baidu_map, name="map"),
    url('contact/$', views.contact, name="contact"),
    # url('galleries/$', views.GalleryListView.as_view(), name="galleries"),
]
