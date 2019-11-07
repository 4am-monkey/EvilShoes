from django.db import models

# Create your models here.
from user.models import UserInfo


class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo)
    name = models.CharField(verbose_name='商品名称', max_length=128)
    unit_price = models.DecimalField(verbose_name='商品单价', max_digits=6, decimal_places=2)
    count = models.IntegerField(verbose_name='商品数量')

    # total_price = models.FloatField(verbose_name='总价', default=unit_price * count)

    class Meta:
        db_table = 'cart_info'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        """
            定义每个数据对象的显示信息
        """
        return self.name
