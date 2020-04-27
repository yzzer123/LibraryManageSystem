from django.contrib import admin

from BuctLib.models import *


class BookAdmin(admin.ModelAdmin):
    """
    图书管理类
    """
    list_display = ['BookID', "BName", "Publisher",
                    "Version", "Author", "Content",
                    "NumInLib", "NumNow", "Area",
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
        "Gender", "MName",
    ]


class ReaderAdmin(admin.ModelAdmin):
    """
    读者管理类
    """
    list_display = [
        "StudentID", "AccountID",
        "Gender", "SName", "School", "BLimit"
    ]


class BorrowAdmin(admin.ModelAdmin):
    """
    阅读记录管理类
    """
    list_display = [
        "StudentID", "BookID", "BorrowTime",
        "BorrowDay", "ReNewTimes"
    ]


class MessageAdmin(admin.ModelAdmin):
    """
    消息管理类
    """
    list_display = [
        "Title", "StudentID", "Content",
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
