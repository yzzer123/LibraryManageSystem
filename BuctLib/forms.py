from django import forms
from django.forms import widgets

from BuctLib.models import *
#   修改信息表单
from .src.formCheck import *


class ReadInfForm(forms.Form):
    Tel = forms.CharField(label="电话号码", max_length=20,
                          required=True,
                          min_length=11,
                          widget=widgets.TextInput(
                              attrs={'class': 'form-control', "data-inputmask": '"mask":"999-9999-9999"',
                                     "data-mask": ""}),
                          error_messages={
                              'required': "电话号码不能为空",
                              'max_length': '电话号码长度不能超过20',
                              'min_length': '电话号码要11位起'
                          })
    Email = forms.EmailField(label="邮箱", required=True,
                             widget=widgets.EmailInput(attrs={"class": "form-control"}),
                             error_messages={
                                 'required': '邮箱不能为空'
                             })
    ReaderID = forms.CharField(label="读者卡号", max_length=30, disabled=True, required=False,
                               widget=widgets.TextInput(attrs={"class": "form-control"})
                               )
    AccountID = forms.CharField(label="账号", max_length=40, disabled=True, required=False,
                                widget=widgets.TextInput(attrs={"class": "form-control"}))
    Gender = forms.TypedChoiceField(label="性别", choices=GENDER_CHOICE, initial=3, empty_value="保密",
                                    widget=widgets.Select(attrs={"class": "form-control select4"}))
    Name = forms.CharField(label="姓名", empty_value="", max_length=30, required=False,
                           widget=widgets.TextInput(attrs={"class": "form-control"}),
                           error_messages={
                               "max_length": "最长姓名不能超过30个字符",
                           })
    School = forms.TypedChoiceField(label="学院", choices=SCHOOLS,
                                    widget=widgets.Select(attrs={"class": 'form-control select2'}),
                                    empty_value="信息技术与科学学院")
    Class = forms.TypedChoiceField(label="级别", disabled=True, required=False,
                                   choices=map(lambda item: (item["Class"], item["Class"]),
                                               ReaderClass.objects.values()),
                                   widget=widgets.Select(attrs={"class": "form-control select3"})
                                   )
    Type = forms.TypedChoiceField(label="类别", choices=[('1', '学生'), ('2', '教职工')], empty_value="学生",
                                  widget=widgets.Select(attrs={"class": "form-control select5"}))


class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ["ReaderID", "AccountID", "Gender", "Name", "School", "Class", "Type"]
