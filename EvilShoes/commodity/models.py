from django.db import models


# Create your models here.
class CommodityInfo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='商品ID')
    name = models.CharField(verbose_name='商品名', max_length=180, null=False)
    shelves = models.BooleanField(verbose_name='是否在售', default=True)
    price = models.DecimalField(verbose_name='商品价格', max_digits=6, decimal_places=2, null=False)
    description = models.TextField(verbose_name='商品描述')
    images = models.ImageField(verbose_name='商品图片', upload_to='commodity/',
                               blank=True, null=True)
    classify = models.ForeignKey('CommodityClassify', verbose_name='商品分类', on_delete=models.CASCADE)

    class Meta:
        db_table = 'commodity_info'
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name


class CommodityClassify(models.Model):
    name = models.CharField(verbose_name='分类名字', max_length=150, null=False)
    description = models.TextField(verbose_name='分类描述')

    class Meta:
        db_table = 'commodity_classify'
        verbose_name = '商品分类信息'
        verbose_name_plural = verbose_name
