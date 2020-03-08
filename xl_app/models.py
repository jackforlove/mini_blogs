from django.db import models

# Create your models here.
class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)

class Cate(models.Model):#每个人对应的博客
    caption=models.CharField(max_length=16)
    user = models.OneToOneField(UserInfo,on_delete=models.CASCADE)
class Artcate(models.Model):#文章分类
    caption=models.CharField(max_length=16)
    blog = models.ForeignKey(verbose_name='所属博客', to='Cate',on_delete=models.CASCADE)
class Articl(models.Model):#文章
    title=models.CharField(max_length=25)
    content=models.CharField(max_length=1000)
    cate=models.ForeignKey(Cate,on_delete=models.CASCADE)
    artcate=models.ForeignKey(Artcate,on_delete=models.CASCADE,default=1)
    comment_count = models.IntegerField(default=0)
    type_choices = [
        (1, "分类阅读"),
        (2, "公开课"),
        (3, "每日精选"),
        (4, "提升自我"),
        (5, "技术区"),
        (6, "灌水区"),
        (7, "创作区"),
    ]
    article_type_id = models.IntegerField(choices=type_choices, default=1)
