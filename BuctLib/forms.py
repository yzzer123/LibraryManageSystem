from django import forms
from django.forms import widgets
from .src.formCheck import *
from BuctLib.models import Book, User, Manager, ReaderClass, Reader, GENDER_CHOICE, SCHOOLS, Notice, Message, Fine
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
                              choices=map(lambda item: (item["Class"], item[
                                  "Class"] + "-------------------------可借%d本---------------------借阅时间上限%d天" % (
                                                            item["Limited"], item["Days"])),
                                          ReaderClass.objects.values()),
                              widget=widgets.Select(attrs={"class": "form-control select3"}))
    Message = forms.CharField(label="备注", empty_value="", required=False,
                              widget=forms.Textarea(attrs={"class": "form-control"}))

    def clean(self):

        if "Class" not in self.changed_data:
            raise forms.ValidationError({"Class": '申请的级别不能与目前相同'})

        if not self.has_changed():
            raise forms.ValidationError({"Class": '申请的级别不能与目前相同'})

        return self.cleaned_data


class NewMessForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['Status']
        widgets = {
            'Title': forms.TextInput(attrs={'class': 'form-control'}),
            'ReaderID': widgets.Select(attrs={"class": "form-control select2"}),
            'Content': forms.Textarea(attrs={'class': 'form-control'})
        }
        error_messages = {
            'Title': {'required': '标题是必填的'},  # 设置错误提示信息
            'Content': {'required': '内容未填写'},
            'ReaderID': {'required': '请选择一个发送对象'},
        }


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        exclude = ["NTime", "ReadTimes"]
        widgets = {
            'Title': forms.TextInput(attrs={'class': 'form-control'}),
            'Content': forms.Textarea(attrs={'class': 'form-control'})
        }
        error_messages = {
            'Title': {'required': '标题是必填的'},  # 设置错误提示信息
            'Content': {'required': '内容未填写'},
        }


class AdminInfForm(forms.Form):
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
    AdminID = forms.CharField(label="读者卡号", max_length=30, disabled=True, required=False,
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


class AddReadInfForm(forms.Form):
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
    ReaderID = forms.CharField(label="读者卡号", max_length=30, required=True,
                               widget=widgets.TextInput(attrs={"class": "form-control"}),
                               error_messages={
                                   'required': '学号不能为空'
                               }
                               )
    AccountID = forms.CharField(label="账号", max_length=40, required=True,
                                widget=widgets.TextInput(attrs={"class": "form-control"}),
                                error_messages={
                                    'required': '账号不能为空'
                                })

    School = forms.TypedChoiceField(label="学院", choices=SCHOOLS,
                                    widget=widgets.Select(attrs={"class": 'form-control select2'}),
                                    empty_value="信息技术与科学学院")

    # 根据读者等级字段来查表生成选择选项
    Class = forms.TypedChoiceField(label="级别", required=True,
                                   choices=map(lambda item: (item["Class"], item["Class"]),
                                               ReaderClass.objects.values()),
                                   widget=widgets.Select(attrs={"class": "form-control select3"}),
                                   error_messages={
                                       'required': '级别不能为空'
                                   }
                                   )
    Type = forms.TypedChoiceField(label="类别", choices=[('1', '学生'), ('2', '教职工')], empty_value="学生", required=True,
                                  widget=widgets.Select(attrs={"class": "form-control select5"}))

    def clean(self):

        Email = self.cleaned_data.get("Email")
        Tel = self.cleaned_data.get("Tel")
        ReaderID = self.cleaned_data.get("ReaderID")
        AccountID = self.cleaned_data.get("AccountID")

        # 电话号码和邮箱需要验证唯一性

        if len(Tel) < 11 or '_' in Tel:
            raise forms.ValidationError({"Tel": '电话号码长度至少11位'})
        else:
            if User.objects.filter(Tel=Tel).exists():
                raise forms.ValidationError({"Tel": '电话号码已存在'})
        errors = check_email(Email)
        if errors != "":
            raise forms.ValidationError({"Email": errors})
        else:
            if User.objects.filter(Email=Email).exists():
                raise forms.ValidationError({"Email": '邮箱已存在'})
        if User.objects.filter(AccountID=AccountID).exists():
            raise forms.ValidationError({"AccountID": '账号已存在'})
        if Reader.objects.filter(ReaderID=ReaderID).exists():
            raise forms.ValidationError({"ReaderID": '学号已存在'})

        return self.cleaned_data


class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = "__all__"
        widgets = {
            'LimitDay': forms.NumberInput(attrs={'class': 'form-control'}),
            'FineMoney': forms.NumberInput(attrs={'class': 'form-control'})
        }
        error_messages = {
            'LimitDay': {'required': '上限天数是必填的'},  # 设置错误提示信息
            'FineMoney': {'required': '罚金未填写'},
        }

    def clean_LimitDay(self):
        day = self.cleaned_data.get("LimitDay")

        if Fine.objects.filter(LimitDay=day).exists():
            raise forms.ValidationError({"LimitDay": '该时间上限的惩罚规则已存在，可以尝试修改罚金'})
        return int(day)

    def clean_FineMoney(self):
        money = self.cleaned_data.get("FineMoney")
        return int(money)


class ClassForm(forms.ModelForm):
    class Meta:
        model = ReaderClass
        fields = "__all__"
        widgets = {
            'Class': forms.TextInput(attrs={'class': 'form-control'}),
            'Limited': forms.NumberInput(attrs={'class': 'form-control'}),
            'Days': forms.NumberInput(attrs={'class': 'form-control'})
        }
        error_messages = {
            'Class': {'required': '等级名称是必填写的'},  # 设置错误提示信息
            'Limited': {'required': '借阅书籍数量未填写'},
            'Days': {'required': '书籍借阅天数未填写'},

        }

    def clean_Class(self):
        Class = self.cleaned_data.get("Class")

        if ReaderClass.objects.filter(Class=Class).exists():
            raise forms.ValidationError({"Class": '该级别名称已经存在，请尝试其他名称，或者修改该等级读者权限'})
        return Class


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ["ReadTimes", "NumNow"]
        widgets = {
            'BName': forms.TextInput(attrs={'class': 'form-control'}),
            'Publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'Author': forms.TextInput(attrs={'class': 'form-control'}),
            'Content': widgets.Textarea(attrs={'class': 'form-control', 'style': 'max-height:150px;'}),
            'Price': forms.NumberInput(attrs={'class': 'form-control'}),
            'NumInLib': forms.NumberInput(attrs={'class': 'form-control'}),
            "Category": widgets.Select(attrs={"class": 'form-control select2'}),
            'PubTime': forms.DateInput(attrs={'class': 'form-control float-right', 'id': 'reservation'}),
        }
        error_messages = {
            'BName': {'required': '书名是必填的'},  # 设置错误提示信息
            'Author': {'required': '作者名称未填写'},
            'Publisher': {'required': '出版社是必填的'},
            'Price': {'required': '价格是必填的'},
            'NumInLib': {'required': '库存数是必填的'},
            'Category': {'required': '分类是必填的'},
            'PubTime': {'required': '出版日期是必填的'},
        }


class ClassMdfForm(forms.Form):
    Class = forms.CharField(label="电话号码", max_length=10,
                            required=False,
                            disabled=True,
                            widget=widgets.TextInput(
                                attrs={'class': 'form-control'})
                            )
    Limited = forms.IntegerField(label="邮箱", required=True,
                                 widget=widgets.NumberInput(attrs={"class": "form-control"}),
                                 error_messages={
                                     'required': '借阅上限不能为空'
                                 })
    Days = forms.IntegerField(label="邮箱", required=True,
                              widget=widgets.NumberInput(attrs={"class": "form-control"}),
                              error_messages={
                                  'required': '借阅天数不能为空'
                              })


class FineMdfForm(forms.Form):
    LimitDay = forms.IntegerField(label="邮箱", required=True,
                                  widget=widgets.NumberInput(attrs={"class": "form-control"}),
                                  error_messages={
                                      'required': '上限天数不能为空'
                                  })
    FineMoney = forms.IntegerField(label="邮箱", required=True,
                                   widget=widgets.NumberInput(attrs={"class": "form-control"}),
                                   error_messages={
                                       'required': '罚金不能为空'
                                   })

    def clean(self):
        changed_datas = self.changed_data
        if "LimitDay" in changed_datas:
            LimitDay = self.cleaned_data.get("LimitDay")
            if Fine.objects.filter(LimitDay=LimitDay).exists():
                raise forms.ValidationError({"LimitDay": '该上限天数规则已存在'})

        return self.cleaned_data
