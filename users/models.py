from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404

from message.models import LeaveMessage


class User(AbstractUser):
    phone = models.CharField(max_length=16, verbose_name='手机号码')
    headshot = models.ImageField(upload_to='avatar/%Y/%m/%d', default="alien.jpg", verbose_name='头像')
    password = models.CharField(max_length=128, verbose_name='密码', default='Changeme123')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username

    # 判断是否点赞
    def is_favorites(self, msgid):
        item = self.like_msg_set.filter(pk=msgid)
        # print(msgid, item)
        if self.like_msg_set.filter(pk=msgid):
            # 已对该留言点赞
            # print("已对该留言点赞")
            return True
        else:
            # 未对该留言点赞
            # print("未对该留言点赞")
            return False

    # 建立点赞
    def add_favorites(self, msgid):
        # print("那就建立点赞关系")
        msg = get_object_or_404(klass=LeaveMessage, id=msgid)
        self.like_msg_set.add(msg)

    # 取消点赞
    def cancel_favorites(self, msgid):
        # print("那就取消点赞")
        msg = get_object_or_404(klass=LeaveMessage, id=msgid)
        self.like_msg_set.remove(msg)

    # 获取已点赞的留言id列表
    def get_favorites_id_list(self):
        id_list = []
        likes = self.like_msg_set.all()
        for msg_obj in likes:
            id_list.append(msg_obj.id)
        return id_list
