from django.contrib import admin

from BuctLib.models import *


class BookAdmin(admin.ModelAdmin):
    """
    图书管理类
    """
    list_display = ['BookID', "BName", "Publisher", "Author", "Content",
                    "NumInLib", "NumNow",
                    "Category", "PubTime", "ReadTimes"
                    ]


class UserAdmin(admin.ModelAdmin):
    """
    用户管理类
    """
    list_display = [
        "AccountID", "Password", "Type", "Email", "Tel"
    ]


class ManagerAdmin(admin.ModelAdmin):
    """
    管理员管理类
    """
    list_display = [
        "ManagerID", "AccountID",
        "Gender", "Name",
    ]


class ApplyAdmin(admin.ModelAdmin):
    list_display = [
        "ReaderID", "Class", "Message"
    ]


class ReaderAdmin(admin.ModelAdmin):
    """
    读者管理类
    """
    list_display = [
        "ReaderID", "AccountID",
        "Gender", "Name", "School", "Type", "Class"
    ]


class FineAdmin(admin.ModelAdmin):
    list_display = [
        "LimitDay", "FineMoney"
    ]


class ReaderClassAdmin(admin.ModelAdmin):
    list_display = [
        "Class", "Limited", "Days"
    ]


class BorrowAdmin(admin.ModelAdmin):
    """
    阅读记录管理类
    """
    list_display = [
        "ReaderID", "BookID", "BorrowTime",
        "ReturnDay", "isReBorrowed", "isDelete", 'isLegal', 'isAllowed', 'isReturned',
        "RealreturnDay"
    ]


class MessageAdmin(admin.ModelAdmin):
    """
    消息管理类
    """
    list_display = [
        "Title", "ReaderID", "Content",
        "MTime"
    ]


class NoticeAdmin(admin.ModelAdmin):
    """
    公告管理类
    """
    list_display = [
        "Title", "NTime", "Content"
    ]


admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Borrow, BorrowAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(ReaderClass, ReaderClassAdmin)
admin.site.register(Fine, FineAdmin)
admin.site.register(ApplyClass, ApplyAdmin)
