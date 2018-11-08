"""
@author: GZP
@contact: 449336625@qq.com
@file: forms.py
@time: 2018/8/24 0024 10:52
"""
import json

from django import forms

from common.msg_check import TextReviews
from message.models import LeaveMessage


class LeaveMessageModelForm(forms.ModelForm):
    class Meta:
        model = LeaveMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': "走过路过不要错过哟"})
        }

    def clean_content(self):
        content = self.cleaned_data.get("content")
        self.ret_json = TextReviews.get_check_json(content=content)  # 访问百度接口, 审核留言内容
        # print(json.dumps(self.ret_json))
        if self.ret_json.get("result").get("spam") == 1:
            # 审核未通过, 有敏感词
            raise forms.ValidationError("您输入的内容含敏感词汇，未能成功留言")
        return content

    def save(self, commit=True):
        """
        重写方法, 根据审核结果执行不同操作
        """
        leave_msg = super(LeaveMessageModelForm, self).save(commit=False)

        if self.ret_json.get("error_code", None):
            # 异常返回, 记录下来, 给予通过
            # print("异常返回")
            error_msg = self.ret_json.get("error_msg")
            leave_msg.is_error_occured = "1"  # 1: 出现异常
            leave_msg.error_msg = error_msg
            leave_msg.reviewed_status = "2"  # 2: 需要复审
        elif self.ret_json.get("result").get("spam") == 0:
            # 审核通过
            # print("审核通过")
            pass
        elif self.ret_json.get("result").get("spam") == 2:
            # 审核需复查
            # print("审核需复查")
            review_obj_list = self.ret_json.get("result").get("review")
            hit = ""
            for obj in review_obj_list:
                for item in obj.get("hit"):
                    hit += (item + " ")
            leave_msg.reviewed_status = "2"  # 2: 需要复审
            leave_msg.reviewed_content = hit
        if commit:
            leave_msg.save()
        return leave_msg
