from django.shortcuts import render
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from photo.forms import PhotoForm
from photo import models


# 相簿列表视图
class PhotoAlbumListView(ListView):
    model = models.Album
    template_name = "photo/album_list.html"

    def get_context_data(self, **kwargs):
        """
        重写方法, 实现对相册列表分行
        """
        context = super(PhotoAlbumListView, self).get_context_data(**kwargs)
        album_list = self.get_queryset()
        # 3个一组, 根据组数组装二维数组
        group_nums = len(album_list) // 3 if len(album_list) % 3 == 0 else len(album_list) // 3 + 1
        ret_list = [[] for _ in range(group_nums)]
        # 开始分组
        for i, album in enumerate(album_list, start=0):
            ret_list[i // 3].append(album)
        album_list = ret_list
        context.update({"album_list": album_list})
        return context


# 图片上传视图
class PhotoView(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {"form": PhotoForm()}
        return render(request, "photo/photo_upload.html", context=context)

    @method_decorator(login_required)
    def post(self, request):
        form = PhotoForm(request.POST, request.FILES)
        instance_list = []
        if form.is_valid():
            # 检验成功，都为图片类型
            uploader = request.user.username
            img_files = request.FILES.getlist("img")
            # 因为不是Model, 没有save方法, 要手动遍历保存为实例
            for index, img_file in enumerate(img_files, 1):
                # 因为模型里自定义了路径, 所以这里直接保存实例就可以了
                album = form.cleaned_data.get("album")
                name = ''.join(reversed(list(''.join(reversed(list(img_file.name)))[:30])))
                photo = models.Photo(name=name, img=img_file, album=album, uploader=uploader)
                photo.save()
                instance_list.append(photo)
        else:
            # 检验不成功, 即有非图片文件
            pass

        # 3个一组, 根据组数组装二维数组
        group_nums = len(instance_list) // 3 if len(instance_list) % 3 == 0 else len(instance_list) // 3 + 1
        ret_list = [[] for _ in range(group_nums)]
        # 开始分组
        for i, instance in enumerate(instance_list, start=0):
            ret_list[i // 3].append(instance)

        context = {"form": form, "instance_list": instance_list, "ret_list": ret_list}
        return render(request, "photo/photo_upload.html", context=context)


# 相簿详情视图
class PhotoAlbumDetailView(View):
    def get(self, request, albums_id):
        album = models.Album.objects.get(id=albums_id)
        photos = album.photo_set.all()
        context = {"photos": photos}
        return render(request, "photo/album_detail.html", context=context)
