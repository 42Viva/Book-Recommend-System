from django.db import models
from django.db.models import Avg


class User(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name="账号")
    password = models.CharField(max_length=32, verbose_name="密码")
    phone = models.CharField(max_length=32, verbose_name="手机号码")
    name = models.CharField(max_length=32, unique=True, verbose_name="名字")
    address = models.CharField(max_length=32, verbose_name="地址")
    email = models.EmailField(verbose_name="邮箱")

    class Meta:
        verbose_name_plural = "用户"
        verbose_name = "用户"

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=32, verbose_name="标签")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Book(models.Model):
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name="标签",
        related_name="tags",
        blank=True,
        null=True,
    )
    collect = models.ManyToManyField(User, verbose_name="收藏者", blank=True)
    sump = models.IntegerField(verbose_name="收藏人数", default=0)
    rate_num = models.IntegerField(verbose_name="评分人数", default=0)
    title = models.CharField(verbose_name="书名", max_length=32)
    author = models.CharField(verbose_name="作者", max_length=32)
    intro = models.TextField(verbose_name="描述")
    num = models.IntegerField(verbose_name="浏览量", default=0)
    pic = models.FileField(verbose_name="封面图片", max_length=64, upload_to='book_cover')
    prize = (("诺贝尔文学奖", "诺贝尔文学奖"), ("茅盾文学奖", "茅盾文学奖"), ("None", "None"))
    good = models.CharField(
        verbose_name="获奖", max_length=32, default=None, choices=prize
    )

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = "图书"

    def __str__(self):
        return self.title


class Rate(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, blank=True, null=True, verbose_name="图书id"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="用户id",
    )
    mark = models.FloatField(verbose_name="评分")
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)

    @property
    def avg_mark(self):
        average = Rate.objects.all().aggregate(Avg('mark'))['mark__avg']
        return average

    class Meta:
        verbose_name = "评分信息"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content = models.TextField(verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True)
    good = models.IntegerField(verbose_name="点赞", default=0)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="书籍")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name


class MessageBoard(models.Model):
    # 读书论坛
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    title = models.CharField(max_length=64, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    look_num = models.IntegerField(verbose_name='点击数', default=1)
    like_num = models.IntegerField(verbose_name='点赞数', default=0)
    feebback_num = models.IntegerField(verbose_name='回复数', default=0)
    collect_num = models.IntegerField(verbose_name='收藏数', default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "留言"
        verbose_name_plural = verbose_name


class CollectBoard(models.Model):
    # 收藏、点赞留言帖子
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    message_board = models.ForeignKey(MessageBoard, on_delete=models.CASCADE, verbose_name="留言")
    create_time = models.DateTimeField(auto_now_add=True)
    is_collect = models.BooleanField(default=False, verbose_name='是否收藏')
    is_like = models.BooleanField(default=False, verbose_name='是否点赞')

    class Meta:
        verbose_name = "收藏/点赞留言"
        verbose_name_plural = verbose_name


class BoardComment(models.Model):
    # 回复留言
    message_board = models.ForeignKey(MessageBoard, on_delete=models.CASCADE, verbose_name="留言")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="用户", related_name="user"
    )
    content = models.TextField( verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "子留言"
        verbose_name_plural = verbose_name


class Num(models.Model):
    #数据统计
    users = models.IntegerField(verbose_name="用户数量", default=0)
    books = models.IntegerField(verbose_name="书本数量", default=0)
    comments = models.IntegerField(verbose_name="评论数量", default=0)
    rates = models.IntegerField(verbose_name="评分汇总", default=0)
    message_boards = models.IntegerField(verbose_name="留言汇总", default=0)

    class Meta:
        verbose_name = "数据统计"
        verbose_name_plural = verbose_name

