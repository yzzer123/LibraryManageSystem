from django.shortcuts import render
from django.http import HttpResponse, Http404
from BuctLib.models import *
from BuctLib.src.formCheck import *
from django.db.models import Q

AccountID = None
AccountType = False
LoginUser = None
UserAccount = None


def hello(request):
    return HttpResponse("<h1>Hello BUCT Library</h1>")


def loginpage(request):
    """
    :param request: none
    :return: 登录界面
    """
    content = {
        "isPwdW": False,
        "isNoAct": False,
    }
    return render(request, "login.html", content)


def logincheck(request):
    """
    :param request: post的密码 账号
    :return: 报错信息 或者主页
    """
    global AccountID, AccountType, LoginUser, UserAccount
    account = request.POST.get("AccountID")
    pswd = request.POST.get("Password")
    search_result = User.objects.filter(AccountID=account)
    if len(search_result) == 1:
        # 如果有这个账户
        if pswd == search_result[0].Password:
            # 密码正确
            print(search_result[0].Type)
            if search_result[0].Type == "2":
                # 查读者表
                AccountID = account
                AccountType = False
                UserAccount = search_result[0]
                try:
                    LoginUser = Reader.objects.get(AccountID=AccountID)
                except:
                    raise Http404
                return render(request, "testmodel/reader.html", {"LoginUser": LoginUser, "UserAccount": UserAccount})
            elif search_result[0].Type == "1":
                # 查管理员表
                AccountID = account
                AccountType = True
                UserAccount = search_result[0]
                try:
                    LoginUser = Manager.objects.get(AccountID=AccountID)
                except:
                    raise Http404
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
        'checkedM': "checked"
    }
    return render(request, "register.html", content)

def registerCheck(request):
    # 注册检查
    account = request.POST["AccountID"]
    pwd = request.POST["Password"]
    ID = request.POST["ID"]
    phone = request.POST["Phone"]
    email = request.POST["email"]
    Type = request.POST["type"]

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
        'PwdERR': check_pwd(pwd),
        'ActERR': check_user_name(account),
        'IdERR': check_id(ID),
        'EmailERR': "",  # Django会自动检查邮箱
        'PhoneERR': check_phone(phone),
    }
    # 记录选中信息
    if Type == 1:
        content["checkedM"] = "checked"
    else:
        content["checkedR"] = "checked"
    # 检查合法性
    islegal = True
    if content["PwdERR"] != "":
        islegal = False
        content["isPwdERR"] = True
    if content["ActERR"] != "":
        islegal = False
        content["isActERR"] = True
    if content["IdERR"] != "":
        islegal = False
        content["isIdERR"] = True
    if content["PhoneERR"] != "":
        islegal = False
        content["isPhoneERR"] = True
    if not islegal:
        return render(request, "register.html", content)

    search = User.objects.filter(AccountID=account)
    if len(search) > 0:
        content["isActERR"] = True
        content["ActERR"] = ("账号已经存在请再试,可以尝试%s" % (account+"_123"))
    del search
    user = None
    reader = None
    manager = None
    if Type == '2':
        stusearch = Reader.objects.filter(Q(Phone=phone)|Q(StudentID=ID)|Q(Mail=email))
        if len(stusearch) > 0:
            for item in stusearch:
                if phone == item.Phone:
                    content["isPhoneERR"] = True
                    content["PhoneERR"] = "手机号已被注册"
                if ID == item.StudentID:
                    content["isIdERR"] = True
                    content["IdERR"] = "学号已被注册"
                if email == item.Mail:
                    content["isEmailERR"] = True
                    content["EmailERR"] = "邮箱已被注册"
            return render(request, "register.html", content)
        user = User.objects.create(AccountID=account, Password=pwd, Type=Type)
        reader = Reader.objects.create(StudentID=ID, AccountID=user, Phone=phone, Mail=email)

    else:
        manasearch = Manager.objects.filter(Q(Phone=phone) | Q(ManagerID=ID) | Q(Mail=email))
        if len(manasearch) > 0:
            for item in manasearch:
                if phone == item.Phone:
                    content["isPhoneERR"] = True
                    content["PhoneERR"] = "手机号已被注册"
                if ID == item.ManagerID:
                    content["isIdERR"] = True
                    content["IdERR"] = "工号已被注册"
                if email == item.Mail:
                    content["isEmailERR"] = True
                    content["EmailERR"] = "邮箱已被注册"
            return render(request, "register.html", content)
        user = User.objects.create(AccountID=account, Password=pwd, Type=Type)
        manager = Manager.objects.create(ManagerID=ID, AccountID=user, Phone=phone, Mail=email)
    if manager:
        manager.save()
        user.save()
    if reader:
        reader.save()
        user.save()
    return render(request, "registerSuccess.html")


def readerindex(request):
    pass


def registerok(request):
    return render(request, 'registerSuccess.html')
