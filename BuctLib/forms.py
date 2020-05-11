from django import forms
from django.forms import widgets
from .src.formCheck import *
from BuctLib.models import User, Manager, ReaderClass, Reader, GENDER_CHOICE, SCHOOLS
#   修改信息表单
from .src.formCheck import *


class ReadInfForm(forms.Form):
    Tel = forms.CharField(label="电话号码", max_length=20,
                          required=True,
                          min_length=11,
                          widget=widgets.TextInput(
                              attrs={'class': 'form-control', "data-inputmask": '"mask":"99999999999"',
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
    # 根据读者等级字段来查表生成选择选项
    Class = forms.TypedChoiceField(label="级别", disabled=True, required=False,
                                   choices=map(lambda item: (item["Class"], item["Class"]),
                                               ReaderClass.objects.values()),
                                   widget=widgets.Select(attrs={"class": "form-control select3"})
                                   )
    Type = forms.TypedChoiceField(label="类别", choices=[('1', '学生'), ('2', '教职工')], empty_value="学生",
                                  widget=widgets.Select(attrs={"class": "form-control select5"}))

    def clean(self):
        changed_datas = self.changed_data
        # 电话号码和邮箱需要验证唯一性
        if "Tel" in changed_datas:
            Tel = self.cleaned_data.get("Tel")
            if len(Tel) < 11 or '_' in Tel:
                raise forms.ValidationError({"Tel": '电话号码长度至少11位'})
            else:
                if User.objects.filter(Tel=Tel).exists():
                    raise forms.ValidationError({"Tel": '电话号码已存在'})
        if "Email" in changed_datas:
            Email = self.cleaned_data.get("Email")
            errors = check_email(Email)
            if errors != "":
                raise forms.ValidationError({"Email": errors})
            else:
                if User.objects.filter(Email=Email).exists():
                    raise forms.ValidationError({"Email": '邮箱已存在'})

        return self.cleaned_data


# class ReaderForm(forms.ModelForm):
#     class Meta:
#         model = Reader
#         fields = ["ReaderID", "AccountID", "Gender", "Name", "School", "Class", "Type"]

class ApplyChangeClass(forms.Form):
    ReaderID = forms.CharField(label="读者卡号", max_length=30, disabled=True, required=False,
                               widget=widgets.TextInput(attrs={"class": "form-control"}))
    Class = forms.ChoiceField(label="级别", required=False,
                                   choices=map(lambda item: (item["Class"], item["Class"]+"-------------------------可借%d本---------------------借阅时间上限%d天" % (item["Limited"], item["Days"])),
                                               ReaderClass.objects.values()),
                                   widget=widgets.Select(attrs={"class": "form-control select3"}))
    Message = forms.CharField(label="备注", empty_value="", required=False, widget=forms.Textarea(attrs={"class": "form-control"}))

    def clean(self):

        if "Class" not in self.changed_data:
            raise forms.ValidationError({"Class": '申请的级别不能与目前相同'})

        if not self.has_changed():
            raise forms.ValidationError({"Class": '申请的级别不能与目前相同'})

        return self.cleaned_data
