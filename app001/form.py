from django import forms
from django.core.exceptions import ValidationError
from app001 import models


class RegForm(forms.Form):
    username = forms.CharField(
        min_length=1,
        max_length=8,
        label="用户名",
        error_messages={
            "min_length": "用户名太短",
            "required": "用户名不能为空",
        },
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control", "placeholder": "用户名至少一位"}
        )
    )

    password = forms.CharField(
        min_length=4,
        max_length=8,
        label="密码",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control", "placeholder": "密码至少四位"},
            # 注册失败返回错误信息时，保留密码只有密码有这个字段
            render_value=True,
        ),
        error_messages={
            "min_length": "密码至少四位",
            "required": "密码不能为空",
        },

    )

    re_password = forms.CharField(
        min_length=4,
        max_length=8,
        label="重复密码",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control", "placeholder": "不能为空"},
            render_value=True,
        ),
        error_messages={
            "min_length": "密码至少四位",
            "required": "密码不能为空",
        }
    )

    email = forms.EmailField(
        label="邮箱",
        error_messages={
            "invalid": "邮箱格式不正确",
            "required": "邮箱不能为空",
        },
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "不能为空"}
        )
    )

    def clean(self):
        pwd = self.cleaned_data.get("password")
        re_pwd = self.cleaned_data.get("re_password")
        if pwd != re_pwd:
            self.add_error("re_password", ValidationError("两次密码不一致"))
        else:
            return self.cleaned_data

    def clean_username(self):
        a = ["包子", "三胖", '日天']
        username = self.cleaned_data.get("username")
        is_exit = models.UserInfo.objects.filter(username=username)
        if is_exit:
            self.add_error("username", ValidationError("用户名已经注册"))
        for i in a:
            if i in username:
                # raise ValidationError("嘿嘿")
                self.add_error("username", ValidationError("不符合社会主义核心价值观"))
        return username
        # 注意return 的位置

    def clean_email(self):
        email = self.cleaned_data.get("email")
        value = models.UserInfo.objects.filter(email=email)
        if value:
            raise ValidationError("邮箱已存在")
        return email