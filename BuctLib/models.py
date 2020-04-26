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
        ('1', '思政类'),
        ('2', '哲学类'),
        ('3', '社会科学类'),
        ('4', '军事类'),
        ('5', '经济类'),
        ('6', '文化科学类'),
        ('7', '语言文字类'),
        ('8', '文学类'),
        ('9', '艺术类'),
        ('10', '体育类'),
        ('11', '历史地理类'),
        ('12', '自然科学总论类'),
        ('13', '数理化学类'),
        ('14', '天文地球科学类'),
        ('15', '生物科学理类'),
        ('16', '医药类'),
        ('17', '农业科学类'),
        ('18', '工业技术类'),
        ('19', '交通运输类'),
        ('20', '航空航天类'),
        ('21', '环境科学类'),
        ('22', '计算机类'),
        ('23', '未分类')
    ]


class Book(models.Model):
    """
    图书类  查询图书信息
    主键： 图书编号 BookID
    属性： ISBN ISBN 书名BName  出版社Publisher  版本 Version
    作者 Author 图书简介 Content 馆藏数量 NumInLib 在架数量 NumNow
    所属区域 Area 分类 Category 出版时间 PubTime
    ReadTimes 阅读数
    TODO(yzzer) 图书封面 BImage
    """
    BookID = models.AutoField(primary_key=True, db_index=True)
    BName = models.CharField(max_length=20)
    Publisher = models.CharField(max_length=20)
    Version = models.CharField(max_length=20)
    Author = models.CharField(max_length=20)
    Content = models.TextField(default="无", blank=True, null=True)
    NumInLib = models.PositiveSmallIntegerField(default=0)
    NumNow = models.PositiveSmallIntegerField(default=0)
    Area = models.CharField(max_length=20, choices=LibFloor)
    Category = models.CharField(max_length=30, default="未分类", choices=CATEGORY_CHOICE)
    PubTime = models.DateField(default="1999-10-11")
    ReadTimes = models.IntegerField(default=0)


class User(models.Model):
    """
     用户类 用于登陆
     主键： 账户名 AccountID
     属性： 密码 Password 账户类别 Type
     """
    AccountID = models.CharField(max_length=20, primary_key=True, db_index=True)
    Password = models.SlugField(max_length=40)
    Type = models.CharField(choices=ACCOUNT_TPYE, default="读者", max_length=20)  # 默认为普通用户


class Manager(models.Model):
    """
    管理员类 查询管理员信息
    主键： 工号 ManagerID
    外键： 账户名 AccountID
    属性： 电话 Phone 邮箱Mail 性别 Gender 姓名 MName
    TODO(yzzer) 管理员照片 MImage
    """

    ManagerID = models.CharField(primary_key=True, max_length=20, db_index=True)
    AccountID = models.OneToOneField(User, on_delete=models.CASCADE)
    Phone = models.CharField(max_length=20, unique=True)
    Mail = models.EmailField(unique=True)
    Gender = models.CharField(max_length=20, choices=GENDER_CHOICE, default="保密")
    MName = models.CharField(max_length=20)


class Reader(models.Model):
    """
     读者类 查阅读者信息
     主键： 学号 StudentID
     外键： 账户名 AccountID
     属性： 电话 Phone 邮箱Mail 性别 Gender 姓名 SName
     学院 School 借书量 BLimit
    TODO(yzzer) 读者照片 MImage
     """
    StudentID = models.CharField(primary_key=True, max_length=20, db_index=True)
    AccountID = models.OneToOneField(User, on_delete=models.CASCADE)
    Phone = models.CharField(max_length=20, unique=True)
    Mail = models.EmailField(unique=True)
    Gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default="保密")
    SName = models.CharField(max_length=20)
    School = models.CharField(max_length=20, choices=SCHOOLS, default="信息技术与科学学院")
    BLimit = models.IntegerField(default=3)


class Borrow(models.Model):
    """
    借阅记录类
    主键 学号 StudentID &&  图书编号 BookID
    外键 学号 StudentID &&  图书编号 BookID
    借书时间 BorrowTime 借书天数BorrowDay
    续借次数 RenewTimes
    """

    StudentID = models.ForeignKey(Reader, on_delete=models.DO_NOTHING)
    BookID = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    BorrowTime = models.DateField(auto_now_add=True)
    BorrowDay = models.PositiveSmallIntegerField(default=30)
    ReNewTimes = models.IntegerField(default=3)

    class Meta:
        unique_together = ('StudentID', 'BookID',)


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
    StudentID = models.ForeignKey(Reader, on_delete=models.DO_NOTHING)
    Content = models.TextField()
    MTime = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=20, choices=STATUS, default="未读")


class Notice(models.Model):
    """
    公告类
    """
    Title = models.CharField(max_length=255)
    NTime = models.DateTimeField(auto_now_add=True)
    Content = models.TextField()
    ReadTimes = models.IntegerField(default=0)


