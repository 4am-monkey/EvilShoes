from django.db import models

# Create your models here.
from user.models import UserInfo


class Favourite(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='商品ID')
    name = models.CharField(verbose_name='商品名', max_length=180, null=False)
    description = models.TextField(verbose_name='商品描述')
    images = models.ImageField(verbose_name='商品图片', upload_to='commodity/', blank=True, null=True)
    user = models.ForeignKey('UserInfo', verbose_name='用户收藏', on_delete=models.CASCADE)

    class Meta:
        db_table = 'favourite'
        verbose_name = '收藏商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        """
            定义每个数据对象的显示信息
        """
        return self.name
