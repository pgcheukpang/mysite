import time
import uuid
import os

from django.db import models


# class Album(models.Model):
#     name = models.CharField(max_length=16, verbose_name="类别")
#
#     def __str__(self):
#         return self.name


class Album(models.Model):
    name = models.CharField(max_length=24, verbose_name="相册名称")
    desc = models.CharField(max_length=128, verbose_name="相册描述")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "相册"
        verbose_name_plural = "相册"

    def __str__(self):
        return self.name


def photo_directory_path(instance, filename):
    # instance代表当前的Photo实例
    photo_suffix = filename.split(".")[-1]
    # filename = "{}.{}".format(uuid.uuid4().hex[:8], photo_suffix)  # 随机文件名(使用uuid)
    filename = "{}.{}".format(uuid.uuid4().hex[:4] + str(int(time.time() * 1000)), photo_suffix)  # 随机文件名(使用uuid + 时间戳)
    # 上传路径, eg: albums\1\7eee24f4.png, 这也是存储在数据库的数据
    upload_to = os.path.join("albums", str(instance.album.pk), filename)
    return upload_to


class Photo(models.Model):
    name = models.CharField(max_length=32, verbose_name="照片名称", blank=True, null=True)
    desc = models.CharField(max_length=64, verbose_name="照片描述", blank=True, null=True)
    img = models.ImageField(upload_to=photo_directory_path, verbose_name="照片")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    uploader = models.CharField(max_length=16, null=True, blank=True, verbose_name="上传者")
    album = models.ForeignKey(Album, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="所属相册")

    class Meta:
        verbose_name = "照片"
        verbose_name_plural = "照片"

    def __str__(self):
        return self.name or self.pk
