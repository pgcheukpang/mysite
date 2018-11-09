import base64
import json
import os
import time
import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import SuccessURLAllowedHostsMixin, PasswordChangeView, PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.fields.files import ImageFieldFile
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, resolve_url
from django.shortcuts import redirect, reverse
from django.contrib.auth import login as auth_login, REDIRECT_FIELD_NAME
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView

from django.conf import settings
from users.forms import RegisterModelForm, LoginForm, PasswordResetCustomEmailForm


def register(request):
    form = RegisterModelForm()
    # 获取跳转地址
    redirect_to = request.POST.get('next', request.GET.get('next', None))
    # 判断是什么方法提交
    if request.method == 'POST':
        # 先生成表单
        form = RegisterModelForm(request.POST)
        # 判断表单数据是否合法
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # 注册成功后直接登录
            # 判断是否存在redirect_to
            if redirect_to:
                return redirect(redirect_to)
            else:
                # 没有就重定向至首页
                return redirect(reverse('home:index'))
    # 验证不合法或者不是POST提交
    return render(request, 'users/register.html', {'form': form, 'next': redirect_to})


class LoginView(SuccessURLAllowedHostsMixin, FormView):
    """
    Displays the login form and handles the login action.
    """
    form_class = LoginForm  # 改成自定义的Form
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME  # 'next'
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        """
            Django拓展该方法是对已通过用户验证的访问进行重定向。例如：先前已登录且没有注销和清除COOKIES，
        当访问/user/login/时，若设置redirect_authenticated_user = True， 则会将用户请求重定向至next或者
        setting.LOGIN_REDIRECT_URL
        """
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        """如果存在next=xxxxx, 返回用户发起的该重定向 URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,  # TCP/IP 地址
            'site_name': current_site.name,  # TCP/IP 地址
        })
        if self.extra_context is not None:
            context.update(self.extra_context)
        return context


class PasswordChangeCustomView(PasswordChangeView):
    # 继承DJango封装好的PasswordChangeView

    def get_success_url(self):
        # 重写方法, 指定页面跳转逻辑
        url = self.get_redirect_url()
        return url or reverse("password_change_done")

    def get_redirect_url(self):
        # 获取重定向url
        redirect_to = self.request.POST.get('next', self.request.GET.get('next', ''))
        # 检查url是否安全
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else None


# 继承PasswordResetView类, 为了使用自定义的发邮箱模版
class PasswordResetCustomView(PasswordResetView):
    # 邮件内容的模板(注释了才是使用默认)
    # email_template_name = 'registration/password_reset_email.html'

    # 邮件主题的模板(注释了才是使用默认)
    # subject_template_name = 'registration/password_reset_subject.txt'

    # 指定重置密码页面的模板名称(输入邮箱页面)
    template_name = "registration/password_reset_form.html"

    # 指定对邮箱进行验证的Form,默认为'PasswordResetForm',如果要实现'邮箱未注册'的提示,可以重写该Form的clean()方法
    form_class = PasswordResetCustomEmailForm


"""
属性:
template_name:指定重置密码页面的模板名称(输入邮箱页面),默认为'registration/password_reset_form.html'
form_class:指定对邮箱进行验证的Form,默认为'PasswordResetForm',如果要实现'邮箱未注册'的提示,可以重写该Form的clean()方法.
email_template_name:邮件内容的模板,默认为'registration/password_reset_email.html'.
subject_template_name:邮件主题的模板,默认'registration/password_reset_subject.txt'.
success_url:邮件发送成功(或邮箱未注册)后重定向的URL.
form_email: 发送邮件的地址.默认使用DEFAULT_FORM_EMAIL.需要在settings.py文件中进行邮箱参数的配置.
extra_context: 需要添加到模板中的额外上下文数据.
"""

"""
还有三4个页面可以还没自定义:
1. PasswordResetCustomView里的email_template_name: password_reset_email.html  
2. PasswordResetCustomView里的subject_template_name: password_reset_subject.txt  
3. 提示密码重置链接已经发送的模版password_reset_done.html
4. 提示新密码设置成功的模版password_reset_complete.html
"""


# 用户详情
class UserInfoView(View):
    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserInfoView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, "users/user_info.html")


# 修改头像
class UserHeadshotView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserHeadshotView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, "users/user_headshot.html")

    def post(self, request):
        data = json.loads(request.body)
        imgBase = data.get("imgBase")
        img_b64_string = imgBase.split(",", 1)[1]  # 获取经过base64编码的jpeg图片数据
        convert_img_raw_data = base64.b64decode(img_b64_string)  # 解码得到图片的字节数据<class 'bytes'>
        photo_suffix = "jpeg"

        # 随机文件名(使用uuid + 时间戳)
        filename = "{}.{}".format(uuid.uuid4().hex[:4] + str(int(time.time() * 1000)),
                                  photo_suffix)
        # 保存文件夹的绝对路径
        folder = os.path.join(settings.MEDIA_ROOT, "avatar/%d/" % request.user.id)
        if not os.path.exists(folder):
            os.makedirs(folder)
        # 新文件的绝对路径
        dest_filename = folder + filename
        # 新建文件写入图片数据
        with open(dest_filename, "wb") as img:
            img.write(convert_img_raw_data)

        # 删除原头像文件
        user = request.user
        old_name = user.headshot.name  # 绝对路径减去( MEDIA_ROOT + \ )
        if old_name == "alien.jpg":
            # 默认的头像不要删除
            pass
        else:
            # old_abs_path = settings.MEDIA_ROOT + "/" + old_name
            old_abs_path = request.user.headshot.path  # 绝对路径
            os.remove(old_abs_path)

        # 更新头像数据
        user.headshot = "avatar/%d/" % request.user.id + filename
        user.save(update_fields=["headshot", ])
        return JsonResponse({"msg": "success"})
