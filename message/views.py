from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse
from django.views.generic import ListView, CreateView, View
from django.utils.decorators import method_decorator
from django.views.generic.list import MultipleObjectMixin
from django.http.response import JsonResponse

from message.models import LeaveMessage
from message.forms import LeaveMessageModelForm
from message import utils


class MessageListView(ListView):
    """显示所有留言"""
    model = LeaveMessage
    template_name = 'message/message_list.html'
    paginate_by = 6  # 不需要自己写捕捉客户端输入的页码号数异常

    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(MessageListView, self).get_queryset().order_by('-created_time')

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        # 自定义分页
        paginator = context.get("paginator")
        message_sums = paginator.count
        sub_msg_list = context.get('page_obj')
        start, end = utils.custom_paginator(sub_msg_list.number, paginator.num_pages, 5)
        # 登陆用户已点赞的留言
        id_list = self.request.user.get_favorites_id_list()
        context.update({
            'form': LeaveMessageModelForm(),  # 留言表单
            'message_sums': message_sums,
            'page_range': range(start, end + 1),
            "id_list": id_list,
        })
        return context


class MessageCreateView(MultipleObjectMixin, CreateView):
    """新增一条留言, 再继承MultipleObjectMixin, 用于在表单验证不通过时, 显示正常的内容和分页"""
    model = LeaveMessage
    form_class = LeaveMessageModelForm
    template_name = 'message/message_list.html'
    paginate_by = 6

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()  # CreateView里不会定义self.object_list, 故要手动添加
        return super(MessageCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('message:leaveword')

    # 重写方法，在验证留言时加入用户信息
    def form_valid(self, form):
        form.instance.messager = self.request.user
        return super(MessageCreateView, self).form_valid(form)

    def get_queryset(self):
        return super(MessageCreateView, self).get_queryset().order_by('-created_time')

    def get_context_data(self, **kwargs):
        context = super(MessageCreateView, self).get_context_data(**kwargs)
        # 自定义分页
        message_sums = self.get_queryset().count()
        paginator = context.get("paginator")
        sub_msg_list = context.get('page_obj')
        start, end = utils.custom_paginator(sub_msg_list.number, paginator.num_pages, 5)
        # 登陆用户已点赞的留言
        id_list = self.request.user.get_favorites_id_list()
        context.update({
            'message_sums': message_sums,
            'page_range': range(start, end + 1),
            "id_list": id_list,
        })
        return context


class MessageDeleteView(View):
    """删除一条留言"""

    def post(self, request):
        try:
            with transaction.atomic():
                LeaveMessage.objects.get(id=request.POST.get('id')).delete()
                data = {"code": 200, "msg": "已成功删除", "status": True}
        except:
            data = {"code": 200, "msg": "出现错误，删除失败", "status": False}
        return JsonResponse(data=data, status=data["code"])


class FavorView(View):
    # 实现正文部分的点赞功能
    # 增加一个点赞
    def post(self, request, msgid):
        # 获取当前登录用户
        user = request.user
        if user.is_favorites(msgid):
            # 用户已点赞, 则取消点赞
            user.cancel_favorites(msgid)
            data = {"code": 200, "msg": "已取消点赞", "like_status": 0}
        else:
            # 用户没点赞, 则在增加点赞
            user.add_favorites(msgid)
            data = {"code": 200, "msg": "点赞成功", "like_status": 1}
        return JsonResponse(data=data, status=data["code"])


class HottestLikeView(View):
    # 实现侧边栏的点赞功能
    # 增加一个点赞
    def post(self, request, msgid):
        # 获取当前登录用户
        user = request.user
        if user.is_favorites(msgid):
            # 用户已点赞, 则返回已点赞提示
            data = {"code": 201, "msg": "您已点赞过该留言", "like_status": 0}
        else:
            # 用户没点赞, 则在增加点赞
            user.add_favorites(msgid)
            data = {"code": 200, "msg": "点赞成功", "like_status": 1}
        return JsonResponse(data=data, status=data["code"])
