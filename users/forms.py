"""
@author: GZP
@contact: 449336625@qq.com
@file: forms.py
@time: 2018/8/25 22:49
"""
import re

from django.contrib.auth.forms import UserCreationForm, forms, AuthenticationForm, PasswordResetForm

from users.models import User


class RegisterModelForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password 1",
        widget=forms.PasswordInput,
        required=False,
    )
    password2 = forms.CharField(
        label="Password 2",
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'phone')
        widgets = {
            'username': forms.widgets.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': '烦请输入真实姓名'}),
            'phone': forms.widgets.NumberInput(attrs={'class': 'form-control',
                                                      'placeholder': '请输入11位手机号码'})
        }

    def clean_password2(self):
        # 覆写该方法, 为了不走注册时密码校验
        # make_random_password
        return "我也不知道填什么"

    def clean_phone(self):
        # 从cleaned_data中取出我们需要的数据
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError('您并未输入电话号码')
        if not len(phone) == 11:
            # 号码长度不正确
            raise forms.ValidationError("该手机号码位数不正确")
        phone_re = "1[3,4,5,7,8]\d{9}"
        if not re.match(phone_re, phone):
            # 号码不是合法号码
            raise forms.ValidationError("您输入的手机号码不合法")
        return phone

    def save(self, commit=True):
        """
        重写方法, 设置默认密码。（如果没有给定密码，密码就会被设置成不使用，同用set_unusable_password()。
        设置user无密码。 不同于密码为空，如果使用 check_password()，则不会返回True。）
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password("0000")  # 设置默认密码为 0000
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    # 直接继承默认的验证表单类
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # 后端验证是否有数据
        if not (username and password):
            raise forms.ValidationError('用户名或密码为空')
        # 调用方法, 验证密码, 成功返回用户
        self.user_cache = self.authenticate(self.request, username=username, password=password)
        return self.cleaned_data

    def authenticate(self, request, username, password=None, **kwargs):
        # 重写authenticate 方法, 跳过Django自带的权限验证
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('用户名或密码错误')
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            else:
                raise forms.ValidationError("用户名或密码错误")

    def user_can_authenticate(self, user):
        """
        验证用户是否激活, 未激活不能登录
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None


class PasswordResetCustomEmailForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email):
            # 该邮箱未注册
            raise forms.ValidationError("该邮箱未注册")
        # 必须返回email, 不然email就会变为None
        return email
