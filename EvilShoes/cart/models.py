from django.db import models

# Create your models here.
from user.models import UserInfo


class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo)
    name = models.CharField(verbose_name='商品名称', max_length=128)
    count = models.IntegerField(verbose_name='商品数量')

    class Meta:
        db_table = 'cart_info'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
