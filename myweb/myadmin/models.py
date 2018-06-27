from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 80)
    email = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 11)
    age = models.IntegerField(null = True)
    sex = models.CharField(max_length = 1 , null = True)
    # 图片picture
    pic = models.CharField(max_length = 100, null = True)
    # 0 正常 1 禁用
    status = models.IntegerField(default = 0)
    addtime = models.DateTimeField(auto_now_add = True)


# 后台：商品分类模型types
class Types(models.Model):
    """
    允许无限分类
    实际使用时多为2级，少数3级，4级已经不常用，因为层数越多，
    递归查询越慢，层数过高时，失去了使用价值
    types
        id      name        pid   path
        1       手机        0     0
         2      苹果手机     1      0，1
           3    女士手机     2      0,1,2
            （4）粉色手机     3       0,1,2,3
    """
    name = models.CharField(max_length = 20)
    pid = models.IntegerField()
    # 路径是个拼接的字符串，不是列表
    path = models.CharField(max_length = 50)
            
# 商品模型
class Goods(models.Model):
    # 一对多，一个typeid对应Types里面的多个分类（或者称之为标签）
    typeid = models.ForeignKey(to ="Types", to_field="id")
    title = models.CharField(max_length=255)
    descr = models.CharField(max_length=255)
    info = models.TextField(null = True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    pics = models.CharField(max_length=100)
    # 0 新发布，1 下架，还可以设置更多状态
    status = models.IntegerField(default = 0)
    store = models.IntegerField(default = 0)
    num = models.IntegerField(default = 0)
    clicknum = models.IntegerField(default = 0)
    addtime = models.DateTimeField(auto_now_add = True)