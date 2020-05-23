# from datetime import datetime
from datetime import datetime, timedelta
from random import seed, random
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from dateutil.relativedelta import relativedelta
from BuctLib.models import *
from BuctLib.src.formCheck import *
from django.db.models import Q, Count
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
    if LoginUser:
        if not AccountType:
            return render(request, "model/base.html", content)
        else:
            return render(request, 'model/adminbase.html', content)

    return render(request, 'page404.html')


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
            return adminindex(request)
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

                return adminindex(request)
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
    Key = request.POST.get("Key")
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
        "KeyERR": "",
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
        if Key != "reader_user":
            content["KeyERR"] = "注册码不正确"
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
        if Key != "admin_manager":
            content["KeyERR"] = "注册码不正确"
            return render(request, "register.html", content)
        user = User.objects.create(AccountID=account, Password=pwd, Type=Type, Tel=phone, Email=email)
        manager = Manager.objects.create(ManagerID=ID, AccountID=user)
        manager.save()
        user.save()
    return render(request, "pagejump.html")


def adminindex(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    books = Book.objects.all().order_by('-ReadTimes')[:5]
    notices = Notice.objects.all().order_by('-NTime')[:5]
    return render(request, "lib_admin/adminindex.html",
                  {"LoginUser": LoginUser, "UserAccount": UserAccount, "books": books, "notices": notices})


def readerindex(request):
    global AccountID, LoginUser, UserAccount

    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    books = Book.objects.all().order_by('-ReadTimes')[:5]
    notices = Notice.objects.all().order_by('-NTime')[:5]
    return render(request, "student/studentindex.html",
                  {"LoginUser": LoginUser, "UserAccount": UserAccount, "books": books, "notices": notices})


def page404(request):
    return render(request, "page404.html")


def jump(request):
    return render(request, "pagejump.html")


def pwdmdf(request):
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    return render(request, "student/information/pwd-mdf.html",
                  {"mdfpwdState": "active", "InfState": "active", "OpenInf": "menu-open", "LoginUser": LoginUser,
                   "UserAccount": UserAccount})


def admin_pwdmdf(request):
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    return render(request, "lib_admin/info/pwd.html",
                  {"mdfpwdState": "active", "InfState": "active", "OpenInf": "menu-open", "LoginUser": LoginUser,
                   "UserAccount": UserAccount})


def checkpwd(request):
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
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


def admin_checkpwd(request):
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
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
        return render(request, "lib_admin/info/pwd.html", content)
    else:
        err = check_pwd(newpwd)
        if err != "":
            content["oldpwd"], content["newpwd"], content["renewpwd"] = oldpwd, newpwd, renewpwd
            content["newpwderr"] = err
            return render(request, "lib_admin/info/pwd.html", content)

        elif newpwd == oldpwd:
            content["oldpwd"], content["newpwd"], content["renewpwd"] = oldpwd, newpwd, renewpwd
            content["newpwderr"] = "与原密码相同"
            return render(request, "lib_admin/info/pwd.html", content)

        elif renewpwd != newpwd:
            content["oldpwd"], content["newpwd"], content["renewpwd"] = oldpwd, newpwd, renewpwd
            content["renewpwderr"] = "密码不一致"
            return render(request, "lib_admin/info/pwd.html", content)

    UserAccount.Password = newpwd
    UserAccount.save()
    content["work"] = "work"
    return render(request, "lib_admin/info/pwd.html", content)


def infmdf(request):
    global AccountID, LoginUser, UserAccount
    # LoginUser: Reader
    # UserAccount: User
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
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


def admin_infmdf(request):
    global AccountID, LoginUser, UserAccount
    # LoginUser: Reader
    # UserAccount: User
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "mdfInfState": "active", "InfState": "active"
    }
    initial_form = {"AccountID": AccountID, "Email": UserAccount.Email, "Tel": UserAccount.Tel,
                    "AdminID": LoginUser.ManagerID,
                    "Gender": LoginUser.Gender,
                    "Name": LoginUser.Name,
                    }
    if request.method == "POST":
        form = AdminInfForm(request.POST, initial=initial_form)
        if form.is_valid():
            content["work"] = "work"  # 数据合法
            UserAccount.Email = form.cleaned_data["Email"]
            UserAccount.Tel = form.cleaned_data["Tel"]
            LoginUser.Gender = form.cleaned_data["Gender"]
            LoginUser.Name = form.cleaned_data["Name"]
            LoginUser.save()
            UserAccount.save()
            content["form"] = AdminInfForm(
                initial={"AccountID": AccountID, "Email": UserAccount.Email, "Tel": UserAccount.Tel,
                         "AdminID": LoginUser.ManagerID,
                         "Gender": LoginUser.Gender,
                         "Name": LoginUser.Name,
                         })
        else:
            content["form"] = form
    else:
        form = AdminInfForm(initial=initial_form)
        content["form"] = form
    return render(request, "lib_admin/info/information-mdf.html", content)


def apllyclass(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "InfState": "active", "applyState": "active"
    }
    initialForm = {
        "ReaderID": LoginUser.ReaderID, "Class": LoginUser.Class.Class, "Message": ""
    }
    if request.method == "POST":
        form = ApplyChangeClass(request.POST, initial=initialForm)
        if form.is_valid():
            content["work"] = "work"
            for item in ApplyClass.objects.filter(ReaderID=LoginUser.ReaderID):
                item.delete()
            apply_text = form.cleaned_data["Message"]
            apply_class = form.cleaned_data["Class"]
            apply = ApplyClass.objects.create(ReaderID=LoginUser, Class=ReaderClass.objects.get(Class=apply_class),
                                              Message=apply_text)
            apply.save()
            content["form"] = ApplyChangeClass(initial=initialForm)
            m = Message.objects.create(Title="级别变更申请", ReaderID=LoginUser,
                                       Content="您申请将读者级别变更为%s级的请求已经提交，管理员会尽量在三个工作日内处理申请" % apply_class)
            m.save()
        else:
            content["form"] = form
    else:
        content["form"] = ApplyChangeClass(initial=initialForm)
    if ApplyClass.objects.filter(ReaderID=LoginUser.ReaderID).exists():
        content["resetApply"] = True
    return render(request, "student/information/applyClass.html", content)


def resetapply(request):
    global LoginUser
    if request.method == "GET":
        for item in ApplyClass.objects.filter(ReaderID=LoginUser.ReaderID):
            item.delete()
        m = Message.objects.create(Title="撤销级别变更申请", ReaderID=LoginUser, Content="您的读者级别变更申请已被撤销")
        m.save()
        return HttpResponse("已撤销全部申请")
    else:
        return None


def getmessage(request):
    global LoginUser
    # 获取消息
    if request.method == "GET" and request.GET.get("way") == "get":
        res = Message.objects.filter(ReaderID=LoginUser.ReaderID, Status="未读").order_by("-MTime").values()
        for item in res:
            item["MTime"] = item["MTime"].strftime('%Y-%m-%d %H:%M:%S')
        # print(datetime.datetime.now())
        return JsonResponse(list(res), safe=False)
    # 标志已读
    elif request.method == "GET" and request.GET.get("way") == "reset":
        res = Message.objects.filter(ReaderID=LoginUser.ReaderID, Status="未读")
        for item in res:
            item.delete()
        return HttpResponse("ok")
    else:
        return None


def getborrow(request):
    global LoginUser
    # 请求借书的数据
    if request.method == "GET" and request.GET.get("way") == "get":
        nullallowed_books = []
        allowed_books = []
        # 查阅未审核记录
        nullallowed_borrow = Borrow.objects.filter(
            Q(ReaderID=LoginUser.ReaderID) & Q(isDelete=False) & Q(isAllowed__isnull=True))
        for item in nullallowed_borrow:
            newbook = {"id": item.id, "BookID": item.BookID.BookID, "BName": item.BookID.BName,
                       "Author": item.BookID.Author, "Publisher": item.BookID.Publisher}
            nullallowed_books.append(newbook)
        # 查阅已借记录
        allowed_borrow = Borrow.objects.filter(
            Q(ReaderID=LoginUser.ReaderID) & Q(isReturned=False) & Q(isDelete=False) & Q(isAllowed=True))
        for item in allowed_borrow:
            newbook = {"id": item.id, "BookID": item.BookID.BookID, "BName": item.BookID.BName,
                       "Author": item.BookID.Author, "Publisher": item.BookID.Publisher}
            allowed_books.append(newbook)
        return JsonResponse({"nullbooks": list(nullallowed_books), "allowbooks": list(allowed_books)}, safe=False)
    # 删除未审核的借书记录
    elif request.method == "GET" and request.GET.get("way") == "reset":
        res = Borrow.objects.get(id=request.GET.get("id"))
        res.isDelete = True
        res.save()
        newMes = Message.objects.create(Title="删除撤销借阅",
                                        Content="您借阅《%s》的记录已经被撤销删除" % res.BookID.BName, ReaderID=LoginUser)
        newMes.save()
        return HttpResponse("ok")
    return None


def noticedetail(request, id):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "notice": Notice.objects.get(id=id)
    }
    content["notice"].ReadTimes += 1
    content["notice"].save()
    return render(request, "student/library/notice_detail.html", content)


def admin_noticedetail(request, id):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "notice": Notice.objects.get(id=id)
    }
    content["notice"].ReadTimes += 1
    content["notice"].save()
    return render(request, "lib_admin/library/notice_detail.html", content)


def allnotice(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
    }
    notices = Notice.objects.defer("Content")
    res = []
    for year in notices.values('NTime__year').distinct().order_by('-NTime__year'):
        for month in notices.filter(NTime__year=year["NTime__year"]).values("NTime__month").distinct().order_by(
                '-NTime__month'):
            monthNotice = {'YM': '%d-%d' % (year["NTime__year"], month["NTime__month"]),
                           "notices": notices.filter(
                               Q(NTime__year=year["NTime__year"]) & Q(NTime__month=month["NTime__month"])).order_by(
                               '-NTime')}
            res.append(monthNotice)
    content["notices"] = res
    return render(request, "student/library/all_notice.html", content)


def admin_allnotice(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
    }
    notices = Notice.objects.defer("Content")
    res = []
    for year in notices.values('NTime__year').distinct().order_by('-NTime__year'):
        for month in notices.filter(NTime__year=year["NTime__year"]).values("NTime__month").distinct().order_by(
                '-NTime__month'):
            monthNotice = {'YM': '%d-%d' % (year["NTime__year"], month["NTime__month"]),
                           "notices": notices.filter(
                               Q(NTime__year=year["NTime__year"]) & Q(NTime__month=month["NTime__month"])).order_by(
                               '-NTime')}
            res.append(monthNotice)
    content["notices"] = res
    return render(request, "lib_admin/library/all_notice.html", content)


def searchbooks(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenLib": "menu-open", "LibState": "active", "SearchState": "active"
    }
    if request.method == "POST":
        search_type = request.POST.get("type")
        keyword = request.POST.get("keyword")
        keyword: str
        content["keyword"] = keyword
        content["type"] = search_type
        if search_type == "全部":
            if keyword.isdigit():
                content["books"] = Book.objects.filter(Q(BookID=int(keyword)) | Q(BName__icontains=keyword)
                                                       | Q(Publisher__icontains=keyword)
                                                       | Q(Author__icontains=keyword) | Q(Category=keyword))
            else:
                content["books"] = Book.objects.filter(Q(BName__icontains=keyword)
                                                       | Q(Publisher__icontains=keyword)
                                                       | Q(Author__icontains=keyword) | Q(Category__icontains=keyword))
        elif search_type == "书号":
            content["books"] = Book.objects.filter(BookID=keyword)
        elif search_type == "书名":
            content["books"] = Book.objects.filter(BName__icontains=keyword)
        elif search_type == "出版社":
            content["books"] = Book.objects.filter(Publisher__icontains=keyword)
        elif search_type == "作者":
            content["books"] = Book.objects.filter(Author__icontains=keyword)
        elif search_type == "分类":
            content["books"] = Book.objects.filter(Category__icontains=keyword)
    else:
        content["keyword"] = ""
        content["type"] = "全部"
        content["books"] = Book.objects.all()
    return render(request, "student/library/searchbooks.html", content)


def admin_searchbooks(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenLib": "menu-open", "LibState": "active", "SearchState": "active"
    }
    if request.method == "POST":
        search_type = request.POST.get("type")
        keyword = request.POST.get("keyword")
        keyword: str
        content["keyword"] = keyword
        content["type"] = search_type
        if search_type == "全部":
            if keyword.isdigit():
                content["books"] = Book.objects.filter(Q(BookID=int(keyword)) | Q(BName__icontains=keyword)
                                                       | Q(Publisher__icontains=keyword)
                                                       | Q(Author__icontains=keyword) | Q(Category=keyword))
            else:
                content["books"] = Book.objects.filter(Q(BName__icontains=keyword)
                                                       | Q(Publisher__icontains=keyword)
                                                       | Q(Author__icontains=keyword) | Q(Category__icontains=keyword))
        elif search_type == "书号":
            content["books"] = Book.objects.filter(BookID=keyword)
        elif search_type == "书名":
            content["books"] = Book.objects.filter(BName__icontains=keyword)
        elif search_type == "出版社":
            content["books"] = Book.objects.filter(Publisher__icontains=keyword)
        elif search_type == "作者":
            content["books"] = Book.objects.filter(Author__icontains=keyword)
        elif search_type == "分类":
            content["books"] = Book.objects.filter(Category__icontains=keyword)
    else:
        content["keyword"] = ""
        content["type"] = "全部"
        content["books"] = Book.objects.all()
    return render(request, "lib_admin/library/searchbooks.html", content)


def borrow(request):
    global AccountID, LoginUser, UserAccount

    if request.method == "GET":
        if len(Borrow.objects.filter(
                ((Q(isAllowed__isnull=True) | Q(isAllowed=True)) & Q(isReturned=False) & Q(isDelete=False)) & (
                        Q(isDelete=False) & Q(ReaderID=LoginUser)))) >= LoginUser.Class.Limited:
            return HttpResponse("out")
        id = request.GET.get("id")
        book = Book.objects.get(BookID=id)
        if book.NumNow == 0:
            return HttpResponse("nobook")
        newBorrow = Borrow.objects.create(ReaderID=LoginUser, BookID=book)
        newBorrow.save()
        newMes = Message.objects.create(Title="借阅申请",
                                        Content="您申请借阅《%s》的请求已发出，管理员会尽快审核" % book.BName, ReaderID=LoginUser)
        newMes.save()
        return HttpResponse("yes")
    return HttpResponse("no")


def bookdetail(request, id):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    book = Book.objects.get(BookID=id)
    readers = list(map(lambda item: item["ReaderID"], list(Borrow.objects.filter(BookID=id).values("ReaderID"))))
    author_books = Book.objects.filter(Q(Author=book.Author) & (~Q(BookID=id)))
    reader_books = Borrow.objects.filter(Q(ReaderID__in=readers) & (~Q(BookID=id))).annotate(
        count=Count('BookID')).order_by("-count")[:5]
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenLib": "menu-open", "LibState": "active", "SearchState": "active",
        "author_books": author_books, "reader_books": reader_books, "book": book
    }
    return render(request, "student/bookdetail.html", content)


def admin_bookdetail(request, id):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    book = Book.objects.get(BookID=id)
    readers = list(map(lambda item: item["ReaderID"], list(Borrow.objects.filter(BookID=id).values("ReaderID"))))
    author_books = Book.objects.filter(Q(Author=book.Author) & (~Q(BookID=id)))
    reader_books = Borrow.objects.filter(Q(ReaderID__in=readers) & (~Q(BookID=id))).annotate(
        count=Count('BookID')).order_by("-count")[:5]
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenLib": "menu-open", "LibState": "active", "SearchState": "active",
        "author_books": author_books, "reader_books": reader_books, "book": book
    }
    return render(request, "lib_admin/library/bookdetail.html", content)


def commend(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    seed(str(datetime.now().date()))
    commend_rd = int(random() * 1000)
    # LoginUser: Reader
    # 选出读者最喜欢的书类别
    readed_books = Borrow.objects.filter(ReaderID=LoginUser.ReaderID)
    books_list = list(map(lambda item: item["BookID"], readed_books.values("BookID")))
    try:
        reader_like_cat = \
            readed_books.values('BookID__Category').annotate(count=Count("BookID__Category")).order_by("-count")[0]
        books = Book.objects.filter(
            (~Q(BookID__in=books_list)) & Q(Category=reader_like_cat["BookID__Category"])).order_by('-ReadTimes')[:10]
        book = books[commend_rd % 10]
    except:
        books = Book.objects.filter(
            (~Q(BookID__in=books_list))).order_by('-ReadTimes')[:10]
        book = books[commend_rd % 10]
    readers = list(map(lambda item: item["ReaderID"], list(Borrow.objects.filter(id=book.BookID).values("ReaderID"))))
    author_books = Book.objects.filter(Q(Author=book.Author) & (~Q(BookID=book.BookID)))
    reader_books = Borrow.objects.filter(Q(ReaderID__in=readers) & (~Q(BookID=book.BookID))).annotate(
        count=Count('BookID')).order_by("-count")[:5]
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenLib": "menu-open", "LibState": "active", "RecState": "active",
        "author_books": author_books, "reader_books": reader_books, "book": book
    }
    return render(request, "student/bookdetail.html", content)


def datavisual(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    borrows = Borrow.objects.filter(Q(isAllowed=True) | Q(isAllowed__isnull=True))
    now = datetime.now()
    week_data = []
    month_data = []
    cate_data = []
    school_data = []
    for i in range(7):
        day = now - timedelta(days=i)
        week_data.append({"data": borrows.filter(BorrowTime=day).count(),
                          "day": day.strftime("%m-%d")})
        if i < 6:
            month = now - relativedelta(months=i)
            month_data.append(
                {"data": borrows.filter(Q(BorrowTime__month=month.month) & Q(BorrowTime__year=month.year)).count(),
                 "month": str(month.strftime("%Y-%m"))})
    for cate in CATEGORY_CHOICE:
        cate_data.append({
            "cate": cate[1],
            "data": borrows.filter(BookID__Category=cate[0]).count()
        })
    for school in SCHOOLS:
        school_data.append({
            "school": school[1],
            "data": borrows.filter(ReaderID__School=school[0]).count()
        })
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenLib": "menu-open", "LibState": "active", "dataState": "active",
        "week_data": week_data, "month_data": month_data, "cate_data": cate_data, "school_data": school_data
    }

    return render(request, "student/library/datavisual.html", content)


def admin_datavisual(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    borrows = Borrow.objects.filter(Q(isAllowed=True) | Q(isAllowed__isnull=True))
    now = datetime.now()
    week_data = []
    month_data = []
    cate_data = []
    school_data = []
    for i in range(7):
        day = now - timedelta(days=i)
        week_data.append({"data": borrows.filter(BorrowTime=day).count(),
                          "day": day.strftime("%m-%d")})
        if i < 6:
            month = now - relativedelta(months=i)
            month_data.append(
                {"data": borrows.filter(Q(BorrowTime__month=month.month) & Q(BorrowTime__year=month.year)).count(),
                 "month": str(month.strftime("%Y-%m"))})
    for cate in CATEGORY_CHOICE:
        cate_data.append({
            "cate": cate[1],
            "data": borrows.filter(BookID__Category=cate[0]).count()
        })
    for school in SCHOOLS:
        school_data.append({
            "school": school[1],
            "data": borrows.filter(ReaderID__School=school[0]).count()
        })
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenLib": "menu-open", "LibState": "active", "dataState": "active",
        "week_data": week_data, "month_data": month_data, "cate_data": cate_data, "school_data": school_data
    }

    return render(request, "lib_admin/library/datavisual.html", content)


def checkingbooks(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    checkings = Borrow.objects.filter(Q(ReaderID=LoginUser) & Q(isAllowed__isnull=True) & Q(isDelete=False)).order_by(
        '-BorrowTime')
    rejects = Borrow.objects.filter(Q(ReaderID=LoginUser) & Q(isAllowed=False) & Q(isDelete=False)).order_by(
        '-BorrowTime')
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenBr": "menu-open", "BrState": "active", "CheckState": "active",
        'checkings': checkings, "rejects": rejects
    }
    return render(request, 'student/borrow/checking.html', content)


def getmesnum(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return HttpResponse("no")
    if request.method == 'GET':
        num = Message.objects.filter(ReaderID=LoginUser).count()
        return HttpResponse(num)
    return HttpResponse("no")


def showbred(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    bred_books = Borrow.objects.filter(
        Q(ReaderID=LoginUser) & Q(isAllowed=True) & Q(isReturned=False) & Q(isDelete=False)).order_by(
        '-BorrowTime')
    outdate = bred_books.filter(ReturnDay__lt=datetime.now().date())

    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenBr": "menu-open", "BrState": "active", "NotRState": "active",
        "bred_books": bred_books.filter(ReturnDay__gte=datetime.now().date()), "nowdate": datetime.now(),
        "outdate_books": outdate, "outdate_num": outdate.count()
    }

    return render(request, "student/borrow/notreturn.html", content)


def returnbook(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        raise Http404
    if request.method == "GET":
        ID = request.GET.get('id')
        br = Borrow.objects.get(id=ID)
        if br.ReturnDay < datetime.now().date():
            br.isLegal = False
            br.isReturned = True
            br.BookID.NumNow += 1
            br.RealreturnDay = datetime.now().date()
            br.BookID.save()
            br.save()
            m = Message.objects.create(Title="逾期归还图书",
                                       Content="您借阅的《%s》已经归还，鉴于您已逾期，违规记录已生成，请在违规记录栏下查看违规报告" % br.BookID.BName,
                                       ReaderID=LoginUser)
            m.save()
            return HttpResponse("ok")
        else:
            br.isReturned = True
            br.BookID.NumNow += 1
            br.RealreturnDay = datetime.now().date()
            br.BookID.save()
            br.save()
            m = Message.objects.create(Title="成功归还图书",
                                       Content="您借阅的《%s》已经归还，欢迎下次借阅" % br.BookID.BName,
                                       ReaderID=LoginUser)
            m.save()
            return HttpResponse("ok")
    return Http404


def delayreturn(request, id):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        raise Http404
    br = Borrow.objects.get(id=id)
    br.ReturnDay += timedelta(days=LoginUser.Class.Days)
    br.isReBorrowed = True
    br.save()
    m = Message.objects.create(Title="续借通知", ReaderID=LoginUser,
                               Content="您借阅《%s》的归还日期已被延长%d天, 请按期归还" % (br.BookID.BName, LoginUser.Class.Days))
    m.save()
    return HttpResponse("ok")


def showreturned(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    br = Borrow.objects.filter(Q(ReaderID=LoginUser) & Q(isDelete=False) & Q(isReturned=True))
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenBr": "menu-open", "BrState": "active", "RState": "active",
        'borrow_record': br,
    }
    return render(request, "student/borrow/returned.html", content)


def showillegal(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        return render(request, "page404.html")
    now = datetime.now().date()
    br = Borrow.objects.filter(Q(ReaderID=LoginUser) & Q(isAllowed=True) & (
            (Q(isDelete=False) & Q(ReturnDay__lt=now) & Q(isReturned=False)) | (Q(isLegal=False) & Q(isReturned=True))))
    fines = []
    for item in br:
        if not item.isReturned:
            days = (now - item.ReturnDay).days
        else:
            days = (item.RealreturnDay - item.ReturnDay).days
        fine = {
            "days": days,
            "fine_money": Fine.objects.filter(LimitDay__gt=days).order_by('LimitDay')[0].FineMoney
        }
        fines.append(fine)
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenBr": "menu-open", "BrState": "active", "IllegalState": "active",
        'illegal_record': zip(br, fines),
    }
    return render(request, "student/borrow/illegal.html", content)


def deletebr(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '1':
        raise Http404
    if request.method == "GET":
        br_id = request.GET.get('id')
        br = Borrow.objects.get(id=br_id)
        br.isDelete = True
        br.save()
        return HttpResponse("ok")
    return Http404


def admin_deletebr(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        raise Http404
    if request.method == "GET":
        br_id = request.GET.get('id')
        Borrow.objects.get(id=br_id).delete()
        return HttpResponse("ok")
    return HttpResponse("no")


def remind_reader(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        raise Http404
    if request.method == "GET":
        br_id = request.GET.get('id')
        br = Borrow.objects.get(id=br_id)
        m = Message()
        m.ReaderID = br.ReaderID
        m.Title = "逾期未归还提醒"
        m.Content = "您借阅的《%s》已经逾期，请您及时归还图书，以免罚金继续增长。" % br.BookID.BName
        m.save()
        return HttpResponse("ok")
    return HttpResponse("no")


def illegal_report(request, id):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '1':
        return render(request, "page404.html")

    report_br = Borrow.objects.get(id=id)
    now = datetime.now()
    if report_br.ReaderID != LoginUser:
        # 非当前读者的违规报告

        render(request, "page404.html")
    elif (not report_br.isLegal) and report_br.isAllowed == True \
            and report_br.isReturned == True:

        # 已归还， 但已经超期
        days = (report_br.RealreturnDay - report_br.ReturnDay).days
        fine = {
            "days": days,
            "fine_money": Fine.objects.filter(LimitDay__gt=days).order_by('LimitDay')[0].FineMoney
        }

        content = {
            "LoginUser": LoginUser, "UserAccount": UserAccount,
            "OpenBr": "menu-open", "BrState": "active", "IllegalState": "active",
            'report_br': report_br, "fine": fine, "nowDate": now.date()
        }

        return render(request, "student/borrow/report.html", content)
    elif report_br.isAllowed == True and report_br.ReturnDay < now.date() and report_br.isReturned == False:
        # 正在借阅 已经超期
        days = (now.date() - report_br.ReturnDay).days
        fine = {
            "days": days,
            "fine_money": Fine.objects.filter(LimitDay__gt=days).order_by('LimitDay')[0].FineMoney
        }

        content = {
            "LoginUser": LoginUser, "UserAccount": UserAccount,
            "OpenBr": "menu-open", "BrState": "active", "IllegalState": "active",
            'report_br': report_br, "fine": fine, "nowDate": now.date()
        }

        return render(request, "student/borrow/report.html", content)
    else:

        return render(request, "page404.html")
    # except:
    #     print('errr')
    #     return render(request, "page404.html")
    return render(request, "page404.html")


def admin_showillegal(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    now = datetime.now().date()
    br = Borrow.objects.filter(Q(isAllowed=True) & (
            (Q(isDelete=False) & Q(ReturnDay__lt=now) & Q(isReturned=False)) | (Q(isLegal=False) & Q(isReturned=True))))
    fines = []
    for item in br:
        if not item.isReturned:
            days = (now - item.ReturnDay).days
        else:
            days = (item.RealreturnDay - item.ReturnDay).days
        fine = {
            "days": days,
            "fine_money": Fine.objects.filter(LimitDay__gt=days).order_by('LimitDay')[0].FineMoney
        }
        fines.append(fine)
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenBr": "menu-open", "BrState": "active", "IllegalState": "active",
        'illegal_record': zip(br, fines), 'borrows': br
    }
    return render(request, "lib_admin/borrow/illegal.html", content)


def admin_illegal_report(request, id):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")

    report_br = Borrow.objects.get(id=id)
    now = datetime.now()
    if (not report_br.isLegal) and report_br.isAllowed == True \
            and report_br.isReturned == True:

        # 已归还， 但已经超期
        days = (report_br.RealreturnDay - report_br.ReturnDay).days
        fine = {
            "days": days,
            "fine_money": Fine.objects.filter(LimitDay__gt=days).order_by('LimitDay')[0].FineMoney
        }

        content = {
            "LoginUser": LoginUser, "UserAccount": UserAccount,
            "OpenBr": "menu-open", "BrState": "active", "IllegalState": "active",
            'report_br': report_br, "fine": fine, "nowDate": now.date()
        }

        return render(request, "lib_admin/borrow/report.html", content)
    elif report_br.isAllowed == True and report_br.ReturnDay < now.date() and report_br.isReturned == False:
        # 正在借阅 已经超期
        days = (now.date() - report_br.ReturnDay).days
        fine = {
            "days": days,
            "fine_money": Fine.objects.filter(LimitDay__gt=days).order_by('LimitDay')[0].FineMoney
        }

        content = {
            "LoginUser": LoginUser, "UserAccount": UserAccount,
            "OpenBr": "menu-open", "BrState": "active", "IllegalState": "active",
            'report_br': report_br, "fine": fine, "nowDate": now.date()
        }

        return render(request, "lib_admin/borrow/report.html", content)
    else:

        return render(request, "page404.html")
    # except:
    #     print('errr')
    #     return render(request, "page404.html")
    return render(request, "page404.html")


def sendMessage(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenMes": "menu-open", "MesState": "active", "MesSendState": "active",

    }
    if request.method == "POST":
        form = NewMessForm(request.POST)
        if form.is_valid():
            # 数据合法
            form.save()
            content["form"], content["work"] = NewMessForm(), "work"
        else:
            content["form"] = form
    else:
        content["form"] = NewMessForm()

    return render(request, "lib_admin/message/mes.html", content)


def sendNotice(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenMes": "menu-open", "MesState": "active", "noticeState": "active",

    }
    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            # 数据合法
            form.save()
            content["form"], content["work"] = NoticeForm(), "work"
        else:
            content["form"] = form
    else:
        content["form"] = NoticeForm()

    return render(request, "lib_admin/message/Notice.html", content)


def cancelNotice(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return HttpResponse("no")
    if request.method == 'GET':
        ID = request.GET.get('ID')
        Notice.objects.get(id=ID).delete()
        return HttpResponse("ok")
    return HttpResponse("no")


def add_user(request):
    global AccountID, LoginUser, UserAccount
    # LoginUser: Reader
    # UserAccount: User
    if AccountID is None or LoginUser is None or UserAccount is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "InfState": "active", "addReaderState": "active"
    }

    if request.method == "POST":

        form = AddReadInfForm(request.POST)
        if form.is_valid():
            content["work"] = "work"  # 数据合法
            new_account = User()
            new_reader = Reader()
            new_account.Email = form.cleaned_data["Email"]
            new_account.AccountID = form.cleaned_data["AccountID"]
            new_account.Tel = form.cleaned_data["Tel"]
            new_account.Password = form.cleaned_data["ReaderID"]
            new_account.Type = '2'
            new_account.save()
            new_reader.School = form.cleaned_data["School"]
            new_reader.Type = form.cleaned_data["Type"]
            new_reader.ReaderID = form.cleaned_data["ReaderID"]
            new_reader.AccountID_id = form.cleaned_data["AccountID"]
            new_reader.Class_id = form.cleaned_data["Class"]
            new_reader.save()
            content["form"] = AddReadInfForm()
        else:
            content["form"] = form
    else:
        form = AddReadInfForm()
        content["form"] = form
    return render(request, "lib_admin/info/add_user.html", content)


def add_class(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "InfState": "active", "addClassState": "active",
    }
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            # 数据合法
            form.save()
            content["form"], content["work"] = ClassForm(), "work"
        else:
            content["form"] = form
    else:
        content["form"] = ClassForm()
    return render(request, 'lib_admin/info/add_class.html', content)


def add_fine(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "InfState": "active", "addFineState": "active",
    }
    if request.method == "POST":
        form = FineForm(request.POST)
        print(request.POST)
        if form.is_valid():
            # 数据合法
            form.save()
            content["form"], content["work"] = FineForm(), "work"
        else:
            content["form"] = form
    else:
        content["form"] = FineForm()
    return render(request, 'lib_admin/info/add_fine.html', content)


def book_admin(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    if request.method == "GET":
        op = request.GET.get("op")
        BookID = request.GET.get("id")
        if op == "add":
            book = Book.objects.get(BookID=BookID)
            book.NumNow += 1
            book.NumInLib += 1
            book.save()
            NumNow = int(book.NumNow)
            NumInLib = int(book.NumInLib)
            return JsonResponse({"NumNow": NumNow, "NumInLib": NumInLib})
        elif op == "cut":
            book = Book.objects.get(BookID=BookID)
            book.NumNow -= 1
            book.NumInLib -= 1
            book.save()
            NumNow = int(book.NumNow)
            NumInLib = int(book.NumInLib)
            return JsonResponse({"NumNow": NumNow, "NumInLib": NumInLib})
        elif op == "delete":
            book = Book.objects.get(BookID=BookID)
            if book.NumNow == book.NumInLib:
                book.delete()
                return HttpResponse("ok")
            else:
                return HttpResponse("err")
    return HttpResponse("no")


def add_book(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenLib": "menu-open", "LibState": "active", "AddState": "active",
    }
    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            book = form.save(commit=False)
            book.NumNow = book.NumInLib
            book.save()
            content["work"] = "work"
            content["form"] = BookForm()
        else:

            content["form"] = form
    else:
        content["form"] = BookForm()
    return render(request, "lib_admin/library/add_book.html", content)


def check_borrow(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenBr": "menu-open", "BrState": "active", "CheckState": "active",
    }
    record = Borrow.objects.filter(Q(isAllowed__isnull=True) & Q(isDelete=False))
    borrows = [dict() for i in record]
    now = datetime.now().date()
    for item, br in zip(borrows, record):
        illegal = Borrow.objects.filter(Q(ReaderID=br.ReaderID) & Q(isDelete=False)
                                        & Q(isAllowed=True) & (Q(ReturnDay__lt=now) | Q(isLegal=False))).count()
        legal = Borrow.objects.filter(Q(ReaderID=br.ReaderID) & Q(isDelete=False)
                                      & Q(isAllowed=True)).count()
        item["legal"] = legal
        item["illegal"] = illegal
    content["borrows"] = zip(borrows, record)
    content["record"] = record
    return render(request, 'lib_admin/borrow/check.html', content)


def check_borrow_op(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return HttpResponse("no")
    if request.method == 'GET':
        way = request.GET.get("way")
        brID = request.GET.get('id')
        br = Borrow.objects.get(id=brID)
        if way == 'agree':
            if br.BookID.NumNow == 0:
                return HttpResponse("在架书籍数量不足，借阅失败")
            else:
                book = br.BookID
                book.NumNow -= 1
                book.ReadTimes += 1
                book.save()
                br.isAllowed = True
                now = datetime.now().date()
                br.BorrowTime = now
                br.ReturnDay = (now + timedelta(days=br.ReaderID.Class.Days))
                br.save()
                m = Message()
                m.ReaderID = br.ReaderID
                m.Title = "借阅申请结果"
                m.Content = "您申请借阅《%s》的请求已通过，阅读愉快！" % book.BName
                m.save()
                return HttpResponse("ok")
        elif way == 'disagree':
            br.isAllowed = False
            m = Message()
            m.ReaderID = br.ReaderID
            m.Title = "借阅申请结果"
            m.Content = "对不起，由于库存或是您的违规情况，您申请借阅《%s》的请求已管理员被拒绝。" % br.BookID.BName
            m.save()
            br.save()
            return HttpResponse("ok")
        else:
            return HttpResponse("no")
    return HttpResponse("no")


def apply_check(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "InfState": "active", "applyState": "active",
        "apply": ApplyClass.objects.all()
    }
    illegal_rate = [dict() for i in content["apply"]]
    now = datetime.now().date()
    for item, rate in zip(content["apply"], illegal_rate):
        illegal = Borrow.objects.filter(Q(ReaderID=item.ReaderID) & Q(isDelete=False)
                                        & Q(isAllowed=True) & (Q(ReturnDay__lt=now) | Q(isLegal=False))).count()
        legal = Borrow.objects.filter(Q(ReaderID=item.ReaderID) & Q(isDelete=False)
                                      & Q(isAllowed=True)).count()
        rate["all"] = legal
        rate["illegal"] = illegal
    content["zip_rate_apply"] = zip(illegal_rate, content["apply"])
    return render(request, "lib_admin/info/class_apply_check.html", content)


def apply_check_ajax(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return HttpResponse("no")
    if request.method == 'GET':
        apply_id = request.GET.get("id")
        way = request.GET.get("way")
        apply = ApplyClass.objects.get(id=apply_id)
        if way == "agree":
            reader = apply.ReaderID
            reader.Class = apply.Class
            reader.save()
            m = Message()
            m.ReaderID = apply.ReaderID
            m.Title = "级别变更申请通过"
            m.Content = "恭喜您，经过管理员的资格审查，您的级别变更申请已通过。"
            m.save()
            apply.delete()
            return HttpResponse("ok")
        elif way == "disagree":
            m = Message()
            m.ReaderID = apply.ReaderID
            m.Title = "级别变更申请驳回"
            m.Content = "对不起，经过管理员的资格审查，您的级别变更申请被拒绝。"
            m.save()
            apply.delete()
            return HttpResponse("ok")
    return HttpResponse("no")


def delete_reader(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "InfState": "active", "deleteReader": "active",
        "readers": Reader.objects.all()
    }
    return render(request, "lib_admin/info/readers.html", content)


def delete_reader_ajax(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return HttpResponse("no")
    if request.method == "GET":
        ReaderID = request.GET.get("id")
        way = request.GET.get("way")
        if way == "delete":
            reader = Reader.objects.get(ReaderID=ReaderID)
            borrow = Borrow.objects.filter(Q(ReaderID=reader) & Q(isAllowed=True) & Q(isReturned=False)).count()
            if borrow > 0:
                return HttpResponse("该读者还有在借图书，只有全部归还完图书后才能撤销账号")
            else:
                user = reader.AccountID
                user.delete()
                reader.delete()
                return HttpResponse("ok")
        elif way == "remind":
            m = Message()
            m.ReaderID_id = ReaderID
            m.Title = "还书提醒"
            m.Content = "管理员提醒您，请及时归还全部图书，谢谢配合。"
            m.save()
            return HttpResponse("ok")
    return HttpResponse("no")


def class_mdf_list(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "InfState": "active", "mdfClassState": "active",
        "classes": ReaderClass.objects.all()
    }
    return render(request, "lib_admin/info/mdf_class.html", content)


def class_mdf(request, ID):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "InfState": "active", "mdfClassState": "active",
    }

    Class = ReaderClass.objects.get(Class=ID)
    content["class"] = Class
    if request.method == "POST":
        form = ClassMdfForm(request.POST, initial={
            "Class": Class.Class,
            "Limited": Class.Limited,
            "Days": Class.Days
        })
        if form.is_valid():
            Class.Days = form.cleaned_data.get("Days")
            Class.Limited = form.cleaned_data.get("Limited")
            Class.save()
            content["work"] = "work"
            content["form"] = form
        else:
            content["form"] = form
    else:
        content["form"] = ClassMdfForm(initial={
            "Class": Class.Class,
            "Limited": Class.Limited,
            "Days": Class.Days
        })

    return render(request, 'lib_admin/info/mdf_class_detail.html', content)


def fine_mdf_list(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "InfState": "active", "mdfFineState": "active",
        "fines": Fine.objects.all().order_by('LimitDay')
    }
    return render(request, "lib_admin/info/mdf_fine.html", content)


def fine_mdf(request, ID):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return render(request, "page404.html")
    content = {
        "LoginUser": LoginUser, "UserAccount": UserAccount,
        "OpenInf": "menu-open", "InfState": "active", "mdfFineState": "active",
    }
    fine = Fine.objects.get(id=ID)
    content["fine"] = fine
    if request.method == "POST":
        form = FineMdfForm(request.POST, initial={
            "LimitDay": fine.LimitDay,
            "FineMoney": fine.FineMoney,
        })
        if form.is_valid():
            fine.LimitDay = form.cleaned_data.get("LimitDay")
            fine.FineMoney = form.cleaned_data.get("FineMoney")
            fine.save()
            content["work"] = "work"
            content["form"] = form
        else:
            content["form"] = form
    else:
        content["form"] = FineMdfForm(initial={
            "LimitDay": fine.LimitDay,
            "FineMoney": fine.FineMoney,
        })

    return render(request, 'lib_admin/info/mdf_fine_detail.html', content)


def admin_class_fine_ajax(request):
    global AccountID, LoginUser, UserAccount
    if AccountID is None or LoginUser is None or UserAccount is None or id is None or UserAccount.Type == '2':
        return HttpResponse("no")
    if request.method == "GET":
        way = request.GET.get("way")
        ID = request.GET.get("id")
        if way == "class":
            if Reader.objects.filter(Class_id=ID).count() > 0:
                return HttpResponse("有读者属于该级别，不能删除")
            else:
                ReaderClass.objects.get(Class=ID).delete()
                return HttpResponse("ok")
        elif way == "fine":
            if ID == '10':
                return HttpResponse("最高处罚机制只能修改不能删除")
            else:
                Fine.objects.get(id=ID).delete()
                return HttpResponse("ok")
    return HttpResponse("no")
