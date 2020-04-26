from django.shortcuts import render
from django.http import HttpResponse, Http404
from BuctLib.models import *

AccountID = ""
AccountType = False
LoginUser = ""
UserAccount = ""


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


def readerindex(request):
    pass
