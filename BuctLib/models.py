from django.db import models


GENDER_CHOICE = [
    ('1', '男'),
    ('2', '女'),
    ('3', '保密')
]


LibFloor = [
    ('1', '图书馆一层'),
    ('2', '图书馆二层'),
    ('3', '图书馆三层'),
    ('4', '图书馆四层'),
]

SCHOOLS = [
    ('1', '信息技术与科学学院'),
    ('2', '材料科学与工程学院'),
    ('3', '机电工程学院'),
    ('4', '化学工程学院'),
    ('5', '经济管理学院'),
    ('6', '化学学院'),
    ('7', '数理学院'),
    ('8', '文法学院'),
    ('9', '生命科学与技术学院'),
    ('10', '继续教育学院'),
    ('11', '马克思主义学院'),
    ('12', '国际教育学院'),
    ('13', '侯德榜工程师学院'),
    ('14', '巴黎居里工程师学院'),

]

ACCOUNT_TPYE = [
    ('1', '管理员'),
    ('2', '读者'),
]

CATEGORY_CHOICE = [
        ('思政类', '思政类'),
        ('哲学类', '哲学类'),
        ('社会科学类', '社会科学类'),
        ('军事类', '军事类'),
        ('经济类', '经济类'),
        ('文化科学类', '文化科学类'),
        ('语言文字类', '语言文字类'),
        ('文学类', '文学类'),
        ('艺术类', '艺术类'),
        ('体育类', '体育类'),
        ('历史地理类', '历史地理类'),
        ('自然科学总论类', '自然科学总论类'),
        ('数理化学类', '数理化学类'),
        ('天文地球科学类', '天文地球科学类'),
        ('生物科学理类', '生物科学理类'),
        ('医药类', '医药类'),
        ('农业科学类', '农业科学类'),
        ('工业技术类', '工业技术类'),
        ('交通运输类', '交通运输类'),
        ('航空航天类', '航空航天类'),
        ('环境科学类', '环境科学类'),
        ('计算机类', '计算机类'),
        ('未分类', '未分类')
    ]


class Book(models.Model):
    """
    图书类  查询图书信息
    主键： 图书编号 BookID
    属性： ISBN ISBN 书名BName  出版社Publisher
    作者 Author 图书简介 Content 馆藏数量 NumInLib 在架数量 NumNow
    分类 Category 出版时间 PubTime
    ReadTimes 阅读数
    TODO(yzzer) 图书封面 BImage
    """
    BookID = models.AutoField(primary_key=True, db_index=True)
    BName = models.CharField(max_length=40)
    Publisher = models.CharField(max_length=40)
    Author = models.CharField(max_length=30)
    Content = models.TextField(default="无", blank=True, null=True)
    Price = models.FloatField(default=30.0)
    NumInLib = models.PositiveSmallIntegerField(default=0)
    NumNow = models.PositiveSmallIntegerField(default=0)
    Category = models.CharField(max_length=30, default="未分类", choices=CATEGORY_CHOICE)
    PubTime = models.DateField(default="1999-10-11")
    ReadTimes = models.IntegerField(default=0)

    def __str__(self):
        return self.BName


class User(models.Model):
    """
     用户类 用于登陆
     主键： 账户名 AccountID
     属性： 密码 Password 账户类别 Type
        邮箱 Email 电话 Tel
     """
    AccountID = models.CharField(max_length=40, primary_key=True, db_index=True)
    Password = models.CharField(max_length=40)
    Type = models.CharField(choices=ACCOUNT_TPYE, default="读者", max_length=10)  # 默认为普通用户
    Email = models.EmailField(unique=True)
    Tel = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.AccountID


class Manager(models.Model):
    """
    管理员类 查询管理员信息
    主键： 工号 ManagerID
    外键： 账户名 AccountID
    属性：  性别 Gender 姓名 MName
    TODO(yzzer) 管理员照片 MImage
    """

    ManagerID = models.CharField(primary_key=True, max_length=30, db_index=True)
    AccountID = models.OneToOneField(to="User", on_delete=models.CASCADE)
    Gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default="保密")
    Name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.ManagerID


class ReaderClass(models.Model):
    """
    读者级别类
    Class为级别
    Limited为可借阅数量
    Day为借阅天数
    """
    Class = models.CharField(max_length=4, primary_key=True, db_index=True)
    Limited = models.PositiveSmallIntegerField(default=3)
    Days = models.PositiveSmallIntegerField(default=30, null=True)

    def __str__(self):
        return self.Class


class Reader(models.Model):
    """
     读者类 查阅读者信息
     主键： 学号 ReaderID
     外键： 账户名 AccountID
     属性：  性别 Gender 姓名 SName
     学院 School
     类型 Type
    TODO(yzzer) 读者照片 MImage
     """
    ReaderID = models.CharField(primary_key=True, max_length=30, db_index=True)
    AccountID = models.OneToOneField(User, on_delete=models.CASCADE)
    Gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default="保密")
    Name = models.CharField(max_length=30, null=True, blank=True)
    School = models.CharField(max_length=30, choices=SCHOOLS, default="信息技术与科学学院")
    Class = models.ForeignKey(to="ReaderClass", on_delete=models.SET_DEFAULT, default="A")
    Type = models.CharField(max_length=10, choices=[('1', '学生'), ('2', '教职工')],  default='学生')

    def __str__(self):
        return self.ReaderID


class Fine(models.Model):
    """
    处罚规则类
    LimitDay是小于该期限的处罚金额
    FineMoney是处罚金额
    """
    LimitDay = models.PositiveSmallIntegerField(unique=True, db_index=True)
    FineMoney = models.PositiveSmallIntegerField(default=10)


class ApplyClass(models.Model):
    """
        借阅记录类
        主键 默认id
        外键 class 申请的级别 ReaderID 申请的读者ID号
    """
    Class = models.ForeignKey(to="ReaderClass", on_delete=models.CASCADE)
    ReaderID = models.ForeignKey(to="Reader", on_delete=models.CASCADE)
    Message = models.TextField(default="")


class Borrow(models.Model):
    """
    借阅记录类
    主键 学号 ReaderID &&  图书编号 BookID
    外键 学号 ReaderID &&  图书编号 BookID
    借书时间 BorrowTime 还书日期 returnTime
    续借状态 isReBorrowed
    """
    ReaderID = models.ForeignKey(to="Reader", on_delete=models.CASCADE)
    BookID = models.ForeignKey(to="Book", on_delete=models.CASCADE)
    BorrowTime = models.DateField(auto_now_add=True)
    ReturnDay = models.DateField(auto_now_add=True)
    RealreturnDay = models.DateField(default='2020-01-01')
    isReBorrowed = models.BooleanField(default=False)
    isLegal = models.NullBooleanField(default=True)
    isDelete = models.BooleanField(default=False)
    isReturned = models.BooleanField(default=False)
    isAllowed = models.NullBooleanField(null=True)

    def __str__(self):
        return "学生%s借了%s书" % (self.ReaderID, self.BookID)


class BuyIn(models.Model):
    """
    进货类
    TODO(yzzer) 记录进货厂商 进货时间 进货书籍 进货负责人（管理员）
    """
    pass


class Message(models.Model):
    """
    消息类
    """
    STATUS = [
        ('1', '已读'),
        ('2', '未读')
    ]
    Title = models.CharField(max_length=255, verbose_name='消息标题')
    ReaderID = models.ForeignKey(to="Reader", on_delete=models.CASCADE)
    Content = models.TextField()
    MTime = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=20, choices=STATUS, default="未读")

    def __str__(self):
        return "消息主题：" + self.Title


class Notice(models.Model):
    """
    公告类
    """
    Title = models.CharField(max_length=40)
    NTime = models.DateTimeField(auto_now_add=True)
    Content = models.TextField()
    ReadTimes = models.IntegerField(default=0)

    def __str__(self):
        return "公告主题：" + self.Title

