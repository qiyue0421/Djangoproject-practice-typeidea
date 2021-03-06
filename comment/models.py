from django.db import models
from blog.models import Post

# Create your models here.


# 评论Model
class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NORMAL, '正常'), (STATUS_DELETE, '删除'),)
    # target = models.ForeignKey(Post, verbose_name='评论目标')  # 暂时使用一对一的关系，耦合到文章上
    target = models.CharField(max_length=100, verbose_name='评论目标')  # 存放任意字符，兼容更多场景
    content = models.CharField(max_length=2000, verbose_name='内容')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return self.target

    @classmethod
    def get_comments(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)

    @classmethod
    def get_by_target(cls, target):  # 提供接口，返回某篇文章下的所有有效评论
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)
