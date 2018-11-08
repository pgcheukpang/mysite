"""
@author: GZP
@contact: 449336625@qq.com
@file: urls.py
@time: 2018/8/25 17:56
"""

from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^password_change/$', views.PasswordChangeCustomView.as_view(), name='password_change'),  # 修改密码
    url(r'^password_reset/$', views.PasswordResetCustomView.as_view(), name='password_reset'),  # 重置密码

    url(r'^user_info/$', views.UserInfoView.as_view(), name='user_info'),  # 个人信息
    url(r'^user_headshot/$', views.UserHeadshotView.as_view(), name='user_headshot'),  # 个人信息
]
