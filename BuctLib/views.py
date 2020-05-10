from django.shortcuts import render
from django.http import HttpResponse, Http404
from BuctLib.models import *
from BuctLib.src.formCheck import *
from django.db.models import Q
import os
from .forms import *

AccountID = None
AccountType = False
LoginUser = None  # 登陆的账号
UserAccount = None  # 登陆的账户


def hello(request):
    content = {
        LoginUser: LoginUser,
        UserAccount: UserAccount,
    }
    return render(request, "model/base.html", content)


def loginpage(request):
    """
    :param request: none
    :return: 登录界面
    """
    global LoginUser
    if LoginUser:
        if not AccountType:
            return readerindex(request)
        else:
            return render(request, "testmodel/manager.html", {"LoginUser": LoginUser, "UserAccount": UserAccount})

    content = {
        "isPwdW": False,
        "isNoAct": False,
    }
    return render(request, "login.html", content)


def loginout(request):
    global AccountType, AccountID, LoginUser, UserAccount
    AccountID = None
    AccountType = False
    LoginUser = None  # 登陆的账号
    UserAccount = None  # 登陆的账户
    return loginpage(request)


def logincheck(request):
    """
    :param request: post的密码 账号
    :return: 报错信息 或者主页
    """

    global AccountID, AccountType, LoginUser, UserAccount
    account = request.POST.get("AccountID")
    pswd = request.POST.get("Password")
    search_result = User.objects.filter(Q(AccountID=account) | Q(Email=account) | Q(Tel=account))
    if len(search_result) == 1:
        # 如果有这个账户
        if pswd == search_result[0].Password:
            # 密码正确

            if search_result[0].Type == "2":
                # 查读者表
                AccountID = search_result[0].AccountID
                AccountType = False
                UserAccount = search_result[0]
                try:
                    LoginUser = Reader.objects.get(AccountID=AccountID)
                except:
                    raise Http404
                return readerindex(request)
            elif search_result[0].Type == "1":
                # 查管理员表
                AccountID = search_result[0].AccountID
                AccountType = True
                UserAccount = search_result[0]
                try:
                    LoginUser = Manager.objects.get(AccountID=AccountID)
                except:
                    return page404(request)

                return render(request, "testmodel/manager.html", {"LoginUser": LoginUser, "UserAccount": UserAccount})
        else:
            # 密码错误
            content = {
                "isPwdW": True,
                "isNoAct": False,
                "pwdWrong": "密码错误",
                "pwd": pswd,
                "Account": account
            }
            return render(request, "login.html", content)
        pass
    else:
        # 没有这个账号
        content = {
            "noAccount": "账户不存在",
            "isNoAct": True,
            "isPwdW": False,
            "pwd": pswd,
            "Account": account
        }
        return render(request, "login.html", content)
    return HttpResponse("404")


def register(request):
    # 返回用户注册的页面
    content = {
        'isPwdERR': False,
        'isActERR': False,
        'isIdERR': False,
        'isEmailERR': False,
        'isPhoneERR': False,
        "checkedM": True,
        "checkedR": False,
    }
    return render(request, "register.html", content)


def registerCheck(request):
    # 注册检查
    account = request.POST.get("AccountID")
    pwd = request.POST.get("Password")
    ID = request.POST.get("ID")
    phone = request.POST.get("Phone")
    email = request.POST.get("email")
    Type = request.POST.get("type")

    # 记录返回值
    content = {
        'Account': account,
        'pwd': pwd,
        'ID': ID,
        'email': email,
        'phone': phone,
        'isPwdERR': False,
        'isActERR': False,
        'isIdERR': False,
        'isEmailERR': False,
        'isPhoneERR': False,
        "checkedM": True,
        "checkedR": False,
        'PwdERR': check_pwd(pwd),
        'ActERR': check_user_name(account),
        'IdERR': check_id(ID),
        'EmailERR': check_email(email),  # Django会自动检查邮箱
        'PhoneERR': check_phone(phone),
    }
    # 记录选中信息
    if Type == '1':
        content["checkedM"] = True
    elif Type == '2':
        content["checkedR"] = True
        content["checkedM"] = False
    # 检查合法性
    islegal = True
    ERR: str
    for ERR in ("PwdERR", "ActERR", "IdERR", "PhoneERR", "EmailERR"):
        if content[ERR] != "":
            islegal = False
            content[("is " + ERR)] = True

    if not islegal:
        return render(request, "register.html", content)

    search = User.objects.filter(Q(AccountID=account) | Q(Tel=phone) | Q(Email=email))

    if len(search) > 0:
        for item in search:
            if phone == item.Tel:
                content["isPhoneERR"] = True
                content["PhoneERR"] = "手机号已被注册"
            if email == item.Email:
                content["isEmailERR"] = True
                content["EmailERR"] = "邮箱已被注册"
            if account == item.AccountID:
                content["isActERR"] = True
                content["ActERR"] = ("账号已经存在请再试,可以尝试%s" % (account + "_123"))
        return render(request, "register.html", content)
    user = None
    reader = None
    manager = None
    if Type == '2':
        search = Reader.objects.filter(ReaderID=ID)
        if len(search) > 0:
            content["isIdERR"] = True
            content["IdERR"] = "学号已被注册"
            return render(request, "register.html", content)
        user = User.objects.create(AccountID=account, Password=pwd, Type=Type, Tel=phone, Email=email)
        reader = Reader.objects.create(ReaderID=ID, AccountID=user)
        reader.save()
        user.save()
    else:
        search = Manager.objects.filter(ManagerID=ID)
        if len(search) > 0:
            content["isIdERR"] = True
            content["IdERR"] = "工号已被注册"
            return render(request, "register.html", content)
        user = User.objects.create(AccountID=account, Password=pwd, Type=Type, Tel=phone, Email=email)
        manager = Manager.objects.create(ManagerID=ID, AccountID=user)
        manager.save()
        user.save()
    return render(request, "pagejump.html")


def readerindex(request):
    global AccountID, LoginUser, UserAccount

    if AccountID is None or LoginUser is None or UserAccount is None:
        return render(request, "page404.html")

    return render(request, "index.html", {"LoginUser": LoginUser, "UserAccount": UserAccount, })


def page404(request):
    return render(request, "page404.html")


def jump(request):
    return render(request, "pagejump.html")


def pwdmdf(request):
    if AccountID is None or LoginUser is None or UserAccount is None:
        return render(request, "page404.html")
    return render(request, "student/information/pwd-mdf.html",
                  {"mdfpwdState": "active", "InfState": "active", "OpenInf": "menu-open", "LoginUser": LoginUser,
                   "UserAccount": UserAccount})


def checkpwd(request):
    if AccountID is None or LoginUser is None or UserAccount is None:
        return render(request, "page404.html")
    content = {
        LoginUser: LoginUser, UserAccount: UserAccount,
        "mdfpwdState": "active", "InfState": "active", "OpenInf": "menu-open",
    }
    oldpwd = request.POST.get("old_pwd")
    newpwd = request.POST.get("new_pwd")
    renewpwd = request.POST.get("renew_pwd")
    if oldpwd != UserAccount.Password:
        content["oldpwd"], content["newpwd"], content["renewpwd"] = oldpwd, newpwd, renewpwd
        content["pwderr"] = "原密码错误"
        return render(request, "student/information/pwd-mdf.html", content)
    else:
        err = check_pwd(newpwd)
        if err != "":
            content["oldpwd"], content["newpwd"], content["renewpwd"] = oldpwd, newpwd, renewpwd
            content["newpwderr"] = err
            return render(request, "student/information/pwd-mdf.html", content)
        elif newpwd == oldpwd:
            content["oldpwd"], content["newpwd"], content["renewpwd"] = oldpwd, newpwd, renewpwd
            content["newpwderr"] = "与原密码相同"
            return render(request, "student/information/pwd-mdf.html", content)
        elif renewpwd != newpwd:
            content["oldpwd"], content["newpwd"], content["renewpwd"] = oldpwd, newpwd, renewpwd
            content["renewpwderr"] = "密码不一致"
            return render(request, "student/information/pwd-mdf.html", content)
    UserAccount.Password = newpwd
    UserAccount.save()
    content["work"] = "work"
    return render(request, "student/information/pwd-mdf.html", content)


def infmdf(request):
    global AccountID, LoginUser, UserAccount
    # LoginUser: Reader
    # UserAccount: User
    if AccountID is None or LoginUser is None or UserAccount is None:
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "mdfInfState": "active", "InfState": "active"
    }
    initial_form = {"AccountID": AccountID, "Email": UserAccount.Email, "Tel": UserAccount.Tel,
                                    "ReaderID": LoginUser.ReaderID,
                                    "Gender": LoginUser.Gender,
                                    "Name": LoginUser.Name,
                                    "School": LoginUser.School,
                                    "Class": LoginUser.Class,
                                    "Type": LoginUser.Type}
    if request.method == "POST":
        form = ReadInfForm(request.POST, initial=initial_form)
        if form.is_valid():
            content["work"] = "work"  # 数据合法
            UserAccount.Email = form.cleaned_data["Email"]
            UserAccount.Tel = form.cleaned_data["Tel"]
            LoginUser.Gender = form.cleaned_data["Gender"]
            LoginUser.Name = form.cleaned_data["Name"]
            LoginUser.School = form.cleaned_data["School"]
            LoginUser.Type = form.cleaned_data["Type"]
            LoginUser.save()
            UserAccount.save()
            content["form"] = ReadInfForm(
                initial={"AccountID": AccountID, "Email": UserAccount.Email, "Tel": UserAccount.Tel,
                         "ReaderID": LoginUser.ReaderID,
                         "Gender": LoginUser.Gender,
                         "Name": LoginUser.Name,
                         "School": LoginUser.School,
                         "Class": LoginUser.Class,
                         "Type": LoginUser.Type
                         })
        else:
            content["form"] = form
    else:
        form = ReadInfForm(initial=initial_form)
        content["form"] = form
    return render(request, "student/information/information-mdf.html", content)


def apllyclass(request):
    global AccountID, LoginUser, UserAccount
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "InfState": "active", "applyState": "active"
    }
    initialForm = {
        "ReaderID": LoginUser.ReaderID, "Class": LoginUser.Class
    }
    content["form"] = ApplyChangeClass(initial=initialForm)
    return render(request, "student/information/applyClass.html", content)
