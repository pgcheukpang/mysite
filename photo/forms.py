"""
@author: GZP
@contact: 449336625@qq.com
@file: form.py
@time: 2018/9/17 0017 15:16
"""
from django import forms

from photo.models import Photo, Album


class PhotoForm(forms.Form):
    # name = forms.CharField(label="照片名称")
    img = forms.ImageField(label="上传照片", widget=forms.FileInput(attrs={"multiple": "multiple"}))  # 仍然有是是否相片文件的校验
    album = forms.ModelChoiceField(label="所属相册", queryset=Album.objects.all(), required=True)


