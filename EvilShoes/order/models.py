from django.db import models

# Create your models here.
from user.models import UserInfo

ORDER_STATUS = (
    (0, "未付款"),
    (1, "等待发货"),
    (2, "配送中"),
    (3, "已完成"),
    (4, "支付失败"),
    (5, "已取消"),
    (6, "订单关闭"),
)


class OrderInfo(models.Model):
    user = models.ForeignKey(UserInfo)
    id = models.AutoField(verbose_name='订单ID', primary_key=True)
    addr_id = models.IntegerField(verbose_name='收货地址ID')
    total_count = models.IntegerField(verbose_name='订单商品总数')
    total_price = models.DecimalField(verbose_name='订单总价', max_digits=6, decimal_places=2)
    create_time = models.DateTimeField(verbose_name='订单创建时间', auto_now_add=True)
    status = models.IntegerField(verbose_name='订单状态', choices=ORDER_STATUS, default=0)

    class Meta:
        db_table = 'order_info'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        """
            定义每个数据对象的显示信息
        """
        # return self.id
        return str(self.id)


class OrderGoods(models.Model):
    goods_id = models.IntegerField(verbose_name="商品名称", default=0)
    price = models.DecimalField(verbose_name='商品价格', max_digits=6, decimal_places=2)
    # desc = models.CharField(verbose_name='描述', max_length=1000, null=True)
    count = models.IntegerField(verbose_name="数量", null=True, default=0)
    # color = models.CharField('颜色', max_length=50)
    # spec = models.CharField('规格', max_length=50)
    # goodsimg = models.ImageField("产品图", upload_to="ordersgood", default="normal.png")
    # trprice = models.DecimalField('商品实际', max_digits=8, decimal_places=2)
    order = models.ForeignKey(OrderInfo)

    class Meta:
        db_table = 'order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        """
            定义每个数据对象的显示信息
        """
        return self.name
